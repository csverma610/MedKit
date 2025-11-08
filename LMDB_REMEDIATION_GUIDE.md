# LMDB Implementation Remediation Guide

## Overview
This guide shows how to add LMDB caching to the 12 modules currently missing it.

## Pattern 1: Physical Exam Modules (8 modules)

### Files to Modify
```
medkit/phyexams/exam_depression_screening.py
medkit/phyexams/exam_nutrition_growth.py
medkit/phyexams/exam_breast_axillae.py
medkit/phyexams/exam_emotional_stability.py
medkit/phyexams/exam_blood_vessels.py
medkit/phyexams/exam_attention_span.py
medkit/phyexams/exam_judgement.py
medkit/phyexams/exam_musculoskeletal.py
```

### Current Structure (Example from exam_depression_screening.py)
```python
from medkit.core.medkit_client import MedKitClient

def generate_depression_questions(
    age: int = None,
    gender: str = None,
    verbose: bool = False
):
    """Generate depression screening questions."""

    client = MedKitClient()
    # ... generate questions
    result = client.generate(prompt)  # ❌ NO CACHING
    return result
```

### Required Changes

#### Step 1: Add Imports
```python
# Add these imports
from medkit.utils.lmdb_storage import LMDBStorage, LMDBConfig
import hashlib
import json
from pydantic import BaseModel
```

#### Step 2: Create Config Class
```python
class ExamConfig(BaseModel):
    """Configuration for exam question generation."""

    # Existing config options...

    # NEW: LMDB Caching
    db_store: bool = True
    db_path: str = ".medkit_cache"
    db_capacity_mb: int = 5000
    db_overwrite: bool = False

    class Config:
        allow_population_by_field_name = True
```

#### Step 3: Create Generator Class
```python
class ExamQuestionGenerator:
    """Generate exam questions with LMDB caching."""

    def __init__(self, config: ExamConfig = None):
        self.config = config or ExamConfig()
        self.client = MedKitClient()
        self.storage = None

        # Initialize LMDB
        if self.config.db_store:
            try:
                lmdb_config = LMDBConfig(
                    db_path=self.config.db_path,
                    capacity_mb=self.config.db_capacity_mb,
                    enable_logging=True,
                    compression_threshold=100
                )
                self.storage = LMDBStorage(config=lmdb_config)
                logger.info(f"LMDB initialized at {self.config.db_path}")
            except Exception as e:
                logger.error(f"LMDB init failed: {e}")
                self.storage = None

    def _generate_cache_key(self, age: int, gender: str, exam_type: str) -> str:
        """Generate unique cache key."""
        query = f"{exam_type}:{age}:{gender}"
        return hashlib.sha256(query.encode()).hexdigest()

    def generate_depression_questions(self, age: int = None, gender: str = None):
        """Generate depression screening questions with caching."""
        cache_key = self._generate_cache_key(age, gender, "depression")

        # Check cache
        if self.config.db_store and self.storage and not self.config.db_overwrite:
            cached = self.storage.get(cache_key)
            if cached:
                logger.info("Depression questions retrieved from cache")
                return json.loads(cached)

        # Generate via LLM
        logger.info("Generating depression questions via LLM")
        prompt = f"Generate depression screening questions for age {age}, gender {gender}"
        result = self.client.generate(prompt)

        # Cache result
        if self.config.db_store and self.storage:
            try:
                self.storage.put(cache_key, json.dumps(result))
                logger.info(f"Cached with key: {cache_key[:16]}...")
            except Exception as e:
                logger.warning(f"Failed to cache: {e}")

        return result
```

#### Step 4: Update Module Function
```python
# Replace old function with wrapper
def generate_depression_questions(
    age: int = None,
    gender: str = None,
    verbose: bool = False,
    db_store: bool = True,
    db_path: str = ".medkit_cache"
):
    """Generate depression screening questions."""

    config = ExamConfig(
        db_store=db_store,
        db_path=db_path
    )
    generator = ExamQuestionGenerator(config)
    return generator.generate_depression_questions(age, gender)
```

### Testing for Physical Exam Modules

```python
import unittest

class TestExamCaching(unittest.TestCase):

    def test_depression_questions_cache_hit(self):
        """Test that second call uses cache."""
        config = ExamConfig(db_store=True, db_overwrite=False)
        gen = ExamQuestionGenerator(config)

        # First call - hits API
        result1 = gen.generate_depression_questions(age=35, gender="M")

        # Second call - hits cache
        result2 = gen.generate_depression_questions(age=35, gender="M")

        # Results should be identical
        self.assertEqual(result1, result2)

    def test_different_params_no_cache_hit(self):
        """Test that different params don't use same cache."""
        config = ExamConfig(db_store=True)
        gen = ExamQuestionGenerator(config)

        result1 = gen.generate_depression_questions(age=35, gender="M")
        result2 = gen.generate_depression_questions(age=45, gender="F")

        # Results should be different (from different API calls)
        self.assertNotEqual(result1, result2)

    def test_cache_disabled(self):
        """Test that db_store=False disables caching."""
        config = ExamConfig(db_store=False)
        gen = ExamQuestionGenerator(config)

        # Both calls should hit API (no caching)
        result = gen.generate_depression_questions(age=35, gender="M")
        self.assertIsNotNone(result)
```

---

## Pattern 2: Analysis/Generation Modules (4 modules)

### Files to Modify
```
medkit/medical/eval_physical_exam_questions.py
medkit/medical/prescription_analyzer.py
medkit/medical/prescription_extractor.py
medkit/medical/user_guide.py
```

### Example: prescription_analyzer.py

#### Current Code ❌
```python
def analyze_prescription(prescription_data: dict) -> dict:
    """Analyze prescription information."""
    client = MedKitClient()
    prompt = f"Analyze prescription: {prescription_data}"
    result = client.generate(prompt)  # NO CACHING
    return result
```

#### Fixed Code ✅
```python
class PrescriptionAnalyzerConfig(BaseModel):
    db_store: bool = True
    db_path: str = ".medkit_cache"
    db_capacity_mb: int = 5000
    db_overwrite: bool = False

class PrescriptionAnalyzer:
    def __init__(self, config: PrescriptionAnalyzerConfig = None):
        self.config = config or PrescriptionAnalyzerConfig()
        self.client = MedKitClient()
        self.storage = None

        if self.config.db_store:
            try:
                lmdb_config = LMDBConfig(
                    db_path=self.config.db_path,
                    capacity_mb=self.config.db_capacity_mb,
                    enable_logging=True,
                    compression_threshold=100
                )
                self.storage = LMDBStorage(config=lmdb_config)
            except Exception as e:
                logger.error(f"LMDB init failed: {e}")
                self.storage = None

    def _generate_cache_key(self, drug_name: str, dosage: str) -> str:
        """Generate cache key from prescription data."""
        query = f"analyze:{drug_name}:{dosage}"
        return hashlib.sha256(query.encode()).hexdigest()

    def analyze(self, drug_name: str, dosage: str) -> dict:
        """Analyze prescription with caching."""
        cache_key = self._generate_cache_key(drug_name, dosage)

        # Check cache
        if self.config.db_store and self.storage and not self.config.db_overwrite:
            cached = self.storage.get(cache_key)
            if cached:
                logger.info(f"Prescription analysis cached for {drug_name}")
                return json.loads(cached)

        # Generate
        prompt = f"Analyze prescription: {drug_name} {dosage}"
        result = self.client.generate(prompt)

        # Cache
        if self.config.db_store and self.storage:
            try:
                self.storage.put(cache_key, json.dumps(result))
            except Exception as e:
                logger.warning(f"Cache failed: {e}")

        return result

def analyze_prescription(drug_name: str, dosage: str):
    """Public API for prescription analysis."""
    config = PrescriptionAnalyzerConfig()
    analyzer = PrescriptionAnalyzer(config)
    return analyzer.analyze(drug_name, dosage)
```

---

## Implementation Checklist

### For Each Module:

- [ ] Add LMDB imports
- [ ] Create Config class with db_store, db_path, db_capacity_mb, db_overwrite
- [ ] Create Generator/Analyzer class
- [ ] Implement `_generate_cache_key()` method
- [ ] Update main function to use Generator class
- [ ] Add logging for cache hits/misses
- [ ] Add try/except for LMDB errors
- [ ] Create unit tests for caching
- [ ] Test cache hit behavior
- [ ] Test different params create different keys
- [ ] Test db_store=False disables caching
- [ ] Test db_overwrite=True bypasses cache
- [ ] Document cache key generation
- [ ] Update module docstring with caching info

---

## Validation Steps

After implementing LMDB in all 12 modules:

### 1. Verify Imports
```bash
grep -n "LMDBStorage\|lmdb_storage" medkit/**/*.py
```
Should return all 12 modules + existing 26 modules = 38 total

### 2. Verify Storage Init
```bash
grep -n "self.storage = LMDBStorage" medkit/**/*.py
```
Should show all modules creating storage instances

### 3. Verify Cache Keys
```bash
grep -n "_generate_cache_key\|hashlib.sha256" medkit/**/*.py
```
Should show all modules generating deterministic keys

### 4. Run Tests
```bash
python -m pytest tests/test_*_*_interaction.py -v
python -m pytest tests/test_*_info.py -v
```
Verify all caching tests pass

---

## Performance Metrics to Track

After implementation, monitor:

1. **Cache Hit Rate**
   - Target: >50% for common operations
   - Measure: cache hits / total requests

2. **Response Time**
   - Cache hit: <10ms
   - Cache miss: 3-5 seconds
   - Improvement: 3-5x faster for hits

3. **API Token Usage**
   - Before: N calls × cost per call
   - After: (N × hit rate) × cost per call
   - Savings: 60-80% for common queries

4. **LMDB Database Size**
   - Monitor storage growth
   - Implement eviction if needed

---

## Priority Implementation Order

### Week 1: Physical Exams (8 modules)
- Most frequently used
- Highest impact
- Easiest to implement
- Estimated time: 2-3 hours

### Week 2: Prescription Modules (2 modules)
- Medium frequency
- Medium complexity
- Estimated time: 1-2 hours

### Week 3: Analysis & Guides (2 modules)
- Lower frequency
- Easy implementation
- Estimated time: 1-2 hours

---

## Success Criteria

- ✅ All 12 modules have LMDB storage initialized
- ✅ All modules generate deterministic cache keys
- ✅ Cache hit logs are visible in logs
- ✅ First call slower (API), second call faster (<10ms)
- ✅ db_overwrite=True properly bypasses cache
- ✅ db_store=False properly disables caching
- ✅ Comprehensive tests for all implementations
- ✅ Performance gains measurable in benchmarks
- ✅ Documentation updated with cache info
- ✅ No regression in functionality

---

**Guide Created:** 2025-11-08
**Modules to Fix:** 12
**Estimated Time:** 4-6 hours
**Expected Benefit:** 3-5x faster repeated queries, 60-80% API token savings

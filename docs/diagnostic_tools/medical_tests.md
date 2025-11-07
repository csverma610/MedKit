# Medical Tests Module

## Overview
Comprehensive information about diagnostic medical tests.

**What it does:** Explains what tests measure, how they're performed, and what results mean.
**Why it matters:** Understanding tests helps patients prepare, reduces anxiety, and lets them understand results.

---

## Scope
This module covers diagnostic medical tests and laboratory tests.

---

## What It Does

When you look up a medical test, you get:

- **Test name:** Official name and common names
- **What it measures:** What the test detects or quantifies
- **Why ordered:** Medical indications for the test
- **How performed:** Step-by-step procedure description
- **Sample needed:** What biological sample is required (blood, urine, etc.)
- **Sample collection:** How the sample is collected
- **Preparation needed:** What patient must do before test
- **Discomfort level:** How uncomfortable the test is
- **Duration:** How long the test takes
- **Results timing:** How long to get results
- **Normal range:** What normal results look like
- **Abnormal results:** What different abnormal values mean
- **Interpretation:** What results might indicate
- **False positives/negatives:** Test accuracy limitations
- **Risks:** Any risks or side effects
- **Cost:** Typical cost (if available)

---

## Why It Matters

**Understanding tests helps you:**
- Prepare mentally and physically
- Know what to expect during test
- Understand what results mean
- Ask informed questions
- Reduce anxiety about the unknown
- Know what happens next based on results

---

## How to Use

### Python API
```python
from medkit.diagnostics.medical_test_info import get_test_info

test = get_test_info("complete blood count")
print(test)

test = get_test_info("glucose test")
print(test)
```

### Command Line
```bash
python cli/cli_medical_tests.py "complete blood count"
python cli/cli_medical_tests.py "glucose test" --details
```

---

## Tests Covered

**Blood Tests:**
- Complete Blood Count (CBC)
- Basic Metabolic Panel (BMP)
- Comprehensive Metabolic Panel (CMP)
- Glucose test
- Hemoglobin A1C
- Lipid panel (cholesterol)
- Thyroid function (TSH, T3, T4)
- Liver function tests
- Kidney function tests
- Coagulation tests (PT, PTT)
- Troponin (heart damage)
- Creatine kinase (muscle damage)
- Many others

**Imaging Tests:**
- X-ray
- Ultrasound
- CT (Computed Tomography) scan
- MRI (Magnetic Resonance Imaging)
- PET scan
- Nuclear imaging

**Cardiac Tests:**
- EKG (Electrocardiogram)
- Echocardiogram (heart ultrasound)
- Stress test
- Holter monitor
- Coronary angiography

**Pulmonary Tests:**
- Spirometry (lung function)
- Chest X-ray
- CT chest
- Bronchoscopy

**Other Tests:**
- Biopsy (tissue sample)
- Endoscopy (camera into organs)
- Colonoscopy (colon camera)
- Lumbar puncture (spinal tap)
- Bone marrow biopsy

---

## Example: Complete Blood Count (CBC)

You learn:
- **What it measures:** Counts and types of blood cells
- **Why ordered:** Check for infection, anemia, leukemia, other blood disorders
- **Sample:** Few drops of blood from finger prick or blood draw
- **Preparation:** Usually fasting not required
- **Duration:** 5-10 minutes to collect; results in 24 hours
- **Normal ranges:**
  - WBC (white blood cells): 4.5-11.0 K/μL (infection if high)
  - RBC (red blood cells): 4.5-5.9 M/μL (anemia if low)
  - Hemoglobin: 13.5-17.5 g/dL (oxygen carrying if low)
  - Platelets: 150-400 K/μL (clotting if low)
- **Abnormal results might indicate:**
  - High WBC: Infection, leukemia, stress
  - Low RBC/hemoglobin: Anemia, bleeding
  - Low platelets: Bleeding disorder, bone marrow problem
- **False positives:** Stress, recent infection, medications can affect results
- **Risks:** Minimal (small bruise at stick site)
- **Cost:** $50-100 typically (varies by location and insurance)

---

## Important Notes

**Results must be interpreted by doctor.** A single abnormal result doesn't mean diagnosis.

**Context matters.** Your doctor looks at complete clinical picture, not just one test.

**Retesting often needed.** One abnormal result usually requires confirmation.

**Medications affect results.** Tell doctor about all medications before testing.

**Individual variation.** Normal ranges vary slightly between labs and by age/sex.

---

## Before Your Test

✓ Ask what the test measures
✓ Ask why your doctor ordered it
✓ Ask about preparation needed
✓ Ask about discomfort level
✓ Ask how you'll get results
✓ Ask what abnormal results would mean
✓ Ask what happens next
✓ Tell doctor about medications
✓ List allergies or concerns
✓ Arrive early to avoid stress

---

## Understanding Your Results

**When you get results:**
✓ Ask doctor to explain them
✓ Ask if results are normal or abnormal
✓ Ask what abnormal results mean
✓ Ask if retesting is needed
✓ Ask what to do next
✓ Ask if lifestyle changes needed
✓ Ask if treatment needed
✓ Get copies for your records

---

## When Results Are Abnormal

**Normal response:**
1. Doctor explains what abnormal result means
2. Doctor determines if retesting needed
3. If confirmed abnormal, further testing may be ordered
4. Treatment or monitoring plan created

**Don't panic.** One abnormal result doesn't mean diagnosis.

**Ask questions.** What does this mean? What happens next?

**Follow recommendations.** Do retesting or additional testing as recommended.

---

## When to Use This Module

✓ Doctor ordered a test and you want to understand it
✓ Preparing for a test
✓ Want to know what your test results mean
✓ Curious about a test you've heard about
✓ Want to ask doctor informed questions

✗ Don't use to self-diagnose based on test results
✗ Don't assume one abnormal result means disease
✗ Don't panic about results—ask your doctor
✗ Don't ignore abnormal results
✗ Don't delay following doctor's recommendations

---

## Limitations

**Simplified explanations.** Tests are more complex than simplified descriptions.

**Normal ranges vary.** Different labs have slightly different normal ranges.

**Individual variation.** Your normal range may differ based on age, sex, health status.

**Context critical.** Results must be interpreted in context of your situation.

**Your doctor is expert.** Ask your doctor to explain your specific results.

---

## Common Test Questions

**Will the test hurt?** Most blood tests cause minimal discomfort (pinch of needle).

**Do I need to fast?** Depends on test. Ask beforehand.

**How long do results take?** Usually 24 hours to few days; some available immediately.

**Why is my result abnormal?** Many things can cause abnormal results; doctor must determine cause.

**Do I need retesting?** One abnormal result usually requires confirmation before diagnosis.

**When should I worry?** Ask doctor what results require immediate attention.

---

## Disclaimer

**Educational Information:** Helps you understand medical tests.

**Not Diagnosis:** Test results must be interpreted by your doctor.

**Not Medical Advice:** Consult your doctor about your specific test results.

**Your Doctor is Expert:** Trust your doctor's interpretation of your results.

**Individual Variation:** Your results interpretation depends on your specific situation.

**Ask Questions:** Never hesitate to ask your doctor about test results.

**Report Concerns:** Contact doctor immediately if you have concerning results or symptoms.

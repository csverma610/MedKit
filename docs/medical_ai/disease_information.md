# Disease Information Module

## Overview
Provides detailed information about medical diseases and health conditions.

**What it does:** Returns comprehensive information about any disease.
**Why it matters:** Helps users understand what diseases are, recognize symptoms, and know what to expect when seeing a doctor.

---

## Scope
This module covers medical diseases, health conditions, and disorders.

---

## What It Does

When you look up a disease, you get:

- **Definition:** What the disease is and how it works
- **Symptoms:** What the person experiences (what to watch for)
- **Causes:** What triggers or causes the disease
- **Risk Factors:** Who is more likely to get the disease (age, genetics, lifestyle, etc.)
- **Diagnosis:** How doctors diagnose it (tests and procedures)
- **Treatment Options:** Available medical treatments
- **Complications:** Possible serious outcomes if untreated
- **Prevention Strategies:** How to reduce risk
- **Prognosis:** Long-term outlook with and without treatment

---

## Why It Matters

**Understanding diseases helps you:**
- Recognize symptoms early
- Know what to tell your doctor
- Understand test results
- Know what treatments exist
- Make informed health decisions
- Reduce anxiety about unknown conditions

---

## How to Use

### Python API
```python
from medkit.medical.disease_info import get_disease_info

info = get_disease_info("diabetes")
print(info)
```

### Command Line
```bash
python cli/cli_disease_info.py diabetes
python cli/cli_disease_info.py "heart disease" --verbose
```

---

## What's Covered

Common diseases and many others including:
- Diabetes (Type 1, Type 2, gestational)
- Heart disease and hypertension
- Infections (bacterial, viral, fungal)
- Cancer (various types)
- Mental health conditions (depression, anxiety, bipolar)
- Autoimmune disorders
- Respiratory diseases
- Digestive disorders
- Neurological conditions
- Endocrine disorders

---

## Important Notes

**This is educational information only.** Do not use to self-diagnose.

**See a doctor for:**
- Diagnosis of any condition
- Treatment planning
- Medication decisions
- Symptom management
- Questions about your specific situation

**One disease, many presentations:** Symptoms vary between individuals. Your symptoms may not match descriptions exactly.

**Seek immediate help if:** Experiencing severe symptoms, chest pain, difficulty breathing, loss of consciousness, or other emergencies.

---

## Example

### Looking up Diabetes
You learn:
- What diabetes is (blood sugar regulation problem)
- Symptoms to recognize (increased thirst, urination, fatigue)
- Types (Type 1 is autoimmune, Type 2 is lifestyle/genetics related)
- Risk factors (family history, weight, age, ethnicity)
- How doctors diagnose it (fasting glucose, HbA1c test)
- Treatment options (lifestyle changes, oral medications, insulin)
- Complications if untreated (kidney damage, vision loss, heart disease)
- Prevention strategies (diet, exercise, weight management)

This helps you understand the condition before your doctor appointment and ask informed questions.

---

## Limitations

**Cannot diagnose you.** Only doctors can diagnose after examining you.

**General information only.** Your specific situation may be different.

**Not personalized.** This doesn't know your medical history, medications, or genetics.

**Individual variation.** Disease presentations differ between people.

---

## When to Use This Module

✓ Want to understand a disease you've heard about
✓ Doctor mentioned a condition and you want to learn more
✓ Recognizing possible symptoms and want information
✓ Preparing for a doctor appointment
✓ Understanding test results your doctor gave you

✗ Don't use this to diagnose yourself
✗ Don't use this instead of seeing a doctor
✗ Don't use this to make treatment decisions alone
✗ Don't ignore emergency symptoms while reading this

---

## Disclaimer

**Educational Use Only:** This information helps you understand medical conditions.

**Not Medical Advice:** This is not professional medical diagnosis, treatment, or advice.

**See a Doctor:** For any health concern, consult a qualified healthcare provider.

**Your Health Matters:** If you have concerning symptoms, don't delay. See a doctor promptly.

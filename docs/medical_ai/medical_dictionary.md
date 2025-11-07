# Medical Dictionary Module

## Overview
A comprehensive reference for medical terminology and abbreviations explained in plain language.

**What it does:** Translates medical terms and abbreviations into understandable explanations.
**Why it matters:** Medical terminology can be confusing. This helps you understand what doctors are saying.

---

## Scope
This module is a medical terminology reference and abbreviation translator.

---

## What It Does

When you look up a medical term, you get:

- **Definition:** What the term means
- **Pronunciation:** How to say it
- **Context:** How and when the term is used
- **Plain English:** Explanation without jargon
- **Related Terms:** Connected medical terms
- **Examples:** Real-world usage examples
- **Abbreviations:** If the term has abbreviations (e.g., MI, MI stands for...)
- **When You'll See It:** Where you might encounter this term (doctor notes, test results, etc.)

---

## Why It Matters

**Understanding medical terminology helps you:**
- Understand doctor conversations
- Read medical reports and test results
- Ask informed questions
- Reduce confusion and anxiety
- Understand medical records
- Communicate better with healthcare providers

---

## How to Use

### Python API
```python
from medkit.medical.medical_dictionary import get_medical_definition

definition = get_medical_definition("hypertension")
print(definition)

definition = get_medical_definition("MI")
print(definition)
```

### Command Line
```bash
python cli/cli_medical_dictionary.py hypertension
python cli/cli_medical_dictionary.py MI
```

---

## What's Included

**Disease and Condition Names:** Hypertension, myocardial infarction, pneumonia, etc.

**Procedure Names:** Angiography, laparoscopy, catheterization, etc.

**Anatomical Terms:** Anterior, posterior, medial, lateral, etc.

**Drug Classification Terms:** Antibiotic, analgesic, anticoagulant, etc.

**Medical Abbreviations:**
- MI (Myocardial Infarction) = Heart attack
- BP (Blood Pressure)
- HR (Heart Rate)
- CBC (Complete Blood Count)
- EKG (Electrocardiogram)
- CT (Computed Tomography)
- MRI (Magnetic Resonance Imaging)

**Physiological Processes:** Metabolism, filtration, circulation, etc.

**Lab and Test Terms:** Glucose, hemoglobin, cholesterol, antibody, etc.

---

## Examples

### Looking up "Hypertension"
You learn:
- Definition: High blood pressure
- How to say it: High-per-TEN-shun
- Context: When your blood pressure is consistently elevated
- Related terms: Hypotension (low BP), systolic, diastolic
- Why it matters: Can lead to heart disease and stroke

### Looking up "MI"
You learn:
- Full name: Myocardial Infarction
- What it means: Heart attack (heart muscle cells dying from lack of blood)
- When you'll see it: Doctor notes, test results, medical records
- Related terms: Cardiac event, infarction, troponin

---

## Important Notes

**Definitions are standardized,** but doctors may use terms slightly differently.

**Context matters.** The same word can have different meanings in different contexts.

**Ask your doctor.** If a term is confusing, ask your healthcare provider to explain.

**Medical language evolves.** New terms are created; old ones sometimes fall out of use.

---

## When to Use This Module

✓ Doctor used a term you didn't understand
✓ Reading medical records and seeing unfamiliar words
✓ Seeing abbreviations on test results
✓ Want to understand medical conversations better
✓ Preparing for a medical appointment

✗ Don't assume this is medical advice
✗ Don't use this to self-diagnose
✗ Don't replace asking your doctor for clarification
✗ Don't assume definitions apply to your specific situation

---

## Limitations

**Simplified:** Medical language can be very detailed; these are simplified versions.

**General definitions:** Your specific context may require more detailed explanation.

**Not a substitute for asking:** If confused, ask your doctor or healthcare provider.

**Etymology:** These are current definitions; historical uses may differ.

---

## Common Abbreviations Quick Reference

| Abbreviation | Full Name | Meaning |
|---|---|---|
| BP | Blood Pressure | Force of blood against vessel walls |
| HR | Heart Rate | Number of heartbeats per minute |
| RR | Respiratory Rate | Number of breaths per minute |
| CBC | Complete Blood Count | Blood test counting cell types |
| BMP | Basic Metabolic Panel | Blood test for kidney/liver function |
| EKG/ECG | Electrocardiogram | Heart electrical activity recording |
| CT | Computed Tomography | 3D X-ray imaging |
| MRI | Magnetic Resonance Imaging | Magnetic imaging |
| IV | Intravenous | Into a vein |
| IM | Intramuscular | Into a muscle |
| PO | Per Oral | By mouth |
| PRN | As Needed | Take when needed |
| BID | Twice Daily | Two times per day |
| TID | Three Times Daily | Three times per day |
| QID | Four Times Daily | Four times per day |

---

## Disclaimer

**Educational Reference Only:** This helps you understand medical terms.

**Not Complete:** Medical terminology is extensive; this covers common terms.

**Context Varies:** Terms may be used differently in different contexts.

**Ask Your Doctor:** When confused, ask your healthcare provider for clarification.

**Medical Records:** If you receive medical records with unfamiliar terms, ask the provider to explain them.

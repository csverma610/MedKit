# Medical Specialties Module

## Overview
Information about different medical specialties and what doctors in each specialty do.

**What it does:** Explains medical specialties and the conditions each treats.
**Why it matters:** When referred to a specialist, you need to understand what they do and why.

---

## Scope
This module covers medical specialties and subspecialties.

---

## What It Does

When you look up a medical specialty, you get:

- **Name:** The specialty title
- **What they treat:** Conditions and diseases they specialize in
- **Procedures:** Common procedures they perform
- **Training:** Educational background and requirements
- **Credentials:** Certifications and credentials
- **When to see them:** Why a patient would be referred
- **Related specialties:** Related fields and specialties
- **Education required:** Years of training needed

---

## Why It Matters

**Understanding specialties helps you:**
- Understand specialist referrals
- Know what doctors specialize in
- Choose between different specialists
- Prepare for specialist appointments
- Ask appropriate questions
- Understand recommendations

---

## How to Use

### Python API
```python
from medkit.medical.medical_speciality import get_speciality_info

specialty = get_speciality_info("cardiology")
print(specialty)

specialty = get_speciality_info("neurology")
print(specialty)
```

### Command Line
```bash
python cli/cli_medical_speciality.py cardiology
python cli/cli_medical_speciality.py neurology --details
```

---

## Specialties Covered

**Cardiology:** Heart and cardiovascular diseases
- Conditions: Heart attacks, arrhythmias, heart failure, valve disease
- Procedures: Angiography, bypass surgery, pacemaker placement

**Neurology:** Brain, spinal cord, and nervous system
- Conditions: Stroke, seizures, Parkinson's, Alzheimer's, migraines
- Procedures: EEG, spinal tap, muscle biopsy

**Orthopedics:** Bones, joints, muscles, ligaments
- Conditions: Fractures, arthritis, back pain, sports injuries
- Procedures: Joint replacement, arthroscopy, bone repair

**Dermatology:** Skin, hair, nails
- Conditions: Rashes, infections, cancer, acne, psoriasis
- Procedures: Biopsies, removal, laser treatment

**Oncology:** Cancer
- Conditions: All types of cancer
- Procedures: Chemotherapy, radiation, biopsy, immunotherapy

**Psychiatry:** Mental health and psychiatric disorders
- Conditions: Depression, anxiety, bipolar disorder, schizophrenia
- Procedures: Medication management, psychotherapy

**Pediatrics:** Children's health
- Focus: Birth through adolescence
- Training: General pediatrics or pediatric subspecialties

**Gastroenterology:** Digestive system
- Conditions: Acid reflux, ulcers, inflammatory bowel disease, liver disease
- Procedures: Endoscopy, colonoscopy, liver biopsy

**Pulmonology:** Lungs and respiratory system
- Conditions: Asthma, COPD, pneumonia, lung cancer
- Procedures: Spirometry, bronchoscopy, lung biopsy

**Nephrology:** Kidneys and kidney disease
- Conditions: Kidney disease, hypertension, electrolyte disorders
- Procedures: Dialysis, kidney biopsy, transplant evaluation

**Endocrinology:** Hormones and metabolism
- Conditions: Diabetes, thyroid disease, hormone imbalances
- Procedures: Hormone testing, medication adjustment

**Rheumatology:** Autoimmune and joint diseases
- Conditions: Rheumatoid arthritis, lupus, scleroderma
- Procedures: Joint injection, immunosuppressive therapy

**Ophthalmology:** Eyes and vision
- Conditions: Cataracts, glaucoma, diabetic retinopathy, macular degeneration
- Procedures: Cataract surgery, laser therapy, injection

**Otolaryngology (ENT):** Ears, nose, throat
- Conditions: Infections, hearing loss, voice problems, throat cancer
- Procedures: Tube placement, sinus surgery, voice surgery

**Urology:** Urinary and male reproductive systems
- Conditions: Kidney stones, prostate disease, urinary incontinence
- Procedures: Cystoscopy, TURP, prostate biopsy

---

## Example: Understanding Cardiology

You learn:
- **What they treat:** Heart, blood vessels, cardiovascular disease
- **Common conditions:** Heart attack, heart failure, arrhythmias, valve disease
- **Procedures:** EKG, stress test, angiography, bypass surgery
- **When to see:** Chest pain, shortness of breath, high blood pressure, family history of heart disease
- **Subspecialties:** Interventional cardiology (stents, angioplasty), heart failure specialist
- **Training:** 4 years medical school + 3 years internal medicine residency + 3 years cardiology fellowship

---

## Important Notes

**Specialties overlap.** Some conditions can be treated by multiple specialties.

**Subspecialties exist.** Many specialties have further subspecialties (pediatric cardiology, neuro-oncology, etc.).

**Board certification.** Look for doctors with appropriate board certification.

**Insurance matters.** You may need a referral from your primary doctor; check insurance requirements.

**Second opinions.** You can always get a second opinion from another specialist.

---

## When to Use This Module

✓ Doctor referred you to a specialist
✓ Want to understand what a specialist does
✓ Considering seeing a specialist
✓ Need to choose between different specialists
✓ Curious about medical fields

✗ Don't use to replace talking to your doctor
✗ Don't assume a specialist is the only option
✗ Don't ignore referrals from your primary doctor
✗ Don't choose specialists without consulting your doctor

---

## Limitations

**This is overview only.** Specialties are complex; this is simplified.

**Subspecialties not listed.** Many subspecialties exist within each specialty.

**Practices vary.** Different specialists may focus on different aspects.

**Training requirements vary.** Requirements differ between countries and programs.

---

## Disclaimer

**Educational Reference:** This helps you understand medical specialties.

**Consult Your Doctor:** For referrals and specialist recommendations, talk to your doctor.

**Board Certification Matters:** Choose specialists with appropriate board certification.

**Not Medical Advice:** This information doesn't replace professional medical guidance.

**Individual Circumstances:** Your specific situation may require different specialist input.

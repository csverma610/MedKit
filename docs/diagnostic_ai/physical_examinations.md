# Physical Examinations Module

## Overview
Detailed guides for physical examinations performed by doctors.

**What it does:** Explains what doctors check during exams and what they're looking for.
**Why it matters:** Understanding exams reduces anxiety and helps you cooperate with doctors.

---

## Scope
This module covers physical examination techniques and procedures.

---

## What It Does

When you look up a physical examination, you get:

- **Exam name:** What examination is being performed
- **What it checks:** What body systems or structures are examined
- **Why performed:** Medical reasons for the exam
- **What doctor looks for:** Normal and abnormal findings
- **Examination techniques:** How doctor performs the exam
- **Preparation:** What patient must do beforehand
- **Positioning:** How patient is positioned
- **Duration:** How long exam takes
- **Discomfort:** Any discomfort or pain involved
- **Equipment used:** Stethoscope, reflex hammer, etc.
- **Normal findings:** What normal looks/sounds like
- **Abnormal findings:** What might indicate problems
- **Follow-up:** What happens if abnormal findings
- **Frequency:** How often exam should be done

---

## Why It Matters

**Understanding exams helps you:**
- Reduce anxiety about exam procedures
- Know what to expect
- Understand what doctor is doing
- Cooperate better during exam
- Understand abnormal findings
- Ask informed questions

---

## How to Use

### Python API
```python
from medkit.diagnostics.medical_tests_graph import get_exam_guide

exam = get_exam_guide("cardiac examination")
print(exam)

exam = get_exam_guide("neurological examination")
print(exam)
```

### Command Line
```bash
python cli/cli_physical_exams.py "cardiac examination"
python cli/cli_physical_exams.py "neurological examination" --details
```

---

## Examinations Covered

**Cardiac (Heart) Examination:**
- Inspection (appearance, color, chest shape)
- Palpation (feeling heart location and force)
- Percussion (tapping to find heart borders)
- Auscultation (listening to heart sounds)
- Checks for: murmurs, arrhythmias, heart failure signs

**Respiratory (Lung) Examination:**
- Inspection (breathing pattern, chest expansion)
- Palpation (checking for vibration)
- Percussion (detecting fluid or air)
- Auscultation (listening to breathing sounds)
- Checks for: infection, asthma, pneumonia, fluid

**Neurological Examination:**
- Mental status (alertness, orientation, memory)
- Cranial nerves (vision, hearing, facial movement)
- Motor (strength, coordination, balance)
- Sensory (touch, pain, temperature sensation)
- Reflexes (quick response to stimuli)

**Abdominal Examination:**
- Inspection (shape, scars, movement)
- Auscultation (listening for bowel sounds)
- Palpation (feeling organs, checking for pain)
- Percussion (detecting fluid or gas)
- Checks for: organ enlargement, pain, masses

**Musculoskeletal Examination:**
- Inspection (alignment, swelling, deformities)
- Palpation (checking for tenderness, swelling)
- Range of motion (how far joints move)
- Strength testing (muscle strength evaluation)
- Checks for: arthritis, injury, weakness

**Skin Examination:**
- Inspection (color, rashes, moles, lesions)
- Palpation (texture, temperature)
- Checks for: infection, cancer, dermatitis

**Eye Examination:**
- Visual acuity (how well you see)
- Eye movement (tracking, alignment)
- Pupil reaction (response to light)
- Fundoscopy (looking inside eye with scope)
- Checks for: vision problems, cataracts, retinal damage

**Ear, Nose, Throat Examination:**
- Otoscopy (looking in ears with scope)
- Nasal examination (checking nasal passages)
- Throat examination (looking at throat)
- Checks for: infection, polyps, blockage

---

## Example: Cardiac Examination

You learn:
- **What it checks:** Heart size, heart sounds, blood vessel integrity
- **Why performed:** Evaluate for heart disease, murmurs, arrhythmias
- **Preparation:** Remove shirt/bra for access to chest
- **Duration:** 5-10 minutes typically
- **Techniques used:**

1. **Inspection:** Look at chest for visible heart pulsations
2. **Palpation:** Feel where heart beat is strongest (point of maximum impulse)
3. **Percussion:** Tap to find heart borders
4. **Auscultation:** Listen with stethoscope to heart sounds

- **Normal findings:**
  - Regular heart rate 60-100 beats/minute
  - Two clear heart sounds (lub-dub)
  - No extra sounds (murmurs, clicks)
  - No heart enlargement
  - No fluid in pericardium

- **Abnormal findings might indicate:**
  - Heart murmur: Valve problem or defect
  - Irregular heartbeat: Arrhythmia
  - Heart gallop: Heart failure sign
  - Muffled sounds: Fluid around heart
  - Displaced point of impulse: Heart enlargement

---

## Examination Techniques Explained

**Inspection:** Doctor looks at the body part for:
- Color (pale, flushed, cyanotic)
- Shape (normal, swollen, deformed)
- Rashes or visible abnormalities
- Movement (normal breathing, tremor, etc.)

**Palpation:** Doctor feels body part with hands:
- Temperature (hot, cold, normal)
- Texture (smooth, rough, firm)
- Lumps or masses
- Tenderness or pain
- Vibration (fremitus)

**Percussion:** Doctor taps to listen to sounds:
- Resonant (hollow sound - air-filled)
- Dull (solid sound - fluid or organ)
- Tympanic (drum-like sound - gas)

**Auscultation:** Doctor listens with stethoscope:
- Heart sounds
- Lung sounds
- Bowel sounds
- Blood vessel sounds (bruits)

---

## Important Notes

**Exams are safe.** Physical exams carry no risk.

**Communication important.** Tell doctor about pain or discomfort.

**Privacy respected.** Doctor examines only necessary areas.

**Normal variation.** Not all people are anatomically identical.

**Findings require context.** One finding doesn't mean diagnosis.

---

## During Your Physical Exam

✓ Remove clothing as requested (privacy maintained with drape)
✓ Tell doctor about pain or discomfort
✓ Relax (tension can affect findings)
✓ Follow positioning instructions
✓ Breathe normally
✓ Ask what doctor is doing
✓ Ask about findings

---

## When to Use This Module

✓ Doctor is performing an exam and you want to know what it is
✓ Want to understand what doctor checks during exams
✓ Anxious about upcoming physical exam
✓ Want to understand why exam is being done
✓ Doctor found abnormal finding and you want to understand

✗ Don't use to self-diagnose based on exam findings
✗ Don't assume abnormal finding means serious disease
✗ Don't move or tense during exam
✗ Don't ignore abnormal findings doctor reports

---

## Limitations

**Exam findings require context.** One finding must be considered with full clinical picture.

**Variation normal.** Normal findings vary between people.

**Expertise matters.** Doctor's experience affects exam quality.

**Follow-up often needed.** Abnormal findings usually require further testing.

---

## Disclaimer

**Educational Information:** Helps you understand physical exams.

**Not Diagnosis:** Physical exam findings don't diagnose without context.

**Not Medical Advice:** Consult your doctor about your exam findings.

**Doctor is Expert:** Trust your doctor's assessment of exam findings.

**Individual Variation:** Your exam findings depend on your specific situation.

**Ask Your Doctor:** Never hesitate to ask what your doctor found.

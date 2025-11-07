# Diagnostic Tools Documentation

## Overview

The Diagnostic Tools module provides information about medical tests, diagnostic equipment, physical examination techniques, and how doctors decide what tests to order.

**What it does:** Explains medical tests, devices, exams, and diagnostic decision-making.
**Why it matters:** Understanding tests helps patients prepare, reduces anxiety, and lets them have informed conversations with doctors.

---

## Medical Tests Information

### Scope
Comprehensive information about diagnostic medical tests.

### What it does
- Explains what the test measures
- Describes why doctors order it
- Details how the test is performed
- Explains what samples are needed (blood, urine, saliva, etc.)
- Lists normal and abnormal results
- Interprets what abnormal results might mean
- Identifies risks or side effects
- Describes preparation needed beforehand
- Explains how long it takes

### Why it matters
When a doctor orders a test, patients need to understand what is being tested, how it works, what results mean, and what happens next.

### Usage
```python
from medkit.diagnostics.medical_test_info import get_test_info

test = get_test_info("complete blood count")
print(test)
```

### Tests Covered
Blood tests (CBC, metabolic panel, glucose), imaging tests (X-ray, ultrasound, CT, MRI), cardiac tests (EKG, stress test, echocardiogram), pulmonary function tests, hormone tests, liver and kidney function tests, and hundreds more.

### Important Note
Results must be interpreted by a doctor. A single abnormal result doesn't mean diagnosis. Doctors look at the complete clinical picture.

---

## Diagnostic Devices

### Scope
Information about medical equipment and machines used to diagnose health problems.

### What it does
- Explains what the device does
- Describes how it works (what technology it uses)
- Identifies what it diagnoses
- Explains what to expect during use
- Lists any risks or discomfort
- Describes preparation needed
- Explains results and timing
- Details contraindications (who can't use it)

### Why it matters
Modern medical devices can be intimidating. Understanding how they work reduces patient anxiety and improves cooperation during procedures.

### Usage
```python
from medkit.diagnostics.medical_test_devices import get_device_info

device = get_device_info("ultrasound machine")
print(device)
```

### Devices Covered
Heart monitors, ultrasound machines, CT scanners, MRI machines, X-ray equipment, EKG machines, endoscopes, colonoscopes, mammography equipment, and others.

### Key Differences

**Ultrasound:** Uses sound waves, safe, no radiation, real-time images.

**X-ray:** Uses radiation, quick images, flat 2D pictures.

**CT (Computed Tomography):** Multiple X-rays create detailed 3D images, higher radiation exposure.

**MRI:** Uses magnets and radio waves, no radiation, very detailed, takes longer.

---

## Physical Examinations

### Scope
Detailed guides for physical examinations performed by doctors.

### What it does
- Explains what the doctor is checking
- Describes the examination steps
- Explains what normal findings are
- Identifies what abnormal findings might mean
- Lists patient preparation needed
- Describes what to expect during exam
- Explains results

### Why it matters
When a doctor examines you, you deserve to understand what they're doing and why. Understanding the exam reduces anxiety and improves cooperation.

### Usage
```python
from medkit.diagnostics.medical_tests_graph import get_exam_guide

exam = get_exam_guide("cardiac examination")
print(exam)
```

### Examinations Covered
Cardiac (heart) examination, respiratory (lung) examination, neurological examination, abdominal examination, musculoskeletal examination, skin examination, eye examination, ear/nose/throat examination, and 19+ others.

### Common Examination Elements

**Inspection:** Looking at the body part for color, swelling, deformities.

**Palpation:** Feeling with hands for lumps, tenderness, temperature.

**Percussion:** Tapping to listen for sounds (hollow vs. solid).

**Auscultation:** Listening with stethoscope for sounds (heart, lungs, bowel).

---

## Medical Decision Guides

### Scope
Evidence-based guides showing how doctors diagnose conditions.

### What it does
- Shows the diagnostic path from symptoms to diagnosis
- Explains what questions doctors ask
- Identifies what tests doctors order first (initial testing)
- Shows how results guide next steps
- Explains why certain tests are done in certain order
- Identifies differential diagnoses (possible conditions)
- Shows how diagnosis is confirmed

### Why it matters
Diagnosis isn't random. Doctors follow evidence-based patterns. Understanding how doctors think helps patients prepare for appointments and understand the process.

### Usage
```python
from medkit.diagnostics.medical_test_info import get_decision_guide

guide = get_decision_guide("chest pain")
print(guide)
```

### Decision Paths Covered
Chest pain diagnosis, shortness of breath, headache, abdominal pain, fever, dizziness, and others.

### Example: Chest Pain Diagnostic Path
1. **Initial assessment:** History and physical exam
2. **Initial tests:** EKG, troponin blood test (checks for heart attack)
3. **If abnormal:** Admit to hospital, additional testing
4. **If normal but high risk:** Stress test or cardiac catheterization
5. **If normal and low risk:** May discharge with instructions
6. **Result:** Rule out life-threatening conditions first, identify actual cause

---

## Symptom Detection

### Scope
AI-powered analysis of symptoms to identify possible conditions.

### What it does
- Analyzes symptom patterns
- Identifies possible conditions that match symptoms
- Prioritizes conditions by likelihood
- Identifies emergency warning signs
- Recommends urgency level (see doctor today, this week, routine appointment)
- Suggests what to tell your doctor
- Lists questions to ask doctor

### Why it matters
When symptoms start, people often don't know if it's serious. This helps guide urgency and preparation for doctor visits.

### Usage
```bash
python cli/cli_symptoms_checker.py --symptoms "fever,cough,fatigue"
```

### Important Limitations

**Cannot diagnose:** Only a doctor who examines you can diagnose.

**Overlapping symptoms:** Many conditions have similar symptoms.

**Many variables:** Age, medical history, medications all affect diagnosis.

**Use as guide:** This is a starting point for doctor conversations, not a diagnosis.

---

## Test Relationships and Sequencing

### Scope
How medical tests relate to each other and the order doctors use them.

### What it does
- Explains initial screening tests vs. confirmatory tests
- Shows why certain tests are done before others
- Identifies follow-up tests based on results
- Explains efficiency in test ordering
- Discusses cost-benefit of testing
- Identifies when additional testing is unnecessary

### Why it matters
Good doctors don't order random tests. They follow logical sequences. Understanding this reduces unnecessary testing and costs.

### Example: Diabetes Testing Sequence

1. **Initial screening:** Fasting blood glucose or HbA1c
2. **If abnormal:** Repeat testing to confirm (not diagnosed on one test)
3. **If confirmed diabetic:** Kidney and liver function tests (baseline)
4. **Routine monitoring:** HbA1c every 3 months, annual labs
5. **Complications screening:** Kidney function, eye exam, foot exam

### Why This Order?
- **Initial tests:** Quick, inexpensive, identify the problem
- **Confirmation:** Avoids misdiagnosis
- **Baseline tests:** Establish normal before medication starts
- **Monitoring:** Ensures treatment is working, watch for side effects
- **Screening:** Catch complications early

---

## Disclaimer

**Educational Information Only:** This information helps you understand medical tests and procedures.

**Not Diagnosis:** This information does not diagnose you or replace examination by a doctor.

**Individual Variation:** Medical testing varies based on your specific situation, age, medical history, and symptoms.

**Interpretation:** Results must be interpreted by a doctor. Context matters. One abnormal result may not mean disease.

**Trust Your Doctor:** If your doctor recommends a test, ask questions. But follow professional medical advice over online information.

**Seek Care When Needed:** If you have concerning symptoms:
- See your doctor promptly
- Call 911 for emergencies
- Go to the ER for severe symptoms
- Don't wait for online tools to decide

**Privacy:** Medical testing may involve sensitive information. Ask about privacy and how results are stored.

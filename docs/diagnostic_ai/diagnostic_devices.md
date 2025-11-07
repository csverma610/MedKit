# Diagnostic Devices Module

## Overview
Information about medical equipment and machines used to diagnose health problems.

**What it does:** Explains how diagnostic devices work and what to expect during use.
**Why it matters:** Modern medical devices can be intimidating. Understanding them reduces anxiety.

---

## Scope
This module covers medical diagnostic equipment and imaging machines.

---

## What It Does

When you look up a diagnostic device, you get:

- **Device name:** Common and official names
- **What it does:** Purpose and function
- **What it diagnoses:** What conditions it detects
- **How it works:** Technology used (sound waves, radiation, magnets, etc.)
- **Procedure:** Step-by-step what happens during use
- **Preparation:** What patient must do beforehand
- **Duration:** How long procedure takes
- **Discomfort level:** Any discomfort or pain
- **Safety:** Radiation exposure (if applicable), risks
- **Contraindications:** Who can't use it (metal implants, pregnancy, etc.)
- **Results timing:** How long to get results
- **Risks:** Possible complications or side effects
- **Advantages:** Why this device is useful
- **Limitations:** What it can't show
- **Comparison:** How it compares to other devices
- **Cost:** Typical cost (if available)

---

## Why It Matters

**Understanding devices helps you:**
- Reduce anxiety about procedure
- Know what to expect
- Prepare properly
- Understand why device is recommended
- Ask informed questions
- Cooperate better during procedure

---

## How to Use

### Python API
```python
from medkit.diagnostics.medical_test_devices import get_device_info

device = get_device_info("ultrasound machine")
print(device)

device = get_device_info("MRI machine")
print(device)
```

### Command Line
```bash
python cli/cli_diagnostic_devices.py "ultrasound machine"
python cli/cli_diagnostic_devices.py "MRI machine" --details
```

---

## Devices Covered

**Imaging Devices:**
- X-ray machine (radiation-based)
- Ultrasound machine (sound wave-based)
- CT scanner (computed tomography, multiple X-rays)
- MRI machine (magnetic resonance imaging)
- PET scanner (positron emission tomography)

**Cardiac Devices:**
- EKG/ECG machine (electrical activity)
- Echocardiography machine (heart ultrasound)
- Stress test equipment (treadmill/medication)
- Holter monitor (portable heart monitor)
- Cardiac catheterization lab

**Pulmonary Devices:**
- Spirometer (lung function)
- Bronchoscope (lung camera)

**Monitoring Devices:**
- Blood pressure monitor
- Pulse oximeter (oxygen level)
- Glucose monitor
- Cardiac monitor

**Endoscopic Devices:**
- Endoscope (general scope)
- Colonoscope (colon scope)
- Gastroscope (stomach scope)
- Bronchoscope (airway scope)

---

## Example: MRI Machine

You learn:
- **What it does:** Creates detailed magnetic images of body
- **What it diagnoses:** Brain, spine, joints, organs, soft tissue
- **How it works:** Uses magnetic field and radio waves; no radiation
- **Procedure:** Patient lies still in scanner for 30-60 minutes
- **Preparation:** Remove metal objects, jewelry, hearing aids
- **Safety:** Very safe; no radiation exposure
- **Risks:** Very minimal; rare allergic reaction to contrast dye (if used)
- **Discomfort:** Loud noise (earplugs provided), must lie still, confined space
- **Duration:** 30-90 minutes depending on what's being scanned
- **Results:** Usually 24-48 hours for detailed report
- **Contraindications:**
  - Pacemakers (some are compatible now, ask doctor)
  - Metal implants that aren't MRI-safe
  - Pregnancy (especially first trimester, though safe if necessary)
  - Severe claustrophobia
- **Advantages:** No radiation, excellent soft tissue detail, very accurate
- **Limitations:** Takes longer than CT, more expensive, not good for emergency situations
- **Compared to CT:** CT faster but has radiation; MRI slower but no radiation and better soft tissue
- **Cost:** $1,000-3,000 typically (varies by region and insurance)

---

## Device Comparison

**Ultrasound:**
- Uses: Sound waves
- Radiation: No
- Speed: Fast (10-30 minutes)
- Cost: Inexpensive ($100-400)
- Best for: Pregnancy, soft tissue, organs, blood flow
- Worst for: Bone detail, dense tissue

**X-ray:**
- Uses: Radiation (ionizing)
- Radiation: Low dose
- Speed: Very fast (minutes)
- Cost: Inexpensive ($75-300)
- Best for: Bones, chest, initial screening
- Worst for: Soft tissue, repeat imaging

**CT (Computed Tomography):**
- Uses: Multiple X-rays creating 3D images
- Radiation: Higher dose than single X-ray
- Speed: Fast (5-10 minutes)
- Cost: Moderate ($500-2,000)
- Best for: Emergency, complex anatomy, 3D detail
- Worst for: Pregnant patients, repeated scans

**MRI (Magnetic Resonance Imaging):**
- Uses: Magnetic field and radio waves
- Radiation: No ionizing radiation
- Speed: Slow (30-90 minutes)
- Cost: Expensive ($1,000-3,000)
- Best for: Soft tissue, brain, spine, joints, detailed images
- Worst for: Metal implants, emergency situations, claustrophobia

---

## Important Notes

**Preparation is important.** Follow all pre-procedure instructions.

**Metal is critical.** Some devices react strongly to metal.

**Claustrophobia common.** Tell doctor if confined spaces cause anxiety.

**Contrast dyes.** Some procedures use contrast; allergies are important to report.

**Pregnancy considerations.** Tell doctor if pregnant; some procedures avoided.

**Radiation safety.** X-ray and CT use radiation; necessary precautions taken.

---

## Before Your Procedure

✓ Ask what device will be used
✓ Ask why this device is chosen
✓ Ask about preparation needed
✓ Ask about discomfort or risks
✓ Ask how long it takes
✓ Ask if contrast dye will be used
✓ Report metal implants
✓ Report pregnancy
✓ Report claustrophobia
✓ Ask about results timing

---

## During Your Procedure

✓ Follow all instructions
✓ Stay still (important for image quality)
✓ Use call button if needed
✓ Tell technician about discomfort
✓ Ask questions if confused
✓ Don't move suddenly
✓ Breathe normally
✓ Remain as calm as possible

---

## When to Use This Module

✓ Doctor recommended a diagnostic device procedure
✓ Scheduled for imaging or diagnostic test
✓ Want to understand how device works
✓ Anxious about procedure and want to know what happens
✓ Have metal implants and want to know if compatible

✗ Don't use instead of talking to technician
✗ Don't ignore preparation instructions
✗ Don't move during procedure
✗ Don't delay reporting contraindications (metal, pregnancy)
✗ Don't assume device is unnecessar without talking to doctor

---

## Limitations

**Device selection varies.** Different facilities may use different equipment.

**Technology evolving.** Newer devices may have different features.

**Individual responses vary.** You may tolerate procedure differently than others.

**Technician communication important.** Tell technician about concerns during procedure.

---

## Disclaimer

**Educational Information:** Helps you understand diagnostic devices.

**Not Medical Advice:** Consult your doctor about which device is appropriate.

**Technician Expertise:** Follow technician's instructions; they're trained in device use.

**Safety Protocols:** Facilities follow strict safety protocols; trust their guidance.

**Questions Welcome:** Ask technician or doctor any questions about devices.

**Concerns Important:** Report any concerns about metal implants or pregnancy.

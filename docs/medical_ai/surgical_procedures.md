# Surgical Procedures Module

## Overview
Detailed information about surgical operations and procedures.

**What it does:** Explains surgical procedures step-by-step so patients understand what happens.
**Why it matters:** Surgery can be frightening. Understanding what happens reduces anxiety and helps patients prepare.

---

## Scope
This module covers surgical procedures and operations.

---

## What It Does

When you look up a surgical procedure, you get:

- **Name:** Official name of the procedure
- **Why needed:** Medical indications for the surgery
- **Preparation:** What you must do before surgery
- **Before surgery:** Hospital admission, anesthesia, positioning
- **During surgery:** Step-by-step explanation of the procedure
- **Duration:** How long it typically takes
- **Anesthesia:** What type of anesthesia is used
- **Tools and devices:** Equipment the surgeon uses
- **After surgery:** Recovery room and immediate aftermath
- **Recovery:** Hospital stay duration and recovery at home
- **Restrictions:** Activity limitations during healing
- **Risks and complications:** Possible complications
- **Benefits:** Expected outcomes and benefits
- **Success rates:** How often the procedure works

---

## Why It Matters

**Understanding surgery helps you:**
- Reduce anxiety about the unknown
- Prepare mentally and physically
- Ask informed questions
- Follow pre-op and post-op instructions
- Know what to expect during recovery
- Understand risks and benefits

---

## How to Use

### Python API
```python
from medkit.medical.surgery_info import get_surgery_info

surgery = get_surgery_info("coronary artery bypass")
print(surgery)

surgery = get_surgery_info("knee replacement")
print(surgery)
```

### Command Line
```bash
python cli/cli_surgery_info.py "coronary artery bypass"
python cli/cli_surgery_info.py "knee replacement" --details
```

---

## Procedures Covered

**Cardiac Surgeries:** Bypass, valve repair, transplant, pacemaker

**Orthopedic Surgeries:** Joint replacement, arthroscopy, spine fusion, fracture repair

**General Surgeries:** Appendectomy, hernia repair, gallbladder removal, weight loss surgery

**Brain Surgeries:** Tumor removal, aneurysm repair, deep brain stimulation

**Gastrointestinal Surgeries:** Stomach bypass, colectomy, bowel resection

**Vascular Surgeries:** Aneurysm repair, bypass grafting, vein stripping

**Gynecologic Surgeries:** Hysterectomy, cesarean section, fibroid removal

**Urologic Surgeries:** Prostate removal, kidney removal, bladder procedures

**Thoracic Surgeries:** Lung resection, esophageal surgery, chest wall repair

---

## Example: Coronary Artery Bypass (CABG)

You learn:
- **Why needed:** Arteries blocked, restricting blood to heart
- **Preparation:** Blood tests, imaging, medication adjustments, fasting
- **During surgery:** Chest opened, heart stopped, machine takes over circulation, new vessel grafted around blockage
- **Duration:** 3-4 hours typically
- **Anesthesia:** General anesthesia (unconscious)
- **Tools:** Surgical instruments, heart-lung machine, monitoring devices
- **After surgery:** Ventilator for breathing initially, pain management, monitoring
- **Hospital stay:** Usually 5-7 days
- **Recovery at home:** 6-12 weeks until fully recovered
- **Restrictions:** No driving for weeks, no heavy lifting, gradual activity increase
- **Risks:** Infection, bleeding, stroke, death (small percentage)
- **Benefits:** Better heart blood flow, reduced chest pain, longer life

---

## Important Notes

**Every person is different.** Recovery varies between individuals.

**Follow doctor's instructions.** Pre-op and post-op instructions are critical for safety.

**Ask questions.** Don't hesitate to ask your surgeon anything.

**Complications can occur.** Even successful surgeries can have complications; know warning signs.

**Recovery takes time.** Don't rush; allow proper healing.

**Support system matters.** Having help during recovery is important.

---

## Before Surgery Checklist

✓ Understand why the surgery is needed
✓ Know the procedure steps
✓ Understand risks and benefits
✓ Get pre-op instructions from surgeon
✓ Arrange transportation home
✓ Arrange help for recovery period
✓ Follow fasting instructions
✓ Take/avoid medications as instructed
✓ Discuss anesthesia concerns with anesthesiologist
✓ Ask about pain management plans

---

## When to Use This Module

✓ Doctor recommended surgery and you want to understand it
✓ Have surgery scheduled and want to prepare
✓ Want to know what recovery involves
✓ Need to ask surgeon informed questions
✓ Understanding surgical options

✗ Don't use to decide whether to have surgery
✗ Don't ignore surgeon's instructions
✗ Don't delay recovery by overexerting
✗ Don't hesitate to contact doctor with post-op concerns

---

## Limitations

**Surgical techniques vary.** Different surgeons may use slightly different techniques.

**Individual variation.** Recovery times and outcomes vary by person.

**Simplified explanation.** Actual surgery is more complex than simplified descriptions.

**Your surgeon's specific approach.** Ask your surgeon about their specific technique.

---

## Warning Signs During Recovery

Seek immediate help if you experience:
- Severe pain not controlled by medication
- Fever over 101°F
- Redness, swelling, warmth, or pus at incision
- Chest pain or difficulty breathing
- Severe bleeding or excessive drainage
- Sudden weakness or numbness
- Inability to urinate or have bowel movement
- Signs of infection

---

## Disclaimer

**Educational Information:** This helps you understand surgical procedures.

**Not Medical Advice:** Consult your surgeon for your specific situation.

**Individual Variation:** Your surgery may differ from standard descriptions.

**Follow Your Surgeon's Instructions:** Medical advice from your surgeon takes priority.

**Complications Possible:** Even with good care, complications can occur; report concerns promptly.

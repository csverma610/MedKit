# Medical Implants Module

## Overview
Information about medical devices and implants placed in the body.

**What it does:** Explains what implants are, how they work, and how to live with them.
**Why it matters:** If a doctor recommends an implant, you need to understand what it is and how it affects your life.

---

## Scope
This module covers medical implants and devices placed in or on the body.

---

## What It Does

When you look up a medical implant, you get:

- **What it is:** Description of the device
- **Why needed:** Medical indications for implantation
- **How it works:** Mechanism and function
- **Implantation procedure:** How it's surgically placed
- **Lifespan:** How long it lasts before replacement
- **Size and materials:** What it's made of
- **Positioning:** Where in the body it's placed
- **Benefits:** Expected improvements
- **Restrictions:** Lifestyle changes or limitations
- **Monitoring:** How often you need check-ups
- **Complications:** Possible problems
- **Maintenance:** Care and upkeep needed
- **Removal:** Whether it can be removed
- **Living with it:** Practical daily life information

---

## Why It Matters

**Understanding implants helps you:**
- Know what will happen during implantation
- Understand how the device works
- Prepare for lifestyle adjustments
- Know what to expect during recovery
- Reduce anxiety about the procedure
- Follow proper maintenance and monitoring

---

## How to Use

### Python API
```python
from medkit.medical.medical_implant import get_implant_info

implant = get_implant_info("pacemaker")
print(implant)

implant = get_implant_info("hip replacement")
print(implant)
```

### Command Line
```bash
python cli/cli_medical_implant.py pacemaker
python cli/cli_medical_implant.py "hip replacement" --details
```

---

## Implants Covered

**Cardiac Implants:**
- Pacemakers (regulate heart rhythm)
- Implantable defibrillators (ICD - prevent sudden death)
- Left ventricular assist devices (LVAD - pump blood)
- Artificial heart (bridge to transplant)

**Orthopedic Implants:**
- Artificial hip replacement
- Artificial knee replacement
- Artificial shoulder replacement
- Artificial ankle replacement
- Spinal fusion hardware
- Bone pins and plates

**Hearing Implants:**
- Cochlear implants (restore hearing)
- Bone-conducting implants

**Eye Implants:**
- Intraocular lens (cataract surgery)
- Artificial lens implants
- Retinal implants (restoring vision)

**Neurostimulators:**
- Deep brain stimulation (Parkinson's, tremor, dystonia)
- Spinal cord stimulation (chronic pain)

**Vascular Implants:**
- Stents (keep vessels open)
- Arteriovenous fistulas
- Vascular grafts

**Dental Implants:**
- Artificial tooth roots

---

## Example: Pacemaker

You learn:
- **What it is:** Battery-powered device that sends electrical signals to heart
- **Why needed:** Slow or irregular heartbeat (bradycardia, heart block)
- **How it works:** Monitors heart rhythm; sends electrical signals when needed
- **Implantation:** Minor surgery, local anesthesia, device placed under collarbone skin
- **Size:** Small, about matchbox-sized, weighs about 20-50 grams
- **Materials:** Metal and plastic case, wires (leads) go to heart
- **Lifespan:** 7-12 years before battery replacement
- **Benefits:** Normal heart rhythm, improved energy, reduced symptoms
- **Restrictions:** No strong magnetic fields, some sports avoided, no contact sports
- **Monitoring:** Check-ups every 3-6 months, device checked electronically
- **Complications:** Infection, lead displacement, device malfunction
- **Maintenance:** Keep up with appointments, report symptoms
- **Removal:** Can be replaced when battery dies; rarely removed otherwise
- **Daily life:** Can do most activities, avoid activities that could impact device

---

## Important Notes

**Implants improve quality of life.** They allow people to do things they couldn't before.

**Monitoring is essential.** Regular check-ups keep implants functioning properly.

**Activity restrictions vary.** Your doctor will advise specific restrictions.

**Medication interactions.** Tell all doctors about your implant (affects future imaging and procedures).

**Long-term follow-up.** Most implants require lifelong monitoring and eventual replacement.

**Insurance coverage.** Check insurance before implantation; most cover recommended implants.

---

## Before Implantation

✓ Understand why the implant is needed
✓ Know what the procedure involves
✓ Understand restrictions and limitations
✓ Ask about lifespan and replacement
✓ Understand monitoring requirements
✓ Arrange transportation and help
✓ Follow pre-op instructions
✓ Discuss concerns with your doctor

---

## After Implantation

✓ Keep follow-up appointments
✓ Report any problems immediately
✓ Know warning signs (unusual symptoms, pain, swelling)
✓ Keep device information card (for imaging and TSA)
✓ Inform all future healthcare providers
✓ Avoid strong magnetic fields and certain procedures
✓ Follow activity restrictions initially
✓ Allow proper healing time

---

## When to Use This Module

✓ Doctor recommended an implant
✓ Scheduled for implantation procedure
✓ Want to understand daily life with an implant
✓ Need to explain implant to family
✓ Have questions about implant care

✗ Don't use to decide whether to get an implant
✗ Don't ignore monitoring appointments
✗ Don't exceed activity restrictions without approval
✗ Don't hesitate to ask doctor questions

---

## Limitations

**Your specific implant may differ.** Devices vary by manufacturer and type.

**Technology evolving.** Newer implants may have different features.

**Individual outcomes vary.** Results differ from person to person.

**Your doctor's guidance takes priority.** Ask your doctor about your specific implant.

---

## Warning Signs Requiring Immediate Care

Seek help if you experience:
- Swelling, redness, warmth at implant site
- Fever over 101°F
- Chest pain or difficulty breathing
- Fainting or severe dizziness
- Persistent hiccups (pacemaker)
- Inability to detect device (if externally palpable)
- Device beeping or alarming
- Any symptoms suggesting device malfunction

---

## Disclaimer

**Educational Information:** Helps you understand medical implants.

**Not Medical Advice:** Consult your doctor for your specific implant.

**Individual Variation:** Your implant may differ from standard descriptions.

**Follow Medical Guidance:** Your doctor's advice takes priority over general information.

**Lifelong Care Required:** Most implants need ongoing monitoring and eventual replacement.

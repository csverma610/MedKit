# Medicine Information Module

## Overview
Detailed information about specific medications and drugs.

**What it does:** Provides comprehensive medication details including usage, side effects, and safety information.
**Why it matters:** Patients need to understand medications to use them safely and effectively.

---

## Scope
This module covers detailed information about medications, drugs, and pharmaceuticals.

---

## What It Does

When you look up a medication, you get:

- **Drug names:** Generic and brand names
- **Drug classification:** Type of drug and category
- **What it treats:** Medical indications and uses
- **Dosage:** Recommended dose and frequency
- **How to take it:** With/without food, timing, instructions
- **Side effects:** Common and serious side effects
- **Serious side effects:** Rare but dangerous reactions
- **Contraindications:** Who shouldn't take it
- **Drug interactions:** Medications it interacts with
- **Food interactions:** Foods that affect the drug
- **Alcohol interactions:** Effects of mixing with alcohol
- **Pregnancy/breastfeeding:** Safety during pregnancy and nursing
- **How it works:** Mechanism of action in the body
- **Duration:** How long it stays in your system
- **Warnings and precautions:** Special considerations
- **Overdose information:** What happens if too much is taken
- **Storage:** How to properly store the medication

---

## Why It Matters

**Understanding medications helps you:**
- Take medication correctly
- Recognize side effects
- Avoid dangerous interactions
- Know when to contact your doctor
- Use medication safely
- Get maximum benefit from treatment

---

## How to Use

### Python API
```python
from medkit.drug.medicine_info import get_medicine_info

info = get_medicine_info("aspirin")
print(info)

info = get_medicine_info("ibuprofen")
print(info)
```

### Command Line
```bash
python cli/cli_medicine_info.py aspirin
python cli/cli_medicine_info.py ibuprofen --interactions
```

---

## Medications Covered

**Over-the-Counter Pain Relievers:**
- Aspirin
- Ibuprofen
- Naproxen
- Acetaminophen

**Antibiotics:**
- Amoxicillin
- Azithromycin
- Ciprofloxacin
- Many others

**Blood Pressure Medications:**
- ACE inhibitors
- Beta-blockers
- Calcium channel blockers
- Diuretics

**Diabetes Medications:**
- Metformin
- Insulin
- Sulfonylureas
- GLP-1 agonists

**Mental Health Medications:**
- SSRIs (antidepressants)
- Anti-anxiety medications
- Antipsychotics
- Mood stabilizers

**Heart Medications:**
- Statins (cholesterol)
- Blood thinners
- Heart failure drugs
- Rhythm medications

---

## Example: Ibuprofen

You learn:
- **Brand names:** Advil, Motrin, and others
- **Drug class:** NSAID (nonsteroidal anti-inflammatory drug)
- **What it treats:** Pain, fever, inflammation
- **Dosage:** 200-400 mg every 4-6 hours, max 1200 mg/day OTC
- **How to take:** With food or milk to reduce stomach upset
- **Common side effects:** Stomach upset, heartburn, nausea
- **Serious side effects:** Bleeding, ulcers, kidney damage, allergic reaction
- **Don't take if:** Allergic to NSAIDs, severe kidney/liver disease, pregnancy (especially 3rd trimester)
- **Interacts with:** Blood thinners (increases bleeding), some blood pressure drugs
- **With alcohol:** Increases stomach bleeding risk
- **Pregnancy:** Avoid especially in third trimester
- **How it works:** Reduces prostaglandins (causes inflammation)
- **Duration:** 4-6 hours per dose
- **Storage:** Room temperature, dry place

---

## Important Notes

**Medications are powerful.** Take exactly as prescribed.

**Side effects vary.** You may experience different side effects than others.

**Timing matters.** Take at correct times for best effect.

**Food/drug interactions.** Some medications require empty stomach; others need food.

**Don't stop suddenly.** Some medications cause problems if stopped abruptly (consult doctor).

**Report problems.** Tell your doctor about concerning side effects.

---

## Before Taking Any Medication

✓ Understand what it treats
✓ Know the correct dose and frequency
✓ Learn how to take it (food, timing, etc.)
✓ Know common side effects
✓ Know serious side effects requiring doctor contact
✓ Tell doctor about all other medications
✓ Ask about interactions
✓ Ask about alcohol interactions
✓ If pregnant/breastfeeding, ask about safety
✓ Ask about food interactions

---

## Common Medication Questions

**How long before it works?**
Varies by drug: some work immediately, some take weeks.

**Can I stop when I feel better?**
No. Some conditions require ongoing treatment. Ask your doctor.

**Can I skip doses?**
No. Consistent dosing is usually important. If missed, follow instructions.

**Can I double up if I missed a dose?**
Usually no. Never double doses without asking.

**Can I mix with alcohol?**
Some medications are safe with alcohol; many aren't. Always ask.

**Can I take with food?**
Depends on the medication. Check instructions.

**How should I store it?**
Usually room temperature, avoid moisture/heat. Check label.

---

## When to Contact Your Doctor

Contact immediately if:
- Severe allergic reaction (difficulty breathing, swelling)
- Severe side effects
- New or worsening symptoms
- Signs of medication not working

Contact within 24 hours if:
- Moderate side effects
- Concerns about the medication
- Accidental overdose

---

## Overdose Emergency

If you think you overdosed:
- **Call Poison Control:** 1-800-222-1222 (US, 24/7)
- **Call 911:** For severe symptoms
- **Go to ER:** If told to by Poison Control

Have the medication bottle with you.

---

## When to Use This Module

✓ Want to understand a medication you're taking
✓ Considering taking a medication
✓ Want to check for interactions
✓ Need to understand side effects
✓ Preparing to talk to your doctor about medications

✗ Don't use to decide whether to take medication
✗ Don't stop medications without doctor approval
✗ Don't change doses on your own
✗ Don't ignore serious side effects
✗ Don't use instead of consulting your pharmacist

---

## Limitations

**Not complete:** Medications have extensive information; this covers key points.

**Your situation matters:** Your specific health conditions may require different guidance.

**Pharmaceutical companies update information.** Check current prescribing information if concerned.

**Individual responses vary.** You may respond differently than described.

---

## Disclaimer

**Educational Information:** Helps you understand medications.

**Not Medical Advice:** Consult your doctor or pharmacist for medical decisions.

**Your Pharmacist is Expert:** Ask your pharmacist—they specialize in medication information.

**Always Follow Doctor's Instructions:** Your doctor's guidance takes priority.

**Questions Encouraged:** Never hesitate to ask about medications.

**Report Problems Promptly:** Tell your doctor about concerning symptoms.

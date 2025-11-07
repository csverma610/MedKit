# Herbal Medicine Module

## Overview
Evidence-based information about herbal remedies and plant-based treatments.

**What it does:** Reviews what herbs do, scientific evidence, safety concerns, and how to use them safely.
**Why it matters:** Herbal remedies can be effective but also carry risks. Users need evidence-based information to use them safely.

---

## Scope
This module covers herbal medicines, traditional remedies, and plant-based treatments.

---

## What It Does

When you look up an herb, you get:

- **Common names:** What the herb is called
- **Scientific name:** Latin botanical name
- **Traditional uses:** What it was historically used for
- **Active compounds:** What chemicals in the herb are active
- **Scientific evidence:** What research shows about effectiveness
- **Dosage:** How much to take and how often
- **Preparation:** How to prepare it (tea, capsule, tincture, etc.)
- **Side effects:** Possible adverse effects
- **Drug interactions:** Medications it may interact with
- **Safety warnings:** Who shouldn't use it
- **Pregnancy/breastfeeding:** Safety during pregnancy and nursing
- **Quality concerns:** Purity and consistency issues
- **Cost:** Typical pricing
- **Availability:** Where to find it

---

## Why It Matters

**Understanding herbs helps you:**
- Use herbs safely and effectively
- Avoid dangerous interactions
- Determine if evidence supports use
- Know when to stop using and see doctor
- Make informed decisions
- Avoid wasting money on ineffective products

---

## How to Use

### Python API
```python
from medkit.medical.herbal_info import get_herbal_information

herb = get_herbal_information("turmeric")
print(herb)

herb = get_herbal_information("ginger")
print(herb)
```

### Command Line
```bash
python cli/cli_herbal_info.py turmeric
python cli/cli_herbal_info.py ginger --safety
```

---

## Herbs Covered

**Anti-inflammatory Herbs:**
- Turmeric (curcumin)
- Ginger
- Boswellia

**Immune Support:**
- Echinacea
- Elderberry
- Garlic

**Sleep and Relaxation:**
- Valerian root
- Passionflower
- Chamomile

**Digestive Health:**
- Peppermint
- Ginger
- Fennel

**Respiratory Support:**
- Licorice root
- Thyme
- Eucalyptus

**Brain Health:**
- Ginkgo biloba
- Ginseng
- Bacopa

**Cardiovascular Support:**
- Hawthorn
- Garlic
- Omega-3 supplements

**Mood Support:**
- St. John's Wort
- Valerian
- Passionflower

---

## Example: Turmeric

You learn:
- **Common names:** Turmeric, curcumin, Indian saffron
- **Scientific name:** Curcuma longa
- **Traditional uses:** Anti-inflammatory, digestive aid, joint health
- **Active compound:** Curcumin (yellow pigment)
- **Scientific evidence:** Good evidence for anti-inflammatory, some for joint pain
- **Dosage:** 400-600 mg curcumin 3 times daily with meals
- **Preparation:** Powder in capsules, added to food, golden milk drink
- **Side effects:** Generally safe; high doses may cause digestive upset
- **Drug interactions:** May increase bleeding (with blood thinners); may lower blood sugar
- **Safety warnings:** Avoid if allergic; use cautiously with blood thinners
- **Pregnancy:** Generally considered safe in food amounts; consult doctor for supplements
- **Effectiveness:** Good evidence for joint inflammation; less evidence for other uses
- **Cost:** Inexpensive; turmeric powder is cheap
- **Quality:** Purity varies; look for standardized curcumin content

---

## Important Notes

**Herbal ≠ Safe.** Natural doesn't mean safe. Many herbs are powerful and can be harmful.

**Variable quality.** Herbal products have inconsistent potency and purity.

**Interactions are real.** Herbs can interact with medications dangerously.

**Evidence varies.** Some herbs have good research; many don't.

**Individual responses differ.** What works for one person may not work for another.

**Tell your doctor.** List all herbs and supplements with your doctor.

---

## Critical Safety Information

### Herbs That Interact With Blood Thinners
- Garlic
- Ginger
- Ginkgo biloba
- Feverfew
- Vitamin E supplements
- These increase bleeding risk

### Herbs That Affect Blood Sugar
- Ginseng
- Bitter melon
- Fenugreek
- These may lower blood sugar

### Herbs That Affect Blood Pressure
- Licorice
- Ginseng
- These may raise blood pressure

### Herbs That Interact With Medications
- St. John's Wort: Reduces effectiveness of many drugs
- Echinacea: May affect immune medications
- Valerian: Increases sedation with other sedatives

---

## Before Using Herbs

✓ Consult your doctor or pharmacist
✓ Tell them all medications you take
✓ Ask about interactions
✓ Check if you're pregnant/breastfeeding
✓ Start with low dose to test tolerance
✓ Monitor for side effects
✓ Keep doctor updated on use
✓ Buy from reputable sources
✓ Check for standardized content
✓ Know what the evidence shows

---

## Warning Signs to Stop Using and See Doctor

Stop immediately if you experience:
- Unusual bleeding or bruising
- Severe allergic reaction
- Unexpected symptoms
- Worsening of existing condition
- Drug interactions
- Pregnancy-related concerns
- Any serious symptoms

---

## When to Use This Module

✓ Interested in herbal remedies
✓ Want to know safety and evidence
✓ Planning to take an herb
✓ Want to check for interactions
✓ Doctor asked about supplements you take

✗ Don't use herbs instead of seeing doctor
✗ Don't assume natural = safe
✗ Don't ignore interactions
✗ Don't use during pregnancy without doctor approval
✗ Don't stop medications to use herbs

---

## Limitations

**Limited research:** Many herbs lack scientific studies.

**Quality varies widely:** Supplement industry has loose regulations.

**Individual variation:** Response to herbs varies greatly.

**Efficacy not proven:** Many herbs lack strong evidence of effectiveness.

**Safety concerns:** Long-term safety unknown for many herbs.

---

## Disclaimer

**Educational Information:** Helps you understand herbal medicine safety and evidence.

**Not Medical Advice:** Consult your doctor before using herbs.

**Individual Caution:** Your specific situation may require different recommendations.

**Tell Your Doctor:** Always inform healthcare providers about herbs and supplements.

**Natural ≠ Safe:** Herbal remedies can be powerful and cause harm.

**Quality Concerns:** Supplements lack FDA quality control; purity and potency vary.

**Pregnant/Breastfeeding:** Consult your doctor before using any herbs.

**Interactions Serious:** Herbal-drug interactions can be dangerous.

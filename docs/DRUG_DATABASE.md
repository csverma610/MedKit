# Drug Database Documentation

## Overview

The Drug Database module provides comprehensive information about medications, drug interactions, and pharmaceutical safety. It helps users understand what medications do, how to use them safely, and what happens when drugs interact.

**What it does:** Delivers medication information and interaction data.
**Why it matters:** Patients need to understand their medications to use them safely and avoid harmful interactions.

---

## Medicine Information

### Scope
Provides detailed information about specific medications and drugs.

### What it does
- Lists the drug name (generic and brand names)
- Explains what the drug treats (indications)
- Specifies dosage and frequency
- Describes how to take it (with food, with water, etc.)
- Lists common side effects
- Identifies serious side effects
- Explains who should NOT take it (contraindications)
- Details drug interactions (see Drug-Drug Interactions below)
- Describes how long it stays in the body
- Explains how the drug works in the body
- Lists warnings and precautions

### Why it matters
When prescribed a medication, patients need to know what it does, how to take it, what to watch for, and when to contact their doctor.

### Usage
```python
from medkit.drug.medicine_info import get_medicine_info

info = get_medicine_info("aspirin")
print(info)
```

### Drugs Covered
Over-the-counter medications, prescription drugs, supplements, and common medications across all categories.

### Important Note
Always take medication exactly as prescribed. Do not change doses or stop taking medications without talking to your doctor.

---

## Drug-Drug Interactions

### Scope
Information about what happens when two or more medications are taken together.

### What it does
- Identifies if two drugs interact
- Explains the type of interaction
- Rates the severity level (mild, moderate, severe)
- Describes what the interaction does
- Recommends whether drugs can be taken together
- Suggests timing adjustments if needed
- Identifies monitoring requirements

### Why it matters
Some drug combinations are dangerous. Even common medications can cause harmful interactions. Patients need to know before taking multiple drugs.

### Severity Levels Explained

**Mild:** Little to no risk, but you should be aware
- May slightly reduce effectiveness of one drug
- May slightly increase side effects
- Usually safe to take together

**Moderate:** Real interaction that needs management
- Can reduce how well one or both drugs work
- Can increase side effects noticeably
- May need dose adjustment
- May need careful timing between doses
- May need monitoring by doctor

**Severe:** Serious risk, avoid combination if possible
- Can cause dangerous side effects
- Can significantly reduce drug effectiveness
- Could harm organs (liver, kidneys, heart)
- Should not be taken together without doctor approval
- May require emergency medical attention if taken together

### Usage
```python
from medkit.drug.drug_drug_interaction import get_drug_interaction

interaction = get_drug_interaction("warfarin", "aspirin")
print(interaction)
```

### Common Serious Interactions

**Warfarin (blood thinner) + Aspirin:** Increases bleeding risk significantly. Needs careful monitoring.

**Metformin + Contrast dye (for imaging):** Can damage kidneys. Dye procedures need special planning.

**SSRIs (antidepressants) + NSAIDs:** Increases stomach bleeding risk.

**Alcohol + Sedatives:** Severely increases drowsiness and impairs judgment.

**Alcohol + Pain relievers:** Can cause serious liver damage.

### Important Note
List all medications, supplements, and herbal products with your doctor and pharmacist. They will check for interactions.

---

## Drug-Disease Interactions

### Scope
Information about whether a medication is safe for someone with a specific medical condition.

### What it does
- Identifies if a drug is safe with a specific condition
- Explains why the drug might be unsafe
- Recommends alternatives if the drug is contraindicated
- Identifies conditions requiring dose adjustments
- Lists monitoring requirements
- Explains potential complications

### Why it matters
Some medications can make certain health conditions worse. A medication safe for one person may be dangerous for another due to their medical history.

### Common Examples

**Ibuprofen + Kidney disease:** NSAIDs can damage kidneys and should be avoided.

**ACE inhibitors + High potassium:** These drugs raise potassium levels, which is dangerous if potassium is already high.

**Statins + Liver disease:** These drugs are processed by the liver and can be harmful if the liver is damaged.

**Steroids + Diabetes:** Steroids raise blood sugar, making diabetes harder to control.

**Bronchodilators + Heart arrhythmias:** Can worsen heart rhythm problems.

### Usage
```python
from medkit.drug.drug_disease_interaction import get_drug_disease_interaction

result = get_drug_disease_interaction("ibuprofen", "kidney disease")
print(result)
```

### Important Note
Tell your doctor about ALL your health conditions. Some conditions require special medication precautions.

---

## Drug-Food Interactions

### Scope
Information about how food and drinks affect medications.

### What it does
- Identifies which foods/drinks interact with a drug
- Explains the type of interaction
- Describes what the interaction does
- Recommends timing adjustments
- Lists foods to avoid
- Identifies safe alternatives

### Why it matters
Food can change how well medications work or increase side effects. Some interactions are serious.

### Common Examples

**Grapefruit juice + Statins:** Increases drug levels, causing side effects like muscle pain and liver damage.

**Leafy greens + Warfarin:** Vitamin K reduces blood thinner effectiveness. Eat consistent amounts of greens.

**Dairy + Antibiotics:** Calcium interferes with absorption. Take on empty stomach, 2 hours before dairy.

**Alcohol + Metronidazole:** Causes severe nausea, vomiting, and flushing.

**Tyramine-rich foods + MAOIs:** Can cause dangerous blood pressure spikes. (Aged cheese, cured meats, fermented foods)

### Usage
```python
from medkit.drug.drug_food_interaction import get_drug_food_interaction

result = get_drug_food_interaction("warfarin", "vitamin K")
print(result)
```

### Important Note
Ask your pharmacist about food interactions when getting a new prescription.

---

## Similar Drugs and Alternatives

### Scope
Information about alternative medications in the same drug class.

### What it does
- Lists medications that work similarly
- Explains differences between drugs
- Identifies which might work better
- Suggests cost alternatives
- Compares side effect profiles
- Helps find alternatives if current drug doesn't work

### Why it matters
If a medication doesn't work, causes bad side effects, or is too expensive, alternatives may be available. This helps users discuss options with doctors.

### Usage
```python
from medkit.drug.similar_drugs import get_similar_drugs

alternatives = get_similar_drugs("aspirin")
print(alternatives)
```

### Example Alternatives

**Instead of Aspirin:** Ibuprofen, naproxen, acetaminophen (different classes, different side effects)

**Instead of One Blood Pressure Drug:** Different classes available: ACE inhibitors, beta-blockers, calcium channel blockers, diuretics

**Instead of One Antibiotic:** Other antibiotics in same or different class may work if bacterial resistance develops

---

## Drug Comparison

### Scope
Side-by-side comparison of multiple medications.

### What it does
- Lists effectiveness at treating the condition
- Compares side effect profiles
- Shows cost differences
- Compares dosing frequency (once daily vs. three times daily)
- Identifies drug interactions for each
- Compares time to work
- Lists contraindications for each

### Why it matters
When choosing between medication options, patients need to understand the tradeoffs between effectiveness, side effects, cost, and convenience.

### Usage
```python
from medkit.drug.drugs_comparison import compare_drugs

comparison = compare_drugs(["aspirin", "ibuprofen", "acetaminophen"])
print(comparison)
```

### What to Compare When Choosing Medications

1. **Effectiveness:** Does it work as well for my specific problem?
2. **Side effects:** Which side effects matter most to me?
3. **Convenience:** Can I take it as prescribed (once daily vs. three times daily)?
4. **Cost:** Can I afford it? Are generic versions available?
5. **Interactions:** Will it interact with my other medications or conditions?
6. **Duration:** How long does it take to work?

---

## Disclaimer

**Informational Only:** This information is educational and does not replace professional medical advice.

**Not Diagnosis or Treatment:** Use this to understand medications, not to diagnose or treat yourself.

**Talk to Your Pharmacist or Doctor:** Before starting any medication, changing doses, or stopping medication:
- Ask your pharmacist or doctor
- Discuss all medications you take
- Ask about side effects to watch for
- Ask about interactions

**Emergency:** If you think you have taken too much medication or are having a severe reaction:
- Call Poison Control: 1-800-222-1222 (US)
- Call 911 for emergency services
- Go to the nearest emergency room

**Never Self-Prescribe:** Do not start, stop, or change medications without talking to your doctor.

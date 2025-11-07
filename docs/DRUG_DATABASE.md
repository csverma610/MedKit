# Drug Database Documentation

The Drug Database module helps you understand medicines and medications. It provides information about how drugs work, their side effects, dosages, and most importantly, how different drugs can interact with each other or with food.

## Medicine Information

Learn detailed information about any medication or drug. When you search for a medicine, you get comprehensive information about what it does, how to take it, what side effects to watch for, and who should not take it.

For example, if your doctor prescribes aspirin, you can look it up to understand what aspirin does, how much to take, what side effects might happen, and what other medicines or conditions might affect whether it's safe for you to take.

**How to Use:**

```python
from medkit.drug.medicine_info import get_medicine_info

# Look up a medication
info = get_medicine_info("aspirin")
print(info)
```

**From Command Line:**

```bash
python cli/cli_medicine_info.py aspirin
python cli/cli_medicine_info.py ibuprofen --interactions
```

**What Information You Get:**

When you look up a medicine, you learn the generic name and brand names, what type of medicine it is, what it's used to treat, how much to take and how often, what side effects can happen, who should not take it, any special warnings, how it works in your body, and how long it stays in your system.

---

## Drug-Drug Interactions

Understand what happens when you take two or more medicines together. Some medicines interact with each other in ways that can be dangerous or reduce how well they work.

For example, some blood thinner medications become dangerous when taken with aspirin because the combination increases bleeding risk too much. This module helps you know if medicines you take together are safe.

**How to Use:**

```python
from medkit.drug.drug_drug_interaction import get_drug_interaction

# Check if two drugs interact
interaction = get_drug_interaction("warfarin", "aspirin")
print(interaction)
```

**From Command Line:**

```bash
python cli/cli_drug_interaction.py warfarin aspirin
python cli/cli_drug_interaction.py metformin alcohol --severity
```

**Understanding Severity:**

When you check a drug interaction, you get a severity rating. Mild interactions mean there's little to no risk, but you should still be aware. Moderate interactions mean the interaction is real but can usually be managed with dose adjustments or careful monitoring. Severe interactions mean you should not take these drugs together without talking to your doctor first.

**Common Examples:**

Blood thinners like warfarin should not be taken with aspirin because it increases bleeding too much. Some heart medications interact with each other in dangerous ways. Some antibiotics reduce the effectiveness of birth control. Alcohol can interact dangerously with many pain relievers and sedatives.

---

## Drug-Disease Interactions

Understand whether a medicine is safe for someone with a specific medical condition. Some medicines can be harmful if you have certain diseases.

For example, if you have kidney disease, some medicines can make it worse. If you have heart disease, certain other medicines might not be safe. This module helps you understand how medicines work with your health conditions.

**How to Use:**

```python
from medkit.drug.drug_disease_interaction import get_drug_disease_interaction

# Check if medicine is safe with a condition
result = get_drug_disease_interaction("ibuprofen", "kidney disease")
print(result)
```

**Common Examples:**

Nonsteroidal anti-inflammatory drugs like ibuprofen can damage kidneys, especially if you already have kidney disease. Certain blood pressure medicines can be dangerous if you have specific heart conditions. Acetaminophen can damage the liver if you have liver disease or drink alcohol heavily. Some medicines that treat low blood pressure can be dangerous if you have heart failure.

---

## Drug-Food Interactions

Learn how food and drinks can affect medicines. Some foods can change how well a medicine works or increase side effects.

For example, grapefruit juice can make some cholesterol medicines work too well, causing side effects. Vitamin K in leafy greens can reduce the effect of blood thinners. This module helps you understand these interactions so you can take your medicines safely.

**How to Use:**

```python
from medkit.drug.drug_food_interaction import get_drug_food_interaction

# Check if food affects a medicine
result = get_drug_food_interaction("warfarin", "vitamin K")
print(result)
```

**Common Examples:**

Grapefruit juice increases the effect of many cholesterol medicines and can cause dangerous side effects. Leafy green vegetables like spinach and kale contain vitamin K which reduces how well blood thinners like warfarin work, so you need to eat about the same amount consistently. Dairy products reduce how well some antibiotics work, so take these antibiotics on an empty stomach. Alcohol mixed with pain relievers or sedatives can cause serious problems.

---

## Similar Drugs and Alternatives

Find alternative medicines that work similarly to a medicine you take. If a medicine isn't working for you, causes bad side effects, or is too expensive, there are usually alternatives.

This module helps you understand what other medicines in the same family might work better for you. You can discuss these alternatives with your doctor or pharmacist.

**How to Use:**

```python
from medkit.drug.similar_drugs import get_similar_drugs

# Find alternatives
alternatives = get_similar_drugs("aspirin")
print(alternatives)
```

**Examples:**

If aspirin doesn't work well for you, similar pain relievers include ibuprofen, naproxen, and acetaminophen. If you're on one blood pressure medicine, your doctor might try a different type that works better for you. If one antibiotic doesn't work, another antibiotic in a similar class might be better.

---

## Drug Comparison

Compare medicines side-by-side to understand their differences. When you have several medicine options, comparison helps you and your doctor decide which is best for you.

You can compare how well medicines work, what side effects each has, how often you need to take them, how much they cost, and other important factors.

**How to Use:**

```python
from medkit.drug.drugs_comparison import compare_drugs

# Compare multiple medicines
comparison = compare_drugs(["aspirin", "ibuprofen", "acetaminophen"])
print(comparison)
```

**What to Compare:**

When comparing medicines, look at how well each medicine works for your specific problem, what side effects each can cause, how often you need to take it, whether it has food or drug interactions, and which one is most convenient for you.

---

## Disclaimer

This drug information is educational only and should not replace consultation with your pharmacist or doctor. Before taking any new medicine, changing doses, or stopping medicine, talk to your healthcare provider or pharmacist. Never stop or change medicines on your own without talking to your doctor first. Always take medicines exactly as prescribed, even if you feel better or feel worse.

Medical interactions can be serious. If you think you have taken too much medicine or are having a bad reaction, call poison control or emergency services immediately.

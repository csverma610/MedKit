# Drug Interactions Module

## Overview
Information about what happens when two or more medications are taken together.

**What it does:** Identifies dangerous drug combinations and explains interaction risks.
**Why it matters:** Some drug combinations are dangerous. Patients must know before taking multiple drugs.

---

## Scope
This module covers drug-drug, drug-disease, and drug-food interactions.

---

## What It Does

When you check for interactions, you get:

- **Interaction identified:** Whether drugs interact
- **Severity level:** Mild, moderate, or severe
- **Type of interaction:** How drugs interact (absorption, metabolism, etc.)
- **What happens:** Specific effects of the interaction
- **Timing:** When the interaction occurs
- **Risk assessment:** How serious the risk is
- **Recommendations:** Whether to take together, timing, monitoring
- **Monitoring needed:** What symptoms to watch for
- **Alternatives:** Can drugs be substituted if unsafe together
- **When to contact doctor:** What requires immediate medical attention

---

## Why It Matters

**Drug interactions can:**
- Reduce medication effectiveness
- Increase side effects significantly
- Cause organ damage
- Cause serious bleeding
- Cause dangerous blood sugar changes
- Cause severe allergic reactions
- Be life-threatening in some cases

---

## How to Use

### Python API
```python
from medkit.drug.drug_drug_interaction import get_drug_interaction

interaction = get_drug_interaction("warfarin", "aspirin")
print(interaction)

interaction = get_drug_interaction("metformin", "alcohol")
print(interaction)
```

### Command Line
```bash
python cli/cli_drug_interaction.py warfarin aspirin
python cli/cli_drug_interaction.py metformin alcohol --severity
```

---

## Severity Levels Explained

### MILD
Little to no risk, but you should be aware.

Effects:
- May slightly reduce one drug's effectiveness
- May slightly increase side effects
- Usually safe to take together

Example: Aspirin + acetaminophen (both pain relievers, can be taken together but watch total dose)

### MODERATE
Real interaction that needs management.

Effects:
- Can noticeably reduce how well one or both drugs work
- Can increase side effects significantly
- May need dose adjustment
- May need careful timing between doses
- May need monitoring by doctor

Example: Metformin + contrast dye (kidney imaging dye). Metformin must be held around dye procedures.

### SEVERE
Serious risk, avoid combination if possible.

Effects:
- Can cause dangerous side effects
- Can significantly reduce drug effectiveness
- Could harm organs (liver, kidneys, heart)
- Should not be taken together without doctor approval
- May require emergency medical attention if taken together

Example: Warfarin (blood thinner) + Aspirin = increased bleeding risk

---

## Common Serious Interactions

**Warfarin (blood thinner) + Aspirin**
- Risk: Severe bleeding
- What happens: Aspirin also thins blood; combination too risky
- What to do: Usually don't take together; if necessary, careful monitoring

**Metformin + Contrast Dye (imaging dye)**
- Risk: Kidney damage
- What happens: Dye can damage kidneys, especially with metformin
- What to do: Hold metformin before and after dye procedure

**SSRIs (antidepressants) + NSAIDs (pain relievers)**
- Risk: Stomach bleeding
- What happens: Both increase bleeding risk in stomach
- What to do: Use alternative pain reliever if possible

**Alcohol + Sedatives**
- Risk: Severe drowsiness, impaired judgment
- What happens: Both depress central nervous system
- What to do: Don't mix alcohol with sedatives

**Alcohol + Pain Relievers**
- Risk: Liver damage, stomach bleeding
- What happens: Both are hard on liver and stomach
- What to do: Don't drink alcohol while taking pain relievers

**Certain antibiotics + Birth control**
- Risk: Reduced contraceptive effectiveness
- What happens: Antibiotic interferes with birth control absorption
- What to do: Use backup contraception during antibiotic use

---

## Drug-Disease Interactions

Some medications are unsafe with certain health conditions:

**Ibuprofen + Kidney disease**
- Risk: Kidney damage
- Alternative: Acetaminophen usually safer

**ACE inhibitors + High potassium**
- Risk: Dangerous potassium levels
- Need: Monitor potassium levels

**Steroids + Diabetes**
- Risk: Difficult blood sugar control
- Need: More frequent monitoring and possible medication adjustment

**Blood pressure drugs + Heart arrhythmia**
- Risk: Worsening arrhythmia
- Alternative: Different drug class may be needed

---

## Drug-Food Interactions

**Grapefruit juice + Statins**
- Risk: Too much drug effect, muscle pain and liver damage
- Solution: Avoid grapefruit juice

**Leafy greens + Warfarin**
- Risk: Reduced blood thinner effect
- Solution: Eat consistent amounts of greens

**Dairy + Antibiotics**
- Risk: Reduced antibiotic absorption
- Solution: Take antibiotic 2 hours before dairy

**Tyramine-rich foods + MAOIs**
- Risk: Dangerous blood pressure spike
- Foods to avoid: Aged cheese, cured meats, fermented foods

---

## How to Prevent Interactions

**Before Taking Any Medication:**
✓ List ALL medications to doctor and pharmacist
✓ Include over-the-counter drugs
✓ Include supplements and herbs
✓ Include vitamin pills
✓ Mention alcohol use
✓ Ask about interactions

**At the Pharmacy:**
✓ Ask pharmacist to check for interactions
✓ Ask about food/alcohol interactions
✓ Ask about side effects
✓ Ask when to take it relative to meals

**When Taking Multiple Medications:**
✓ Use a pill organizer or tracker
✓ Set phone alarms for doses
✓ Keep a list of all medications
✓ Report new symptoms to doctor
✓ Don't add over-the-counter drugs without asking

---

## When to Seek Help

**Call Poison Control (1-800-222-1222):** If accidental overdose or drug interaction effects

**Call Doctor/Pharmacist:** For questions about interactions, side effects, new symptoms

**Go to ER / Call 911:** For severe symptoms (difficulty breathing, chest pain, severe bleeding, etc.)

---

## When to Use This Module

✓ Taking multiple medications
✓ Starting a new medication
✓ Taking over-the-counter with prescription drugs
✓ Using supplements or herbs with medications
✓ Drinking alcohol while on medications
✓ Want to verify no interactions

✗ Don't use to decide whether to take drugs
✗ Don't ignore moderate/severe interactions
✗ Don't assume all interactions are minor
✗ Don't stop medications without doctor approval
✗ Don't use this instead of asking pharmacist

---

## Limitations

**New interactions discovered.** Medical science constantly finds new interactions.

**Individual variation.** Some people are more susceptible to interactions.

**Dosage matters.** Higher doses increase interaction risk.

**Your pharmacist is expert.** Always verify with your pharmacist.

---

## Disclaimer

**Check Current Information:** Interaction information changes; ask pharmacist about current status.

**Not Medical Advice:** Consult healthcare provider about your specific medications.

**Your Pharmacist is Expert:** Pharmacists specialize in drug interactions; use their expertise.

**Always Inform Healthcare Providers:** List ALL medications, supplements, and herbs.

**Questions Encouraged:** Never hesitate to ask about interactions.

**Report Problems:** Tell doctor/pharmacist about any concerning symptoms.

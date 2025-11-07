# Mental Health Assessment Module

## Overview
Structured screening questionnaires for common mental health conditions.

**What it does:** Screens for depression, anxiety, bipolar, PTSD, substance use, suicide risk.
**Why it matters:** Early screening identifies mental health issues so people can get treatment.

---

## Scope
This module covers mental health screening questionnaires and assessments.

---

## What It Does

When you complete a mental health assessment, you get:

- **Questions:** Targeted questions about specific symptoms
- **Scoring:** Numerical score based on responses
- **Risk level:** Low, moderate, high, or crisis risk determination
- **Symptom analysis:** What symptoms you reported
- **Condition identification:** Possible mental health conditions
- **Severity:** How severe the symptoms appear
- **Urgency:** How quickly professional evaluation is needed
- **Recommendations:** What actions to take based on results
- **Resources:** What help is available
- **Next steps:** Specific guidance on what to do

---

## Why It Matters

**Screening helps:**
- Identify mental health issues early
- Reduce time to diagnosis and treatment
- Reduce suffering
- Prevent crises
- Connect people with help
- Track symptom changes over time
- Provide objective measurement

---

## How to Use

### Python API
```python
from medkit.mental_health.mental_health_assessment import assess_mental_health

responses = {
    "mood": "sad",
    "sleep": "poor",
    "energy": "low",
    "interest": "none"
}

assessment = assess_mental_health(responses)
print(assessment)
```

---

## Screening Categories

**Depression Screening:**
- Questions about: Sadness, hopelessness, guilt, energy, sleep, appetite, concentration
- Indicators: Feeling down most days, loss of interest, significant changes in sleep/appetite
- Urgency: High if suicidal thoughts; moderate if affecting function

**Anxiety Screening:**
- Questions about: Worry, panic, physical symptoms, avoidance
- Indicators: Excessive worry, panic attacks, physical tension
- Urgency: High if severe panic; moderate if interfering with function

**Bipolar Screening:**
- Questions about: Mood episodes (high and low), energy changes
- Indicators: Periods of high energy followed by depression
- Urgency: Moderate to high; requires specialist evaluation

**PTSD Screening:**
- Questions about: Trauma exposure, flashbacks, nightmares, avoidance
- Indicators: Recurrent trauma memories, hypervigilance, emotional numbness
- Urgency: Moderate; trauma-specific treatment needed

**Substance Use Screening:**
- Questions about: Frequency, amount, consequences of use
- Indicators: Regular use, repeated attempts to cut back, continued use despite problems
- Urgency: Moderate to high; depends on severity and consequences

**Suicide Risk Screening:**
- Questions about: Thoughts of suicide, intent, plan, access to means
- Indicators: Any suicidal ideation requires immediate attention
- Urgency: CRISIS if any suicidal thoughts or plan

---

## Understanding Scoring Results

### LOW RISK
- Minimal symptoms
- Functioning normally
- No immediate concern
- Action: Routine follow-up; maintain healthy habits

### MODERATE RISK
- Some symptoms present
- Symptoms may interfere with some activities
- Consider professional evaluation
- Action: See mental health professional within 1-2 weeks

### HIGH RISK
- Significant symptoms
- Interfering with work, relationships, daily function
- Strongly recommend professional evaluation
- Possible diagnosis: Probable mental health condition
- Action: See mental health professional within 1-3 days

### CRISIS RISK
- Severe symptoms
- Significant suicidal/homicidal ideation
- Or: Complete inability to function
- Action: EMERGENCY - Seek immediate help

---

## What Assessments Screen For

**Depressive Symptoms:**
- Persistent sadness (2+ weeks)
- Loss of interest in activities
- Changes in sleep or appetite
- Fatigue or low energy
- Difficulty concentrating
- Feelings of worthlessness or guilt
- Thoughts of death or suicide

**Anxiety Symptoms:**
- Excessive worry about many things
- Panic attacks (sudden intense fear)
- Physical symptoms (racing heart, sweating, shortness of breath)
- Avoidance of situations
- Restlessness or difficulty relaxing
- Irritability
- Sleep problems

**Bipolar Symptoms:**
- Periods of high energy, racing thoughts, decreased need for sleep
- Followed by periods of depression
- Impulsive behavior during high periods
- Family history of bipolar disorder

**PTSD Symptoms:**
- Traumatic event exposure
- Intrusive memories or flashbacks
- Nightmares about the event
- Avoidance of trauma reminders
- Negative mood changes
- Hypervigilance (feeling on guard)
- Angry outbursts

**Substance Use Issues:**
- Regular use despite negative consequences
- Failed attempts to cut back
- Continued use despite problems
- Neglect of other activities
- Tolerance (needing more to get same effect)
- Withdrawal when not using

---

## Important Notes

**These are screening tools,** not diagnostic instruments.

**Professional diagnosis required.** Only mental health professionals can diagnose.

**Screening is starting point.** Results indicate need for professional evaluation, not diagnosis.

**False positives possible.** Screening tool may suggest condition you don't have.

**False negatives possible.** Negative screening doesn't guarantee no mental health condition.

**Professional evaluation necessary.** Professional assessment includes more detailed evaluation.

---

## When to Take an Assessment

✓ Feeling down or worried for 2+ weeks
✓ Friends/family express concern
✓ Symptoms interfering with function
✓ Want to track symptoms over time
✓ Before seeing mental health professional
✓ To help determine if professional help needed

✗ Don't use as substitute for professional evaluation
✗ Don't assume results are diagnosis
✗ Don't delay getting help while waiting for assessment
✗ Don't use to self-treat; professional evaluation necessary

---

## After Completing Assessment

If LOW RISK:
- Continue healthy habits
- Monitor symptoms
- Routine follow-up if symptoms develop

If MODERATE RISK:
- Contact mental health professional
- Schedule appointment within 1-2 weeks
- Tell doctor about symptoms
- Ask for referral from primary care doctor

If HIGH RISK:
- Contact mental health professional immediately
- Schedule urgent appointment
- Consider crisis line if can't get prompt appointment
- Tell someone you trust about your symptoms

If CRISIS RISK:
- **Call 988 (US) or emergency number**
- Go to emergency room
- Tell someone immediately
- Remove access to means (if suicidal)
- Don't wait for appointment

---

## Crisis Resources

**National Suicide Prevention Lifeline:** 988
- Call or text 24/7, free, confidential
- Trained counselors available

**Crisis Text Line:** Text HOME to 741741
- Text-based crisis support
- 24/7, free, confidential

**911:** For immediate emergency
- Life-threatening situation
- Imminent danger to self or others

**Emergency Room:** Go immediately
- Suicidal or homicidal thoughts with plan
- Severe symptoms preventing function
- Psychiatric emergency

---

## When to Use This Module

✓ Want to screen for mental health conditions
✓ Wondering if symptoms are serious
✓ Preparing for mental health appointment
✓ Tracking symptoms over time
✓ Want objective assessment of symptoms

✗ Don't use instead of professional evaluation
✗ Don't assume positive screening = diagnosis
✗ Don't delay getting help
✗ Don't use for crisis situations (call 988 instead)

---

## Limitations

**Screening tools not diagnostic.** Professional evaluation necessary for diagnosis.

**Self-reported answers.** Results depend on honest, accurate answers.

**Context limited.** Assessment doesn't know your full history or situation.

**Individual variation.** Same symptoms can mean different things to different people.

**Professional interpretation.** Results should be discussed with mental health professional.

---

## Disclaimer

**Screening Tool Only:** This is educational screening, not diagnosis.

**Not Professional Evaluation:** Only mental health professionals can diagnose.

**Not Therapy:** Completing assessment doesn't provide treatment.

**Seek Professional Help:** If results suggest mental health condition, see professional.

**Crisis Requires Immediate Action:** If suicidal or in crisis, call 988 or go to ER.

**Your Life Matters:** Help is available. Mental health conditions are treatable.

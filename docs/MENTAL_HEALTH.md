# Mental Health Documentation

## Overview

The Mental Health module provides tools for mental health screening, assessment, and support. It includes structured questionnaires, chat interfaces, and crisis resources.

**What it does:** Screens for mental health conditions and provides support information.
**Why it matters:** Early screening helps identify mental health issues. Support tools provide education and crisis resources when needed.

---

## Mental Health Assessment

### Scope
Structured screening questionnaires for common mental health conditions.

### What it does
- Asks questions about mood, sleep, energy, concentration
- Evaluates anxiety symptoms (worry, panic, physical symptoms)
- Screens for depression (sadness, hopelessness, interest loss)
- Assesses substance use concerns
- Screens for bipolar disorder (high and low moods)
- Evaluates PTSD and trauma reactions
- Assesses suicide risk
- Provides scoring to indicate risk level

### Scoring Results

**Low Risk:** Minimal symptoms, no immediate concern, consider routine follow-up

**Moderate Risk:** Some symptoms present, consider talking to a doctor

**High Risk:** Significant symptoms, strongly recommend professional evaluation

**Crisis Risk:** Immediate danger, requires emergency intervention

### Why it matters
Early identification of mental health issues helps people get treatment. Screening questionnaires are used by professionals and validated through research.

### Usage
```python
from medkit.mental_health.mental_health_assessment import assess_mental_health

assessment = assess_mental_health(user_responses)
print(assessment)
```

### Important Note
These assessments are educational screening tools, not diagnosis. Only a mental health professional can diagnose.

---

## Mental Health Chat

### Scope
A conversational interface for discussing mental health concerns.

### What it does
- Provides supportive responses to mental health concerns
- Offers information about mental health conditions
- Suggests coping strategies (breathing, grounding techniques)
- Provides psychoeducation
- Identifies crisis warning signs
- Provides emergency resources when needed
- Encourages professional help
- Validates user experiences

### What It Cannot Do
- This is NOT therapy
- Cannot replace talking to a mental health professional
- Cannot prescribe medications
- Cannot treat mental health conditions
- Cannot provide crisis counseling (for that, call a hotline)

### Why it matters
When someone is struggling, having immediate supportive communication can reduce isolation and help them seek professional help.

### Usage
```python
from medkit.mental_health.mental_health_chat import start_mental_health_chat

chat = start_mental_health_chat()
response = chat.send_message("I've been feeling really sad")
print(response)
```

### Limitations

**Not a therapist:** AI cannot build the therapeutic relationship professionals provide.

**Not your doctor:** Cannot assess your unique medical situation.

**General guidance:** Uses general mental health knowledge, not your personal history.

**Always see a professional:** For any concerning symptoms or crisis, see a professional.

---

## SANE Interview

### Scope
Structured mental health interview used by mental health professionals.

### What it does
- Gathers current mental health symptoms
- Asks about symptom duration
- Explores past mental health history
- Investigates family mental health history
- Assesses substance use history
- Reviews medical history
- Evaluates social support and life situation
- Performs mental status examination
- Organizes information for professional review

### Why it matters
Professional mental health assessment requires comprehensive information. The SANE format ensures important areas are covered systematically.

### Interview Sections

1. **Demographics:** Age, gender, occupation, family composition
2. **Chief complaint:** Why the person is seeking help
3. **History of present illness:** Detailed symptom description
4. **Past psychiatric history:** Previous diagnoses, treatments, hospitalizations
5. **Family history:** Family members with mental health conditions
6. **Substance use:** Alcohol, drugs, tobacco, medications
7. **Medical history:** Physical conditions, surgeries, medications
8. **Social history:** Support systems, living situation, employment
9. **Mental status exam:** Appearance, mood, thought processes, perception

### Usage
```python
from medkit.mental_health.sane_interview import SANEInterview

interview = SANEInterview()
response = interview.next_question()
print(response)
```

### Why Professionals Use This Format
- Ensures nothing important is missed
- Provides standardized information for comparison
- Helps identify patterns and relationships
- Creates organized documentation
- Supports treatment planning

---

## Symptom Detection Chat

### Scope
Conversational symptom analysis for mental health concerns.

### What it does
- Listens to symptom description
- Asks clarifying questions
- Analyzes symptom patterns
- Identifies possible mental health conditions
- Prioritizes conditions by likelihood
- Identifies warning signs
- Recommends urgency of professional evaluation
- Suggests questions to ask a professional

### Why it matters
When people describe symptoms conversationally rather than answering questionnaires, they may provide more detailed information. This tool helps organize that information.

### Important Limitations

**Cannot diagnose:** Only professionals can diagnose mental health conditions.

**Overlapping symptoms:** Many conditions share similar symptoms.

**Individual variation:** Mental health presentations vary greatly by person.

**Use as starting point:** This helps prepare for professional evaluation, not replace it.

### Usage
```bash
python cli/cli_symptoms_checker.py --symptoms "sadness,hopelessness,sleep problems"
```

---

## Emergency Resources

### When to Use Emergency Resources

**Call or Text 988 (US Suicide & Crisis Lifeline):**
- Having thoughts of suicide
- In mental health crisis
- Feeling hopeless or overwhelmed
- Need to talk to someone immediately
- Available 24/7, free, confidential

**Text HOME to 741741 (Crisis Text Line):**
- Prefer texting to talking
- In crisis but not safe to call
- Need immediate support
- Available 24/7, free, confidential

**Call 911 or Go to ER:**
- Immediate danger to self or others
- Severe symptoms (unable to function, extreme agitation)
- Medication overdose or poisoning
- Medical emergency related to mental health

**Tell Someone You Trust:**
- A family member
- A close friend
- A teacher or counselor
- Anyone who cares about you

### International Resources

**International Association for Suicide Prevention:**
https://www.iasp.info/resources/Crisis_Centres/

Lists crisis hotlines and mental health resources worldwide.

---

## When to Seek Professional Help

### See a Mental Health Professional If:
- Feeling sad, empty, or hopeless most days for 2+ weeks
- Losing interest in activities you enjoy
- Significant changes in sleep or appetite
- Difficulty concentrating or making decisions
- Feeling worthless or guilty
- Thoughts of death or suicide
- Excessive worry interfering with daily life
- Panic attacks
- Using alcohol or drugs to cope
- Significant relationship or work problems

### Types of Professionals
- **Psychiatrist:** Medical doctor, prescribes medications
- **Psychologist:** Provides therapy and counseling
- **Licensed counselor:** Provides therapy and support
- **Clinical social worker:** Provides therapy and connects to resources
- **Peer specialist:** Someone with lived mental health experience

### Treatment Options
- **Therapy:** Talk therapy with trained professional
- **Medication:** Prescribed by psychiatrist
- **Support groups:** Connect with others having similar experiences
- **Hospitalization:** For safety when in crisis
- **Lifestyle changes:** Sleep, exercise, social connection

---

## Disclaimer

**Not Therapy:** These tools are not therapy. Therapy requires a trained professional building a relationship with you.

**Not Diagnosis:** These tools do not diagnose mental health conditions. Only professionals can diagnose.

**Not Crisis Counseling:** If in crisis, call a crisis hotline, not this tool.

**Educational Only:** This information educates about mental health. It does not treat mental health conditions.

**Immediate Help:** If thinking about suicide or in crisis:
- Call 988 (US)
- Text HOME to 741741
- Call 911
- Go to nearest emergency room
- Tell someone you trust

**Your Life Matters:** Help is available. Mental health conditions are treatable. You don't have to suffer alone.

**Professional Help Works:** Therapy, medication, and support help people recover. Treatment is effective.

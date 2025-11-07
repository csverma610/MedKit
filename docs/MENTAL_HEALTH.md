# Mental Health Documentation

The Mental Health module provides tools to understand, assess, and support mental health. It includes screening questionnaires, assessment tools, conversation interfaces, and important crisis resources.

## Mental Health Assessment

Complete structured assessments to understand your mental health. These are questionnaires used by mental health professionals to screen for common conditions like depression, anxiety, and other mental health issues.

Mental health assessments help you understand what you're experiencing and whether you should talk to a mental health professional. The assessments use questions that have been proven to help identify mental health conditions accurately.

**How to Use:**

```python
from medkit.mental_health.mental_health_assessment import assess_mental_health

# Complete an assessment
assessment = assess_mental_health()
print(assessment)
```

**From Command Line:**

```bash
python cli/cli_mental_health.py --assessment
```

**What Assessments Are Available:**

The module includes screening for depression that asks about mood, sleep, appetite, and energy. There's an anxiety screening that asks about worry and panic. Substance use screening helps identify if alcohol or drugs are a problem. Bipolar disorder screening looks for periods of high energy. PTSD screening asks about trauma reactions.

**How Assessments Work:**

You answer questions about how you've been feeling. Your answers create a score that indicates whether you might have a mental health condition. If your score suggests you might have an issue, the recommendation is to talk to a mental health professional for proper evaluation.

---

## Mental Health Chat

Talk to a supportive chatbot about your mental health concerns. This isn't therapy, but it provides a way to discuss what you're experiencing and get supportive responses.

The chat interface listens to what you say, responds supportively, provides information about mental health conditions, suggests coping strategies, and can help you understand whether you should talk to a professional.

**How to Use:**

```python
from medkit.mental_health.mental_health_chat import start_mental_health_chat

# Start chatting
chat = start_mental_health_chat()
response = chat.send_message("I've been feeling really sad")
print(response)
```

**From Command Line:**

```bash
python cli/cli_mental_health.py --chat
```

**What the Chat Can Do:**

The chat provides emotional support and understanding about your feelings. It offers information about mental health conditions. It suggests practical coping strategies like breathing exercises, grounding techniques, and self-care activities. It can identify if you're in crisis and provide emergency resources. It encourages you to talk to a professional.

**What the Chat Cannot Do:**

This chat is not therapy and cannot replace talking to a mental health professional. It doesn't prescribe medications. It doesn't treat mental health conditions. For serious concerns, always talk to a doctor or mental health professional.

---

## SANE Interview

Complete a structured mental health interview called SANE (Structured Affective Neuroscience Environment). This is a comprehensive interview format used by mental health professionals to gather detailed information about your mental health history.

The SANE interview systematically asks about your current symptoms, how long you've had them, past mental health issues, family history, substance use, medical conditions, and your current situation. This structured approach ensures nothing important is missed.

**How to Use:**

```python
from medkit.mental_health.sane_interview import SANEInterview

# Start the interview
interview = SANEInterview()
response = interview.next_question()
print(response)
```

**From Command Line:**

```bash
python cli/cli_mental_health.py --interview
```

**Interview Sections:**

The interview starts by getting your basic information. It asks about your main concern. It goes into detail about current symptoms. It asks about past mental health issues. It asks about family history of mental health problems. It asks about substance use. It covers medical history. It collects information about your life situation and support systems. It does a mental status examination.

**Why This Format Helps:**

The structured approach makes sure doctors have all the information they need. It follows the format mental health professionals are trained to use. It creates a comprehensive picture of your mental health history. Information gathered is organized so it's easy for professionals to review.

---

## Symptom Detection Chat

Chat about your symptoms in a conversational way to explore what might be going on. This is different from a rigid questionnaire - it's more like talking to someone.

As you describe your symptoms in conversation, the tool analyzes them and helps identify possible conditions you might want to discuss with a doctor.

**How to Use:**

```bash
python cli/cli_symptoms_checker.py --symptoms "sadness,hopelessness,sleep problems"
```

**What Happens:**

You describe how you're feeling. The tool asks clarifying questions to understand better. Based on what you say, it suggests possible mental health conditions that have those symptoms. It identifies any emergency warning signs. It recommends whether you should talk to a professional.

**Important Limitation:**

This symptom checker is educational only. It cannot diagnose you. Many different mental health conditions have overlapping symptoms. Only a mental health professional who talks to you and learns your full history can make a real diagnosis. Use this as a starting point for talking to a professional, not as a diagnosis.

---

## Emergency Resources

If you're in a mental health crisis or having thoughts of suicide, get help immediately. These resources are available 24/7.

**National Suicide Prevention Lifeline:** 988 (call or text, available in the US)
You can call or text 988 any time if you're having thoughts of suicide or if you're in crisis. Trained counselors will listen and help.

**Crisis Text Line:** Text HOME to 741741
You can text if you're more comfortable communicating that way. Send messages to 741741 and trained counselors will respond.

**Emergency Services:** 911 (in the US) or your local emergency number
Call 911 if you're in immediate danger. Go to your nearest emergency room if you think you might hurt yourself.

**International Association for Suicide Prevention:** https://www.iasp.info/resources/Crisis_Centres/
This website lists crisis hotlines around the world.

---

## When to Get Help

Talk to a mental health professional if you're experiencing any of these: feeling sad or empty most of the day for more than two weeks, losing interest in activities you normally enjoy, significant changes in sleep or appetite, difficulty concentrating, feeling hopeless or worthless, having thoughts of death or suicide, excessive worry that interferes with daily life, panic attacks, substance use problems, or significant life changes.

Mental health is just as important as physical health. Getting help early works better than waiting. Mental health professionals can help, and treatment works.

---

## What Mental Health Treatment Involves

Therapy involves talking to a trained mental health professional who helps you understand your feelings and develop strategies to feel better. Different types of therapy work for different people.

Medication prescribed by a psychiatrist can help with some mental health conditions. Many people benefit from a combination of therapy and medication.

Support groups connect you with others experiencing similar challenges. Peer support from people who understand what you're going through can be very helpful.

Lifestyle changes like better sleep, exercise, and social connection support mental health recovery.

---

## Disclaimer

This mental health information is educational only. It is not treatment. If you're struggling mentally, please talk to a mental health professional, doctor, or call a crisis line. Mental health conditions are treatable, and help is available. You don't have to struggle alone.

If you're thinking about suicide or hurting yourself, please reach out:
- Call or text 988 (Suicide & Crisis Lifeline)
- Text HOME to 741741
- Call 911 or go to your nearest emergency room
- Tell someone you trust how you're feeling

Your life matters. Help is available.

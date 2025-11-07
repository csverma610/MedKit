# Diagnostic Tools Documentation

The Diagnostic Tools module helps you understand medical tests, equipment, physical examinations, and how doctors decide what tests to order. It includes information about blood tests, imaging tests, procedures, and examination techniques.

## Medical Tests Information

Understand what medical tests do and what the results mean. Medical tests help doctors figure out what's wrong or monitor how you're doing with a treatment.

When your doctor orders a blood test, imaging test, or other diagnostic test, you can look it up to understand what the test is for, how it's done, what the normal results are, and what abnormal results might mean.

**How to Use:**

```python
from medkit.diagnostics.medical_test_info import get_test_info

# Look up a test
test = get_test_info("complete blood count")
print(test)
```

**Types of Tests:**

The diagnostic module covers many common tests including blood tests that count different cell types and measure chemicals, tests that look at how your heart functions, tests that measure hormone levels, kidney and liver function tests, and many others. Each test explanation tells you why the test is done, what samples are needed, what the normal values are, and what abnormal results might indicate.

**Why Tests Matter:**

Tests help doctors detect diseases early, monitor how well treatments are working, and understand what's causing your symptoms. Understanding what tests measure helps you have better conversations with your doctor about your health.

---

## Diagnostic Devices

Learn about medical equipment and machines used to diagnose health problems. These devices include heart monitors, ultrasound machines, CT scanners, and many others.

Understanding how diagnostic devices work helps you know what to expect if your doctor orders imaging or monitoring. Some devices use sound waves, some use radiation, and some use magnets to create pictures of your body.

**How to Use:**

```python
from medkit.diagnostics.medical_test_devices import get_device_info

# Learn about a device
device = get_device_info("ultrasound machine")
print(device)
```

**Common Devices:**

This module covers heart monitors that record your heartbeat, ultrasound machines that use sound waves to make pictures, CT scanners that take many X-rays to create detailed images, MRI machines that use magnets, X-ray equipment, and many other machines. Each device explanation describes what it does and what to expect.

---

## Physical Examinations

Get detailed guides for physical examinations performed by doctors. Physical examination is when your doctor looks at, listens to, and feels your body to check for health problems.

The examination guides cover how to examine different body systems including the heart and lungs, abdomen, nervous system, muscles and joints, skin, and others. These guides help you understand what doctors are doing during exams and what they're looking for.

**How Physical Exams Work:**

During a physical exam, doctors use special techniques to evaluate each part of your body. They listen with a stethoscope to hear heart and lung sounds. They feel your abdomen to check if organs feel normal. They test reflexes to check nerve function. They look at your eyes, ears, and throat. All these examinations help doctors detect problems.

**What Gets Examined:**

The cardiac examination looks for signs of heart problems. The respiratory examination checks lung function. The neurological examination tests how your brain and nerves work. The abdominal examination checks the organs in your belly. The musculoskeletal examination evaluates bones, muscles, and joints.

---

## Medical Decision Guides

Understand the process doctors use to figure out what's causing your symptoms. Decision guides are step-by-step paths that help doctors decide what disease you might have based on your symptoms and test results.

These guides are based on medical experience and research about what symptoms lead to what diagnoses. Understanding decision guides helps you see how doctors think about diagnosis.

**How Decision Guides Work:**

A doctor starts with your symptoms, then asks questions to understand more about them. Based on your answers, the doctor narrows down possible diagnoses and orders specific tests. Test results provide more information. Eventually, the doctor has enough information to make a diagnosis.

**Examples of Conditions with Guides:**

There are decision guides for chest pain (is it a heart attack, anxiety, or muscle pain?), shortness of breath (is it heart disease, lung disease, or anxiety?), headaches (is it a migraine, tension headache, or something serious?), and many other conditions.

---

## Symptom Detection

Use this tool to explore what conditions might cause your symptoms. This is not a diagnosis, but it helps you understand possibilities you could discuss with your doctor.

When you input your symptoms, the tool analyzes them and suggests conditions that commonly cause those symptoms. This helps you prepare for a doctor visit by thinking about what questions to ask.

**How to Use:**

```bash
python cli/cli_symptoms_checker.py --symptoms "fever,cough,fatigue"
```

**Important:**

This tool provides educational information only. It cannot diagnose you. Many different conditions can cause the same symptoms. Only a doctor who examines you and does appropriate tests can make a real diagnosis. If you think you have a serious condition, see a doctor right away instead of using an online tool.

---

## Test Relationships and Sequencing

Understand how medical tests relate to each other and what order doctors use to figure out diagnosis.

Doctors don't order tests randomly. They start with initial tests that give general information, then order follow-up tests based on what the first tests show. This helps get to a diagnosis efficiently and avoids unnecessary testing.

**How Testing Sequences Work:**

For example, if someone has symptoms of diabetes, the doctor might first do a blood sugar test. If that's high, the doctor then does a more specific test to confirm diabetes. Then, once diabetes is confirmed, the doctor does tests to check for complications like kidney or heart damage.

**Benefits of Smart Testing:**

Good test sequencing saves money by not doing unnecessary tests. It gets to diagnosis faster. It avoids exposing you to unnecessary radiation or other risks. It helps doctors understand your specific situation rather than testing for everything.

---

## Disclaimer

This diagnostic information is educational only. It helps you understand medical tests and examinations better, but it should not replace consultation with your doctor. Only a doctor who evaluates you can determine what tests you need and what the results mean for your specific situation. Don't try to self-diagnose based on this information. Always see a healthcare provider about medical concerns.

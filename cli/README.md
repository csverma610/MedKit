# MedKit CLI Tools

This directory contains command-line interfaces for querying MedKit medical information modules. These tools provide easy access to comprehensive medical knowledge through the terminal.

## Available CLI Tools (11 Tools)

### 1. Disease Information
```bash
python cli/cli_disease_info.py <disease_name> [--verbose]
```
Get comprehensive disease definitions, symptoms, causes, and treatments.

**Example:**
```bash
python cli/cli_disease_info.py diabetes
python cli/cli_disease_info.py "heart disease" --verbose
```

### 2. Comprehensive Medical Topic Documentation
```bash
python cli/cli_medical_topic.py <topic_name> [--output file.json] [--verbose]
```
Generate comprehensive medical documentation with epidemiology, pathophysiology, clinical presentation, diagnosis, treatment, prognosis, prevention, and embedded patient FAQs.

**Example:**
```bash
python cli/cli_medical_topic.py diabetes
python cli/cli_medical_topic.py "heart disease" --verbose
python cli/cli_medical_topic.py asthma --output asthma_info.json
```

### 3. Medical Test Information
```bash
python cli/cli_medical_test.py <test_name> [--output file.json] [--verbose]
```
Get detailed information about medical tests including what they measure, how they're performed, normal ranges, abnormal findings, risks, and timelines.

**Example:**
```bash
python cli/cli_medical_test.py "complete blood count"
python cli/cli_medical_test.py CBC --verbose
python cli/cli_medical_test.py "chest X-ray" --output xray_info.json
```

### 4. Medicine/Drug Information
```bash
python cli/cli_medicine_info.py <drug_name> [--interactions] [--verbose]
```
Get detailed medication information including dosages, side effects, and contraindications.

**Example:**
```bash
python cli/cli_medicine_info.py aspirin
python cli/cli_medicine_info.py ibuprofen --interactions
```

### 5. Drug-Drug Interaction Checker
```bash
python cli/cli_drug_interaction.py <drug1> <drug2> [--severity] [--verbose]
```
Check interactions between two medications and get severity information.

**Example:**
```bash
python cli/cli_drug_interaction.py aspirin ibuprofen
python cli/cli_drug_interaction.py warfarin aspirin --severity
```

### 6. Medical Anatomy
```bash
python cli/cli_medical_anatomy.py <body_part> [--functions] [--verbose]
```
Get anatomical structures and physiological function information about body parts.

**Example:**
```bash
python cli/cli_medical_anatomy.py heart
python cli/cli_medical_anatomy.py brain --functions
```

### 7. Medical Dictionary/Terminology
```bash
python cli/cli_medical_dictionary.py <term> [--synonyms] [--verbose]
```
Look up medical terms and get definitions, synonyms, and related information.

**Example:**
```bash
python cli/cli_medical_dictionary.py hypertension
python cli/cli_medical_dictionary.py "myocardial infarction" --verbose
```

### 8. Medical Specialties
```bash
python cli/cli_medical_speciality.py <specialty> [--doctors] [--conditions] [--procedures]
```
Get information about medical specialties, specialists, and their areas of focus.

**Example:**
```bash
python cli/cli_medical_speciality.py cardiology
python cli/cli_medical_speciality.py neurology --conditions
```

### 9. Herbal Medicine Information
```bash
python cli/cli_herbal_info.py <herb_name> [--benefits] [--interactions] [--dosage] [--safety]
```
Get information about herbal remedies, traditional uses, and safety information.

**Example:**
```bash
python cli/cli_herbal_info.py turmeric
python cli/cli_herbal_info.py ginger --benefits
python cli/cli_herbal_info.py echinacea --interactions
```

### 10. Mental Health Tools
```bash
python cli/cli_mental_health.py [--assessment] [--chat] [--interview] [--anonymous]
```
Access mental health assessments, support chat, and SANE interview tools.

**Example:**
```bash
python cli/cli_mental_health.py --assessment
python cli/cli_mental_health.py --chat
python cli/cli_mental_health.py --interview
```

### 11. Symptom Checker
```bash
python cli/cli_symptoms_checker.py --symptoms "symptom1,symptom2,..." [--severity] [--duration] [--urgent]
```
Check symptoms and get possible conditions for informational purposes (NOT a diagnosis).

**Example:**
```bash
python cli/cli_symptoms_checker.py --symptoms "fever,cough,fatigue"
python cli/cli_symptoms_checker.py --symptoms "chest pain" --urgent
```

## Setup

Install MedKit with development dependencies:
```bash
pip install -e ".[dev]"
```

Or install CLI requirements directly:
```bash
pip install -r requirements.txt
```

## Using from Command Line

After installation, you can run CLI scripts from any directory:

```bash
cd /path/to/medkit
python cli/cli_disease_info.py diabetes
```

Or make scripts executable:
```bash
chmod +x cli/cli_*.py
./cli/cli_disease_info.py diabetes
```

## Adding New CLI Tools

To add a new CLI tool:

1. Create a new file `cli/cli_<module_name>.py`
2. Import the relevant medkit function
3. Use argparse for argument handling
4. Add usage examples in this README

## Integration with Entry Points

These CLI tools are also accessible via the main package entry point:
```bash
pip install -e .
medkit --help
```

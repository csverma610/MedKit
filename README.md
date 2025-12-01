# MedKit: Medical Knowledge System

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation Status](https://readthedocs.org/projects/medkit/badge/?version=latest)](https://medkit.readthedocs.io)

A comprehensive medical information and reference system powered by Google's Gemini AI. MedKit provides programmatic access to medical knowledge, drug interactions, disease information, diagnostic tools, and clinical decision support.

**Status:** Beta (v1.0.0) | **License:** MIT | **Python:** 3.8+

## System Architecture

![MedKit Architecture Diagram](medkit_architecture.svg)

### Text Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MedKit: Medical Reference System                          │
│                      Powered by Google Gemini AI                             │
└─────────────────────────────────────────────────────────────────────────────┘

                         ┌──────────────────────────┐
                         │   Core Client & Config   │
                         │   (Gemini API Client)    │
                         └──────────────┬───────────┘
                                        │
        ┌───────────────────────────────┼───────────────────────────────┐
        │                               │                               │
        ▼                               ▼                               ▼
 ┌─────────────────┐           ┌─────────────────┐           ┌─────────────────┐
 │ Medical Reference│           │  Drug Database  │           │ Diagnostic Tools│
 ├─────────────────┤           ├─────────────────┤           ├─────────────────┤
 │ • Disease Info  │           │ • Medicine Info │           │ • Medical Tests │
 │ • Anatomy       │           │ • Drug-Drug     │           │ • Devices       │
 │ • Dictionary    │           │ • Drug-Disease  │           │ • Exams         │
 │ • Specialties   │           │ • Drug-Food     │           │ • Decision Guide│
 │ • Surgery       │           │ • Alternatives  │           │ • Symptom Check │
 │ • Implants      │           │ • Comparison    │           │ • Case Reports  │
 │ • Herbs         │           │                 │           │                 │
 └─────────────────┘           └─────────────────┘           └─────────────────┘

        ┌──────────────────────────────────────────────────────────────┐
        │                    Mental Health Support                     │
        ├──────────────────────────────────────────────────────────────┤
        │ • Assessments  • Chat Support  • SANE Interview  • Resources │
        └──────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  Utilities: LMDB Caching • Privacy Compliance • Fact Checking • Offline     │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Features

### Medical Reference

Comprehensive medical knowledge base covering:
- Disease information with definitions, symptoms, causes, and treatments
- Anatomical structures and physiological functions
- Medical specialties and disciplines
- Surgical procedures, techniques, and instruments
- Medical implants and prosthetics
- Herbal medicine with evidence-based information

See [docs/medical_ai/](docs/medical_ai/) for complete documentation.

### Drug Database

Pharmaceutical reference covering:
- Medicine information including dosing, side effects, contraindications
- Drug-drug interactions between medications
- Drug-disease interactions and safety in specific conditions
- Drug-food interactions and dietary considerations
- Alternative medications and drug comparisons

See [docs/drug_ai/](docs/drug_ai/) for complete documentation.

### Diagnostic Tools

Clinical decision support including:
- Medical tests and diagnostic procedures
- Medical diagnostic equipment and devices
- Physical examination guides for 27+ body systems
- Symptom analysis and differential diagnosis
- Evidence-based clinical decision trees
- Medical case studies for reference

See [docs/diagnostic_ai/](docs/diagnostic_ai/) for complete documentation.

### Mental Health

Psychological assessment and support:
- Structured screening tools and assessments
- Conversational support interface
- Structured clinical interview tools
- Interactive symptom assessment
- Crisis resources and support information

See [docs/psychology_ai/](docs/psychology_ai/) for complete documentation.

### Utilities

Infrastructure and support features:
- LMDB-based caching for offline access and performance
- HIPAA-compliant data handling
- Medical fact verification
- Structured logging and configuration

## Installation

### Basic Installation

```bash
pip install git+https://github.com/csv610/medkit.git
```

### With Development Tools

```bash
pip install git+https://github.com/csv610/medkit.git#egg=medkit[dev]
```

### With Documentation Building

```bash
pip install git+https://github.com/csv610/medkit.git#egg=medkit[docs]
```

### Local Development

```bash
git clone https://github.com/csv610/medkit.git
cd medkit
make dev-setup
```

Or manually:
```bash
pip install -e ".[dev]"
```

## System Requirements

- Python 3.8+
- Google Gemini API key (obtain from https://ai.google.dev/)
- 512MB minimum RAM (1GB recommended)
- 500MB+ disk space for LMDB caching
- Internet connection for initial setup and generation (caching enables offline use)

## Quick Start

### Programmatic Usage

```python
from medkit.medical.disease_info import get_disease_info
from medkit.drug.medicine_info import get_medicine_info
from medkit.drug.drug_drug_interaction import get_drug_interaction

# Get disease information
disease_info = get_disease_info("diabetes")
print(disease_info)

# Get medicine information
med_info = get_medicine_info("aspirin")
print(med_info)

# Check drug interactions
interaction = get_drug_interaction("aspirin", "ibuprofen")
print(interaction)
```

### Command-Line Usage

```bash
# Disease information
python cli/cli_disease_info.py diabetes
python cli/cli_disease_info.py "heart disease" --verbose

# Medicine information
python cli/cli_medicine_info.py aspirin
python cli/cli_medicine_info.py ibuprofen --interactions

# Medical anatomy
python cli/cli_medical_anatomy.py heart
python cli/cli_medical_anatomy.py brain --functions
```

See [cli/README.md](cli/README.md) for more CLI examples.

## Project Structure

```
medkit/
├── core/                    # Core client and configuration
│   ├── config.py           # Configuration management
│   ├── medkit_client.py    # Main MedKit client
│   └── gemini_client.py    # Google Gemini API integration
│
├── medical/                # Medical reference modules (32 files)
│   ├── disease_info.py
│   ├── medical_anatomy.py
│   ├── medical_dictionary.py
│   ├── medical_speciality.py
│   ├── medical_procedure_info.py
│   ├── surgery_info.py
│   ├── surgical_tool_info.py
│   ├── medical_implant.py
│   ├── herbal_info.py
│   ├── medical_test_graph.py
│   └── ... (more modules)
│
├── drug/                   # Drug and medicine information
│   ├── medicine_info.py
│   ├── drug_drug_interaction.py
│   ├── drug_disease_interaction.py
│   ├── drug_food_interaction.py
│   ├── similar_drugs.py
│   ├── drugs_comparison.py
│   ├── rxnorm_client.py    # RxNorm API integration
│   └── rx_med_info.py
│
├── diagnostics/            # Diagnostic tools
│   ├── medical_test_info.py
│   ├── medical_test_devices.py
│   └── medical_tests_graph.py
│
├── mental_health/          # Mental health modules
│   ├── mental_health_assessment.py
│   ├── mental_health_chat.py
│   ├── sane_interview.py
│   └── sympton_detection_chat.py
│
├── phyexams/               # Physical examination modules (27 files)
│   ├── exam_head_and_neck.py
│   ├── exam_heart.py
│   ├── exam_lungs_chest.py
│   ├── exam_neurological.py
│   └── ... (more exam modules)
│
├── utils/                  # Utility modules
│   ├── logging_config.py
│   ├── privacy_compliance.py
│   ├── lmdb_storage.py
│   └── pydantic_prompt_generator.py
│
└── vistools/               # Visualization tools
    └── visualize_decision_guide.py
```

## Configuration

### Environment Setup

Set the Google Gemini API key:

```bash
export GEMINI_API_KEY="your-api-key-here"
```

### Programmatic Configuration

```python
from medkit.core.config import MedKitConfig

config = MedKitConfig(
    api_key="your-api-key",
    model="gemini-2.5-flash",
    temperature=0.3,              # Low temperature for medical accuracy
    db_store=True,                # Enable LMDB caching
    db_path="~/.medkit/cache",    # Custom cache location
    db_capacity_mb=500,           # Cache size limit
    verbosity="info"              # Logging level
)
```

## Documentation

Comprehensive documentation is available for all features and modules.

### Documentation Index

| Section | Description | Location |
|---------|-------------|----------|
| Medical Reference | Disease info, anatomy, specialties, implants, herbal medicine | [docs/medical_ai/](docs/medical_ai/) |
| Drug Database | Medicine info, drug interactions, dosing, alternatives | [docs/drug_ai/](docs/drug_ai/) |
| Diagnostic Tools | Medical tests, devices, physical exams, decision guides | [docs/diagnostic_ai/](docs/diagnostic_ai/) |
| Mental Health | Assessments, chat, SANE interview, crisis resources | [docs/psychology_ai/](docs/psychology_ai/) |
| CLI Tools | Command-line interfaces for all modules | [cli/README.md](cli/README.md) |
| API Reference | Complete API documentation | [docs/api/](docs/api/) |
| Tutorials | Step-by-step usage guides | [docs/tutorials.rst](docs/tutorials.rst) |
| Development | Setup for developers | [docs/development_setup.rst](docs/development_setup.rst) |

### Building Documentation Locally

Using Make:
```bash
make docs              # Build HTML documentation
make docs-serve        # Build and serve locally at http://localhost:8000
make docs-clean        # Remove built documentation
```

Or manually:
```bash
cd docs
pip install -r ../requirements-dev.txt
sphinx-build -b html . _build/html
```

Then open `docs/_build/html/index.html` in your browser.

### Online Documentation

- ReadTheDocs: https://medkit.readthedocs.io
- Full API reference with module and function documentation
- Practical tutorials and use cases
- Contributor setup instructions

## Usage Examples

### Disease Information

```python
from medkit.medical.disease_info import get_disease_info

# Get comprehensive disease information
info = get_disease_info("type 2 diabetes")
print(f"Definition: {info.definition}")
print(f"Symptoms: {info.symptoms}")
print(f"Treatment: {info.treatment}")
```

### Drug Interactions

```python
from medkit.drug.drug_drug_interaction import get_drug_interaction

# Check interaction between two drugs
interaction = get_drug_interaction("aspirin", "warfarin")
print(f"Severity: {interaction.severity}")
print(f"Details: {interaction.description}")
```

### Physical Examinations

```python
from medkit.phyexams.exam_heart import examine_heart

# Get heart examination guide
exam_guide = examine_heart()
print(exam_guide.procedure)
print(exam_guide.findings)
```

### Mental Health Assessment

```python
from medkit.mental_health.mental_health_assessment import assess_mental_health

# Conduct mental health assessment
assessment = assess_mental_health(user_responses)
print(f"Risk Level: {assessment.risk_level}")
print(f"Recommendations: {assessment.recommendations}")
```

## Testing

The project includes 135 test files covering all modules with comprehensive coverage.

### Using Make

```bash
make test              # Run all tests
make test-cov          # Run with coverage report
make test-parallel     # Run tests in parallel (faster)
make test-unit         # Unit tests only
make test-fast         # Quick tests with minimal output
```

### Using pytest Directly

```bash
pip install -e ".[dev]"      # Install test dependencies

pytest tests/                 # Run all tests
pytest tests/ --cov=medkit    # Run with coverage
pytest tests/test_disease_info.py  # Run specific test file
```

### Coverage Reports

Coverage reports are generated automatically with:
```bash
make test-cov
# View report in htmlcov/index.html
```

## Development

### Setup Development Environment

```bash
make dev-setup          # Complete setup
# or manually:
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

### Available Make Targets

```bash
make help               # Show all available targets
make install-dev        # Install development dependencies

# Code Quality
make lint               # Run all quality checks
make format             # Format code with black and isort
make format-check       # Check formatting without changes
make typecheck          # Type checking with mypy
make security           # Security scanning with bandit

# Testing
make test               # Run all tests
make test-cov           # Run tests with coverage report
make test-fast          # Quick test run
make test-parallel      # Run tests in parallel

# Documentation
make docs               # Build documentation
make docs-serve         # Build and serve locally

# CI/CD
make pre-commit         # Quick checks before commit
make ready              # Full CI checks locally

# Cleanup
make clean              # Remove all artifacts
make clean-pyc          # Remove Python cache files
```

### Code Quality

Format and lint code:
```bash
black medkit/ cli/ tests/           # Format with black
isort medkit/ cli/ tests/           # Sort imports
flake8 medkit/ cli/ tests/          # Check linting
mypy medkit/ cli/ tests/            # Type checking
```

Or use the convenience target:
```bash
make lint               # Run all checks
make format             # Run formatters
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [CONTRIBUTING.md](docs/contributing.rst) for detailed guidelines.

## Important Disclaimers

**Medical Disclaimer:** This tool is for informational purposes only and should not be used as a substitute for professional medical advice. Always consult with qualified healthcare professionals for medical decisions.

**Accuracy:** Medical information is constantly evolving. Verify all information with current medical literature and professional guidance before use.

**Privacy:** Handle all patient data with care. Ensure compliance with HIPAA and applicable data protection regulations. MedKit provides privacy-aware features but users remain responsible for compliance.

**Emergency Situations:** For medical emergencies, contact emergency services or visit a hospital immediately. Do not rely on this tool for emergency diagnosis or treatment.

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## Citation

If you use MedKit in research or publications, please cite:

```bibtex
@software{medkit2024,
  title={MedKit: Medical Information and Reference System},
  author={Your Name},
  year={2024},
  url={https://github.com/csv610/medkit}
}
```

## Acknowledgments

- Google Gemini AI (https://ai.google.dev/)
- RxNorm API (https://www.nlm.nih.gov/research/umls/rxnorm/)
- Pydantic (https://pydantic-docs.helpmanual.io/)
- LMDB (https://lmdb.readthedocs.io/)
- Sphinx documentation generator (https://www.sphinx-doc.org/)

## Support & Feedback

- Documentation: https://medkit.readthedocs.io
- Issues: https://github.com/csv610/medkit/issues
- Discussions: https://github.com/csv610/medkit/discussions
- Help: See /help in Claude Code

## Technology Stack

### Core Dependencies
- google-genai (>=0.3.0) - Gemini AI integration
- pydantic (>=2.0.0) - Data validation and schemas
- requests (>=2.28.0) - HTTP client
- lmdb (>=1.0.0) - Embedded database caching
- networkx (>=3.0) - Graph analysis
- matplotlib (>=3.6.0) - Visualization
- streamlit - Web UI framework

### Development Tools
- pytest - Testing framework
- black - Code formatting
- flake8 - Linting
- mypy - Type checking
- sphinx - Documentation generation

## Project Statistics

- **Python Modules:** 123
- **Lines of Code:** ~39,560
- **Test Files:** 135
- **CLI Tools:** 19+
- **Physical Exam Guides:** 27+

## Roadmap

Planned features include:
- Web dashboard for interactive queries
- Mobile app integration
- EHR system integration
- Multilingual support
- Enhanced offline capabilities
- API endpoint service
- Real-time clinical guideline updates

## Related Resources

- [SNOMED CT](https://www.snomed.org/) - Standardized medical terminology
- [ICD-10](https://www.cdc.gov/nchs/icd/icd10cm.htm) - International Classification of Diseases
- [OpenEHR Standards](https://www.openehr.org/) - Electronic health record standards
- [HL7 FHIR](https://www.hl7.org/fhir/) - Healthcare data interchange standard
- [PubMed](https://pubmed.ncbi.nlm.nih.gov/) - Medical literature database
- [NIH](https://www.nih.gov/) - National Institutes of Health
- [CDC](https://www.cdc.gov/) - Centers for Disease Control

---

**Last Updated:** December 2024

For the latest information, visit the GitHub repository: https://github.com/csv610/medkit

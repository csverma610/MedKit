"""synthetic_case_report - Generate synthetic medical case reports following CARE Guidelines.

This module generates comprehensive, realistic synthetic medical case reports using structured
Pydantic data models and the MedKit AI client. Reports follow CARE Guidelines (CAse REport)
standards with schema-aware prompting for consistent, high-quality output. Reports are specifically
designed for specialized physicians and contain detailed clinical information without explicit
disease/condition names to prevent diagnostic bias and require independent clinical assessment.

QUICK START:
    Generate a single case report:

    >>> from synthetic_case_report import SyntheticCaseReportGenerator
    >>> generator = SyntheticCaseReportGenerator()
    >>> result = generator.generate("Type 2 Diabetes")
    >>> print(f"Generated case report saved")

    Generate multiple case reports for the same condition:

    >>> results = generator.generate_multiple("Myocardial Infarction", num_cases=3)
    >>> print(f"Generated {len(results)} case reports")

    Or use the CLI:

    $ python synthetic_case_report.py "Acute Stroke"
    $ python synthetic_case_report.py "Pneumonia" -n 5 -o reports/

COMMON USES:
    1. Medical education - providing realistic case scenarios for resident and medical student training
    2. Clinical decision support - testing diagnostic reasoning without revealing diagnosis upfront
    3. Research datasets - generating synthetic patient data for clinical research studies
    4. Test data generation - creating realistic test cases for medical software applications
    5. Diagnostic reasoning exercises - developing physician assessment skills through unbiased case presentation

KEY FEATURES AND COVERAGE AREAS:
    - Patient information and demographics including age, gender, ethnicity, occupation, and social history
    - Clinical findings with chief complaint, symptom onset, progression, associated symptoms, and physical exam results
    - Complete diagnostic workup including laboratory tests, imaging, pathology, and specialized testing results
    - Timeline with key clinical events and diagnostic progression chronologically documented
    - Therapeutic interventions including medications, surgeries, procedures, and supportive care
    - Follow-up outcomes and functional status tracking patient recovery and current condition
    - Discussion section with case significance, learning points, and clinical pearls without naming diagnosis
    - Patient perspective capturing experience, understanding, and treatment satisfaction
    - Ethical documentation including informed consent and institutional approval status
    """

import json
import sys
import uuid
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from pydantic import BaseModel, Field
from typing import Optional, List

from medkit.core.medkit_client import MedKitClient
from medkit.core.module_config import get_module_config
from medkit.utils.logging_config import setup_logger

import hashlib
from medkit.utils.lmdb_storage import LMDBStorage, LMDBConfig
from medkit.utils.storage_config import StorageConfig

# Configure logging
logger = setup_logger(__name__)

# ============================================================================ 
# CONFIGURATION
# ============================================================================ 

@dataclass
class Config(StorageConfig):
    """Configuration for the synthetic case report generator."""
    output_dir: Path = field(default_factory=lambda: Path("outputs"))
    log_file: Path = field(default_factory=lambda: Path(__file__).parent / "logs" / f"{Path(__file__).stem}.log")
    specialty: str = "Medicine/Advanced Clinical Case"
    verbosity: int = 2  # Verbosity level: 0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG

    def __post_init__(self):
        """Set default db_path if not provided, then validate."""
        if self.db_path is None:
            self.db_path = str(
                Path(__file__).parent.parent / "storage" / "synthetic_case_report.lmdb"
            )
        # Call parent validation
        super().__post_init__()
# ============================================================================ 
# PYDANTIC MODELS FOR CASE REPORT STRUCTURE
# ============================================================================ 

class PatientInformation(BaseModel):
    age: int = Field(description="Patient age in years")
    gender: str = Field(description="Patient gender (Male/Female/Other)")
    ethnicity: str = Field(description="Patient ethnicity or ancestry")
    occupation: str = Field(description="Patient's occupation or profession")
    relevant_family_history: str = Field(description="Family history relevant to the condition")
    past_medical_history: str = Field(description="Previous medical conditions, comma-separated")
    surgical_history: str = Field(description="Previous surgical procedures, comma-separated")
    medication_history: str = Field(description="Current and recent medications, comma-separated")
    allergy_history: str = Field(description="Known allergies or adverse reactions, comma-separated")
    social_history: str = Field(description="Smoking, alcohol, substance use, living situation")

class ClinicalFindings(BaseModel):
    chief_complaint: str = Field(description="Primary reason for presentation")
    history_of_present_illness: str = Field(description="Detailed chronological description of current illness")
    symptom_onset: str = Field(description="When symptoms started and initial presentation")
    symptom_progression: str = Field(description="How symptoms have changed over time")
    associated_symptoms: str = Field(description="Related symptoms experienced, comma-separated")
    alleviating_factors: str = Field(description="What makes symptoms better, comma-separated")
    aggravating_factors: str = Field(description="What makes symptoms worse, comma-separated")
    impact_on_activities: str = Field(description="Effect on daily activities and quality of life")
    physical_exam_findings: str = Field(description="Physical examination results with vital signs")
    abnormal_findings: str = Field(description="Specific abnormal clinical findings, comma-separated")

class Timeline(BaseModel):
    initial_presentation_date: str = Field(description="Date of first symptom or presentation (format: Month/Year or descriptive)")
    key_clinical_events: str = Field(description="Major events in chronological order with dates")
    diagnostic_workup_timeline: str = Field(description="Sequence of diagnostic tests and dates performed")
    treatment_initiation_date: str = Field(description="When treatment began")
    significant_changes: str = Field(description="Important changes in clinical status over time")
    duration_of_illness: str = Field(description="Total time from onset to current status")

class DiagnosticAssessment(BaseModel):
    laboratory_tests_performed: str = Field(description="Blood tests, CSF analysis, biopsies, etc. with results")
    laboratory_values: str = Field(description="Specific abnormal lab values with reference ranges")
    imaging_studies: str = Field(description="CT, MRI, X-ray, ultrasound, or other imaging with findings")
    imaging_findings: str = Field(description="Specific abnormal imaging findings with measurements")
    pathology_results: str = Field(description="Tissue diagnosis or pathological findings if applicable")
    specialized_testing: str = Field(description="EKG, EEG, genetic testing, immunology panels, etc.")
    diagnostic_criteria_assessment: str = Field(description="Clinical criteria findings without naming the diagnosis")
    diagnostic_challenges: str = Field(description="Difficulties encountered in reaching diagnosis")
    noteworthy_findings_pattern: str = Field(description="Overall pattern of findings without disclosing diagnosis")

class TherapeuticInterventions(BaseModel):
    initial_management: str = Field(description="First-line treatment approach and rationale")
    medications_prescribed: str = Field(description="Medications given with dosage, frequency, and dates")
    dosage_adjustments: str = Field(description="Changes in medication doses over time")
    surgical_interventions: str = Field(description="Any surgical procedures performed with dates and outcomes")
    procedural_interventions: str = Field(description="Non-surgical procedures (catheterization, biopsy, etc)")
    supportive_care: str = Field(description="Supportive measures, monitoring, and nursing care")
    lifestyle_modifications: str = Field(description="Recommended dietary, activity, or behavioral changes")
    rehabilitation_therapy: str = Field(description="Physical, occupational, or speech therapy if applicable")
    adverse_events: str = Field(description="Medication side effects or treatment complications, comma-separated")
    treatment_response: str = Field(description="How patient responded to treatment over time")

class FollowUpAndOutcomes(BaseModel):
    clinical_response_to_treatment: str = Field(description="How symptoms improved or changed with treatment")
    symptom_resolution: str = Field(description="Whether symptoms resolved, improved, or persisted")
    functional_status: str = Field(description="Ability to perform daily activities and return to work/life")
    final_clinical_status: str = Field(description="Current health status and disease state")
    complications_during_course: str = Field(description="Any complications that developed, comma-separated")
    length_of_hospital_stay: str = Field(description="If hospitalized, duration and reason for discharge")
    duration_of_followup: str = Field(description="How long patient was followed up after initial treatment")
    discharge_medications: str = Field(description="Medications at discharge or end of acute treatment")
    followup_schedule: str = Field(description="Planned follow-up appointments and monitoring")
    current_status: str = Field(description="Most recent assessment and current clinical condition")

class Discussion(BaseModel):
    case_significance: str = Field(description="Why this case is clinically important or unusual without naming diagnosis")
    findings_interpretation: str = Field(description="Analysis of clinical findings and their significance")
    diagnostic_approach_discussion: str = Field(description="Analysis of diagnostic strategy and reasoning process")
    treatment_rationale: str = Field(description="Why specific treatments were chosen and their evidence base")
    treatment_effectiveness: str = Field(description="Assessment of treatment response without assuming diagnosis")
    learning_points: str = Field(description="Key clinical lessons and takeaways from this case")
    pathophysiological_insights: str = Field(description="Biological mechanisms highlighted by findings")
    clinical_pearls: str = Field(description="Important clinical observations and patterns to recognize")
    implications_for_practice: str = Field(description="How this case may inform clinical practice and differential diagnosis")
    recommendations: str = Field(description="Recommendations for managing similar presentations")

class PatientPerspective(BaseModel):
    patient_experience: str = Field(description="How patient experienced the symptoms and treatment")
    understanding_of_diagnosis: str = Field(description="Patient's comprehension of their diagnosis")
    treatment_satisfaction: str = Field(description="Patient's satisfaction with care received")
    quality_of_life_impact: str = Field(description="Impact on patient's quality of life and well-being")
    adherence_to_treatment: str = Field(description="How well patient followed treatment recommendations")
    psychosocial_factors: str = Field(description="Emotional, social, or psychological aspects affecting recovery")

class InformedConsent(BaseModel):
    consent_statement: str = Field(description="Statement indicating informed consent was obtained from patient")
    patient_anonymity: str = Field(description="Confirmation that patient identifiers have been removed or anonymized")
    institutional_approval: str = Field(description="IRB approval or institutional review status if applicable")
    ethical_considerations: str = Field(description="Any ethical issues or considerations in the case")

class CaseReportMetadata(BaseModel):
    case_report_title: str = Field(description="Descriptive title describing patient presentation or clinical presentation, without naming the diagnosis")
    keywords: str = Field(description="5-10 clinical keywords describing findings/presentations without diagnosis, comma-separated")
    medical_specialty: str = Field(description="Primary medical specialty relevant to this case")
    date_case_compiled: str = Field(description="Date when case report was compiled")
    case_authors: str = Field(description="Treating physician/medical team names (can be fictional)")
    institution: str = Field(description="Medical institution or hospital where case was managed")
    information_sources: str = Field(description="Sources of medical information used, comma-separated")
    confidence_level: str = Field(description="Confidence in the realism of case data (high, medium)")
    clinical_accuracy: str = Field(description="Note on clinical accuracy and evidence-based information")
    bias_mitigation_note: str = Field(description="Note confirming diagnosis/condition name has been withheld to prevent diagnostic bias")

class SyntheticCaseReport(BaseModel):
    metadata: CaseReportMetadata
    patient_information: PatientInformation
    clinical_findings: ClinicalFindings
    timeline: Timeline
    diagnostic_assessment: DiagnosticAssessment
    therapeutic_interventions: TherapeuticInterventions
    follow_up_and_outcomes: FollowUpAndOutcomes
    discussion: Discussion
    patient_perspective: PatientPerspective
    informed_consent: InformedConsent

# ============================================================================ 
# SYNTHETIC CASE REPORT GENERATOR CLASS
# ============================================================================ 

class SyntheticCaseReportGenerator:
    """Generates synthetic medical case reports."""

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        # Load model name from ModuleConfig

        try:

            module_config = get_module_config("synthetic_case_report")

            model_name = module_config.model_name

        except ValueError:

            # Fallback to default if not registered yet

            model_name = "gemini-1.5-pro"

        

        self.client = MedKitClient(model_name=model_name)

        # Apply verbosity level to logger
        verbosity_levels = {0: "CRITICAL", 1: "ERROR", 2: "WARNING", 3: "INFO", 4: "DEBUG"}
        logger.setLevel(verbosity_levels.get(self.config.verbosity, "WARNING"))

    def generate(self, disease_condition: str, output_path: Optional[Path] = None) -> SyntheticCaseReport:
        logger.info(f"Starting case report generation for: {disease_condition}")

        if not disease_condition or not disease_condition.strip():
            logger.error("Disease condition cannot be empty")
            raise ValueError("Disease condition cannot be empty")

        if output_path is None:
            condition_name = disease_condition.replace(" ", "_").lower()
            output_path = self.config.output_dir / f"{condition_name}_casereport.json"
            logger.debug(f"Generated output path: {output_path}")

        self.config.output_dir.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Output directory ensured: {self.config.output_dir}")

        generation_prompt = (
            f"Create a realistic synthetic medical case report for a patient with {disease_condition}. "
            f"CRITICAL INSTRUCTION: Do NOT explicitly mention the disease or condition name anywhere in the report. "
            f"DO NOT state the diagnosis. Present only the clinical findings, symptoms, test results, and observations. "
            f"The report should be detailed enough that a specialized physician can independently determine the diagnosis "
            f"based solely on the presented clinical data. Include realistic and medically accurate findings consistent with "
            f"this condition, but never explicitly name it in any field."
        )
        logger.debug("Generation prompt prepared")

        try:
            logger.info(f"Generating case report using MedKit client for specialty: {self.config.specialty}")
            result = self.client.generate_text(
                prompt=generation_prompt,
                schema=SyntheticCaseReport,
            )
            logger.info(f"Successfully generated case report for: {disease_condition}")

            if output_path:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, "w") as f:
                    json.dump(result.model_dump(), f, indent=2)
                logger.info(f"Saved case report to: {output_path}")

            self.print_summary(result)
            return result
        except Exception as e:
            logger.error(f"Error generating case report for {disease_condition}: {e}")
            raise

    def generate_multiple(self, disease_condition: str, num_cases: int = 1, output_dir: Optional[Path] = None) -> List[SyntheticCaseReport]:
        logger.info(f"Starting generation of {num_cases} case reports for: {disease_condition}")

        if num_cases < 1:
            logger.error("Number of cases must be at least 1")
            raise ValueError("Number of cases must be at least 1")

        if output_dir is None:
            output_dir = self.config.output_dir
            logger.debug(f"Using default output directory: {output_dir}")

        output_dir.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Output directory ensured: {output_dir}")

        results = []
        for i in range(num_cases):
            condition_name = disease_condition.replace(" ", "_").lower()
            case_filename = f"{condition_name}_casereport.json"
            output_path = output_dir / case_filename
            logger.debug(f"Generating case {i+1}/{num_cases}: {output_path}")

            try:
                case_report = self.generate(disease_condition=disease_condition, output_path=output_path)
                results.append(case_report)
                logger.info(f"Successfully generated case {i+1}/{num_cases}")
                print(f"✓ Generated case {i+1}/{num_cases}")
            except Exception as e:
                logger.error(f"Error generating case {i+1}/{num_cases}: {e}")
                print(f"✗ Error generating case {i+1}: {e}")
                raise

        logger.info(f"Successfully generated all {num_cases} case reports for: {disease_condition}")
        return results

    def print_summary(self, case_report: SyntheticCaseReport):
        print("\n" + "="*70)
        print(f"SYNTHETIC CASE REPORT SUMMARY: {case_report.metadata.case_report_title}")
        print("="*70)
        print(f"  - Specialty: {case_report.metadata.medical_specialty}")
        print(f"  - Patient: {case_report.patient_information.age}-year-old {case_report.patient_information.gender}")
        print(f"  - Chief Complaint: {case_report.clinical_findings.chief_complaint}")
        print(f"\n✓ Generation complete.")

# ============================================================================
# CLI INTERFACE
# ============================================================================

def get_case_report(disease_condition: str, output_path: Optional[str] = None, verbose: bool = False) -> Optional[SyntheticCaseReport]:
    """
    High-level function to generate and optionally save a synthetic case report.
    """
    config = Config(verbose=verbose)
    generator = SyntheticCaseReportGenerator(config=config)
    return generator.generate(disease_condition, output_path=Path(output_path) if output_path else None)

def main():
    """
    CLI entry point for generating synthetic case reports.
    """
    parser = argparse.ArgumentParser(description="Generate synthetic medical case reports.")
    parser.add_argument("-i", "--condition", nargs="?", help="Name of the disease or medical condition")
    parser.add_argument("-n", "--num-cases", type=int, default=1, help="Number of case reports to generate.")
    parser.add_argument("-o", "--output", type=Path, help="Output directory for case reports.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging output.")

    args = parser.parse_args()

    if not args.condition:
        parser.print_help()
        logger.error("Disease condition is required")
        sys.exit(1)

    try:
        config = Config(verbose=args.verbose)
        generator = SyntheticCaseReportGenerator(config=config)
        logger.info(f"CLI invoked with condition: {args.condition}, num_cases: {args.num_cases}")

        output_dir = args.output if args.output else None
        generator.generate_multiple(disease_condition=args.condition, num_cases=args.num_cases, output_dir=output_dir)
        logger.info(f"Successfully generated {args.num_cases} case reports for: {args.condition}")
        print(f"✓ Successfully generated {args.num_cases} case reports!")

    except Exception as e:
        logger.critical(f"Fatal error in CLI: {e}")
        print(f"✗ Failed to generate case reports: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()


    def close(self):
        """Close LMDB storage and release resources."""
        if self.storage:
            try:
                self.storage.close()
                logger.info("LMDB storage closed successfully.")
            except Exception as e:
                logger.error(f"Error closing LMDB storage: {e}")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

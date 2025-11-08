"""
medical_test_info.py - Medical Test Information Generator

Generate comprehensive, evidence-based medical test documentation using structured
data models and the MedKit AI client with schema-aware prompting.

This module creates detailed information about medical tests and diagnostics for
clinicians and patient education.

QUICK START:
    from medical_test_info import MedicalTestInfoGenerator

    # Generate comprehensive test information
    generator = MedicalTestInfoGenerator()
    test_info = generator.generate("blood glucose test")

    # Access different sections
    print(test_info.test_name)
    print(test_info.test_purpose.primary_purpose)
    print(test_info.results_information.normal_range)

    # Save to file
    test_info = generator.generate("complete blood count", output_path="cbc.json")

COMMON USES:
    1. Generate patient education about upcoming tests
    2. Provide clinical reference for test interpretation
    3. Create test preparation instructions
    4. Understand normal and abnormal values
    5. Support clinical decision making
    6. Create test ordering guidance for clinicians

COVERAGE AREAS:
    - Test identification and names
    - Purpose and indications
    - When tests are ordered
    - Preparation requirements
    - Sample collection methods
    - Test procedures and techniques
    - Normal and abnormal values
    - Clinical interpretation
    - Complications and risks
    - Cost and availability
"""

import json
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from pydantic import BaseModel, Field
from typing import Optional, List

from medkit.utils.logging_config import setup_logger
from medkit.core.medkit_client import MedKitClient
from medkit.core.module_config import get_module_config

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
    """Configuration for the medical test info generator."""
    output_dir: Path = field(default_factory=lambda: Path("outputs"))
    enable_cache: bool = True
    log_file: Path = field(default_factory=lambda: Path(__file__).parent / "logs" / f"{Path(__file__).stem}.log")
    verbosity: int = 2  # 0=CRITICAL, 1=ERROR, 2=WARNING (default), 3=INFO, 4=DEBUG

    def __post_init__(self):
        """Set default db_path if not provided, then validate."""
        if self.db_path is None:
            self.db_path = str(
                Path(__file__).parent.parent / "storage" / "medical_test_info.lmdb"
            )
        # Call parent validation
        super().__post_init__()
# ============================================================================ 
# PYDANTIC MODELS FOR TEST INFORMATION STRUCTURE
# ============================================================================ 

class TestPurpose(BaseModel):
    primary_purpose: str = Field(description="Main reason this test is performed.")
    diagnostic_uses: str = Field(description="Specific conditions or diseases this test helps diagnose, comma-separated.")
    monitoring_uses: str = Field(description="Conditions this test helps monitor over time, comma-separated.")
    screening_uses: str = Field(description="Who should get this test as preventive screening.")

class TestIndications(BaseModel):
    when_ordered: str = Field(description="Clinical situations when this test is typically ordered, comma-separated.")
    symptoms_prompting_test: str = Field(description="Symptoms that lead doctors to order this test, comma-separated.")
    risk_factors_requiring_test: str = Field(description="Risk factors that make this test necessary, comma-separated.")

class PreparationRequirements(BaseModel):
    fasting_required: str = Field(description="Whether fasting is needed and for how long with specific hours.")
    medication_adjustments: str = Field(description="Medications to stop or adjust before test with specific washout periods in days/weeks, comma-separated.")
    dietary_restrictions: str = Field(description="Foods or drinks to avoid before test with specific timeframes, comma-separated.")
    timing_considerations: str = Field(description="Best time of day (with specific hours) or menstrual cycle phase (with specific days) for test.")
    items_to_bring: str = Field(description="What to bring to the test appointment, comma-separated.")
    activity_restrictions: str = Field(description="Exercise, physical activity, or stress restrictions before test with specific duration.")

class SpecimenInformation(BaseModel):
    sample_type: str = Field(description="Type of sample required (blood, urine, tissue, saliva, etc), comma-separated if multiple.")
    sample_volume: str = Field(description="Amount of sample needed (e.g., 5ml blood, mid-stream urine).")
    collection_method: str = Field(description="How the sample is collected (venipuncture, clean-catch, swab, biopsy).")
    collection_supplies: str = Field(description="Special tubes, containers, or supplies needed, comma-separated.")
    sample_handling: str = Field(description="Storage and transport requirements (refrigerate, room temp, light-protected).")
    sample_stability: str = Field(description="How long sample remains valid for testing.")
    rejection_criteria: str = Field(description="Conditions that make sample unusable (hemolyzed, clotted, insufficient volume), comma-separated.")

class TestProcedure(BaseModel):
    procedure_type: str = Field(description="Type of test (blood draw, imaging, biopsy, etc).")
    step_by_step_process: str = Field(description="Detailed steps of how the test is performed, numbered or comma-separated.")
    duration: str = Field(description="How long the test takes from start to finish.")
    location: str = Field(description="Where the test is typically performed (hospital, clinic, lab).")
    equipment_used: str = Field(description="Medical equipment and instruments used, comma-separated.")

class DiscomfortAndRisks(BaseModel):
    discomfort_level: str = Field(description="Expected level of pain or discomfort (none, mild, moderate, severe).")
    common_sensations: str = Field(description="What patients typically feel during test, comma-separated.")
    common_side_effects: str = Field(description="Temporary side effects that are normal, comma-separated.")
    serious_risks: str = Field(description="Rare but serious complications to be aware of, comma-separated.")
    contraindications: str = Field(description="Conditions that make this test unsafe, comma-separated.")

class InterferingFactors(BaseModel):
    medications_affecting_results: str = Field(description="Medications that can alter test results with mechanism, comma-separated.")
    supplements_herbs: str = Field(description="Dietary supplements and herbs that interfere, comma-separated. MUST include biotin for immunoassays.")
    foods_beverages: str = Field(description="Foods or drinks that affect results beyond standard fasting, comma-separated.")
    substances_activities: str = Field(description="Smoking, alcohol, exercise, stress that impact results, comma-separated.")
    medical_conditions_interfering: str = Field(description="Diseases or conditions that cause false results, comma-separated.")
    assay_interferences: str = Field(description="Technical interferences: biotin, hemolysis, icterus, lipemia (HIL), hook effect/prozone, heterophile antibodies, comma-separated.")
    pre_analytical_errors: str = Field(description="Common specimen collection and handling errors that affect results, comma-separated.")

class ResultsInformation(BaseModel):
    turnaround_time: str = Field(description="How long until results are available.")
    result_format: str = Field(description="How results are reported (numerical, narrative, images).")
    normal_range: str = Field(description="Normal or reference values for this test with specific numerical ranges.")
    abnormal_result_meanings: str = Field(description="What different abnormal results indicate, comma-separated.")
    factors_affecting_results: str = Field(description="Things that can cause false positives or negatives, comma-separated.")
    critical_values: str = Field(description="Panic values requiring immediate physician notification with specific thresholds.")
    result_reporting_time: str = Field(description="Typical time for critical vs routine results notification.")

class AgeSpecificInformation(BaseModel):
    pediatric_considerations: str = Field(description="Special considerations for infants and children including age-specific reference ranges.")
    pediatric_reference_ranges: str = Field(description="Normal values by specific age groups with numerical ranges (e.g., 0-1 month, 1-12 months, 1-5 years, 6-12 years, 13-18 years).")
    geriatric_considerations: str = Field(description="Special considerations and modified reference ranges for elderly patients (65+ years).")
    pregnancy_specific: str = Field(description="How pregnancy affects test and interpretation. MUST include trimester-specific numerical ranges (1st, 2nd, 3rd trimester with values).")
    breastfeeding_considerations: str = Field(description="Safety and interpretation for breastfeeding mothers.")
    sex_specific_differences: str = Field(description="Reference ranges and considerations for males vs females with specific values.")

class Interpretation(BaseModel):
    what_normal_means: str = Field(description="Clinical significance of normal results.")
    what_abnormal_means: str = Field(description="Clinical significance of abnormal results with specific clinical decision thresholds.")
    false_positive_rate: Optional[str] = Field(description="How often test incorrectly shows positive with percentage and clinical context.")
    false_negative_rate: Optional[str] = Field(description="How often test misses actual condition with percentage and clinical context.")
    confirmatory_tests: str = Field(description="Additional tests needed to confirm abnormal results, comma-separated.")
    positive_predictive_value: Optional[str] = Field(description="Probability that positive result truly indicates disease, stratified by prevalence/population.")
    negative_predictive_value: Optional[str] = Field(description="Probability that negative result truly rules out disease, stratified by prevalence/population.")
    likelihood_ratios: Optional[str] = Field(description="Positive and negative likelihood ratios with numerical values.")
    clinical_decision_thresholds: str = Field(description="Specific numerical cutoffs for clinical actions (observation, further testing, treatment) with values.")

class FollowUpActions(BaseModel):
    normal_result_actions: str = Field(description="What happens if test is normal, comma-separated.")
    abnormal_result_actions: str = Field(description="Next steps if test is abnormal, comma-separated.")
    repeat_testing_schedule: str = Field(description="When test should be repeated with specific timeframes.")
    monitoring_criteria: str = Field(description="For serial monitoring: established criteria for disease progression, response, or recurrence (e.g., doubling time, percentage change thresholds, specific organizational criteria like GOG, RECIST).")
    baseline_requirements: str = Field(description="Requirements for establishing baseline values for future comparison.")

class ConsentAndRights(BaseModel):
    informed_consent_required: str = Field(description="Whether written consent is required and what it covers.")
    right_to_refuse: str = Field(description="Patient's right to decline test and implications.")
    results_access: str = Field(description="Who can access results (patient, family, providers) and timing.")
    privacy_considerations: str = Field(description="HIPAA protections and confidentiality measures.")
    genetic_privacy: str = Field(description="Special privacy considerations for genetic/hereditary information.")

class CostAndInsurance(BaseModel):
    typical_cost_range: str = Field(description="General cost range without insurance.")
    insurance_coverage: str = Field(description="How typically covered by insurance.")
    prior_authorization: str = Field(description="Whether insurance pre-approval is needed.")
    medicare_coverage: str = Field(description="Medicare coverage specifics including frequency limits.")
    medicaid_coverage: str = Field(description="Medicaid coverage information.")
    financial_assistance_programs: str = Field(description="Programs to help with costs, comma-separated.")
    cpt_codes: Optional[str] = Field(description="Current Procedural Terminology codes for billing.")

class Alternatives(BaseModel):
    alternative_tests: str = Field(description="Other tests that provide similar information, comma-separated.")
    advantages_over_alternatives: str = Field(description="Why this test may be preferred, comma-separated.")
    complementary_tests: str = Field(description="Tests often done alongside this one, comma-separated.")
    when_alternatives_preferred: str = Field(description="Clinical scenarios where other tests are better, comma-separated.")

class TechnicalDetails(BaseModel):
    testing_methodology: str = Field(description="Scientific principle and technology used.")
    measurement_units: str = Field(description="Units results are reported in.")
    detection_limit: str = Field(description="Minimum level test can detect with numerical value.")
    analytical_range: str = Field(description="Range of values test can accurately measure with numerical bounds.")
    sensitivity: str = Field(description="Ability to correctly identify those with condition (true positive rate) with percentage.")
    specificity: str = Field(description="Ability to correctly identify those without condition (true negative rate) with percentage.")
    clia_complexity: Optional[str] = Field(description="CLIA complexity level (waived, moderate, high complexity).")
    coefficient_of_variation: Optional[str] = Field(description="Analytical precision (CV%) - typically intra-assay and inter-assay variation.")
    biological_variation: Optional[str] = Field(description="Expected within-person biological variation percentage.")
    assay_standardization: str = Field(description="Whether different manufacturers/platforms give comparable results. Note if serial testing requires same assay platform.")
    fda_status: str = Field(description="FDA clearance/approval status vs laboratory-developed test (LDT).")

class TestLimitations(BaseModel):
    when_test_unreliable: str = Field(description="Specific conditions making test results unreliable, comma-separated.")
    population_specific_limitations: str = Field(description="Limitations for pregnancy, children, elderly, ethnic groups, comma-separated.")
    cannot_detect: str = Field(description="What this test cannot identify or measure, comma-separated.")
    requires_clinical_correlation: str = Field(description="Why test must be interpreted with symptoms and history.")
    known_false_results_causes: str = Field(description="Common causes of incorrect results, comma-separated.")

class SpecialPopulations(BaseModel):
    immunocompromised_patients: str = Field(description="Special considerations for patients with weakened immune systems.")
    patients_with_disabilities: str = Field(description="Accessibility accommodations and procedural modifications.")
    ethnic_racial_variations: str = Field(description="Known differences in reference ranges or disease prevalence by ethnicity.")
    language_cultural_considerations: str = Field(description="Communication and cultural sensitivity needs.")
    obese_patients: str = Field(description="Technical challenges or modified procedures for obese patients.")

class MedicalTestInfo(BaseModel):
    """Comprehensive model for medical test information."""
    # Basic Information
    test_name: str = Field(description="Official name of the test")
    alternative_names: str = Field(description="Other names for this test, comma-separated")
    test_category: str = Field(description="Category (blood test, imaging, etc)")
    medical_specialty: str = Field(description="Primary medical specialties, comma-separated")
    
    # Purpose and Indications
    test_purpose: TestPurpose
    indications: TestIndications
    
    # Test Process
    preparation: PreparationRequirements
    specimen_information: SpecimenInformation
    procedure: TestProcedure
    discomfort_and_risks: DiscomfortAndRisks
    
    # Results
    interfering_factors: InterferingFactors
    results_information: ResultsInformation
    interpretation: Interpretation
    follow_up_actions: FollowUpActions
    
    # Population-Specific
    age_specific_information: AgeSpecificInformation
    special_populations: SpecialPopulations
    
    # Alternatives
    alternatives: Alternatives
    
    # Technical Information
    technical_details: TechnicalDetails
    
    # Evidence and Guidelines
    evidence_summary: str = Field(description="Summary of major guidelines and evidence quality")
    test_limitations: TestLimitations
    
    # Practical Information
    cost_and_insurance: CostAndInsurance
    consent_and_rights: ConsentAndRights
    
    # Educational Content
    plain_language_explanation: str = Field(description="Simple explanation for patients")
    key_takeaways: str = Field(description="3-5 most important points, comma-separated")
    common_misconceptions: str = Field(description="Common myths about this test, comma-separated")

# ============================================================================ 
# MEDICAL TEST INFO GENERATOR CLASS
# ============================================================================ 

class MedicalTestInfoGenerator:
    """Generate comprehensive information for medical tests."""

    def __init__(self, config: Optional[Config] = None):
        """Initialize the generator with a configuration."""
        self.config = config or Config()
        # Load model name from ModuleConfig

        try:

            module_config = get_module_config("medical_test_info")

            model_name = module_config.model_name

        except ValueError:

            # Fallback to default if not registered yet

            model_name = "gemini-1.5-flash"

        

        self.client = MedKitClient(model_name=model_name)
        self.test_name: Optional[str] = None
        self.output_path: Optional[Path] = None

        # Apply verbosity level to logger
        verbosity_levels = {
            0: "CRITICAL",
            1: "ERROR",
            2: "WARNING",
            3: "INFO",
            4: "DEBUG"
        }
        log_level = verbosity_levels.get(self.config.verbosity, "WARNING")
        logger.setLevel(log_level)

    def generate_test_info(self, test_name: str) -> MedicalTestInfo:
        """
        Generate the core medical test information.

        Args:
            test_name: The name of the medical test.

        Returns:
            A MedicalTestInfo object with the generated data.
        """
        logger.info(f"Generating medical test information for: {test_name}")
        try:
            prompt = f"""Generate comprehensive medical test information for: {test_name}

Include detailed information about:
1. Test name and alternative names
2. Purpose and clinical use
3. Test indications and when it is ordered
4. Sample requirements and collection procedures
5. Test methodology and technology
6. Normal reference ranges and result interpretation
7. Preparatory requirements and restrictions
8. Risks, benefits, and limitations
9. Cost and availability information
10. Results interpretation and follow-up actions

Provide accurate, evidence-based medical test information."""

            result = self.client.generate_text(prompt, schema=MedicalTestInfo)
            logger.info(f"Successfully generated medical test information for: {test_name}")
            return result
        except Exception as e:
            logger.error(f"Error generating medical test information for {test_name}: {e}")
            raise

    def generate(self, test_name: str, output_path: Optional[Path] = None) -> MedicalTestInfo:
        """
        Generate and save comprehensive medical test information.

        Args:
            test_name: Name of the medical test.
            output_path: Optional path to save the JSON output.

        Returns:
            The generated MedicalTestInfo object.

        Raises:
            ValueError: If test_name is empty.
        """
        if not test_name or not test_name.strip():
            logger.error("Test name cannot be empty")
            raise ValueError("Test name cannot be empty")

        self.test_name = test_name

        if output_path is None:
            output_path = self.config.output_dir / f"{test_name.lower().replace(' ', '_')}_info.json"

        self.output_path = output_path

        logger.info(f"Starting medical test information generation for: {test_name}")

        try:
            test_info = self.generate_test_info(test_name)
            self.save(test_info, self.output_path)
            logger.info(f"Successfully generated all test information for: {test_name}")
            self.print_summary(test_info)
            return test_info
        except Exception as e:
            logger.error(f"Failed to generate test information for {test_name}: {e}")
            raise

    def save(self, test_info: MedicalTestInfo, output_path: Path) -> Path:
        """
        Save the generated test information to a JSON file.

        Args:
            test_info: The MedicalTestInfo object to save.
            output_path: The path to save the file to.

        Returns:
            The path to the saved file.
        """
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                json.dump(test_info.model_dump(), f, indent=2)
            logger.info(f"Saved test information to: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error saving test information to {output_path}: {e}")
            raise

    def print_summary(self, test_info: MedicalTestInfo) -> None:
        """
        Print a summary of the generated test information.

        Args:
            test_info: The MedicalTestInfo object.
        """
        print("\n" + "="*70)
        print(f"MEDICAL TEST INFORMATION SUMMARY: {test_info.test_name}")
        print("="*70)
        print(f"  - Category: {test_info.test_category}")
        print(f"  - Specialty: {test_info.medical_specialty}")
        print(f"  - Purpose: {test_info.test_purpose.primary_purpose}")
        print(f"  - Sample Type: {test_info.specimen_information.sample_type}")
        print(f"\n✓ Generation complete. Saved to {self.output_path}")

def get_medical_test_info(test_name: str, output_path: Optional[Path] = None) -> MedicalTestInfo:
    """
    High-level function to generate and optionally save test information.
    """
    generator = MedicalTestInfoGenerator()
    return generator.generate(test_name, output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate comprehensive information for a medical test.")
    parser.add_argument("-i", "--test", type=str, required=True, help="The name of the medical test to generate information for.")
    parser.add_argument("-o", "--output", type=str, help="Optional: The path to save the output JSON file.")
    
    args = parser.parse_args()
    
    generator = MedicalTestInfoGenerator()
    
    output_file_path = Path(args.output) if args.output else None
    
    generator.generate(test_name=args.test, output_path=output_file_path)

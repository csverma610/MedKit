"""medical_implant - Generate comprehensive medical implant documentation.

This module generates detailed, evidence-based information about medical implants
(orthopedic, cardiovascular, neurological, etc.). It provides complete implant
documentation including indications, materials, installation procedures, outcomes,
complications, and maintenance using the MedKit AI client with structured Pydantic schemas.

QUICK START:
    Generate implant information:

    >>> from medical_implant import MedicalImplantInfoGenerator
    >>> generator = MedicalImplantInfoGenerator()
    >>> result = generator.generate("Hip Replacement")
    >>> print(result.metadata.implant_name)
    Hip Replacement

    Or use the CLI:

    $ python medical_implant.py -i "Hip Replacement"
    $ python medical_implant.py -i "Pacemaker" -o custom_output.json

COMMON USES:
    1. Patient education - helping patients understand implant details
    2. Informed consent - providing comprehensive pre-implant information
    3. Clinical reference - detailed implant guidelines for healthcare teams
    4. Surgical planning - implant specifications, installation techniques, compatibility
    5. Insurance and billing - cost information, billing codes, coverage details
    6. Follow-up care - long-term monitoring and management requirements

KEY FEATURES AND COVERAGE AREAS:
    - Implant identification: official names, types, manufacturers, models
    - Purpose and indications: clinical reasons for implant, what it treats
    - Implant materials: composition, biocompatibility, allergic considerations
    - Installation procedure: surgical approach, duration, anesthesia type
    - Recovery and healing: timeline, restrictions, pain management
    - Functionality: how the implant works, expected performance, adjustments
    - Complications and risks: infection, rejection, displacement, failure rates
    - Lifespan and longevity: expected durability, revision rates, replacement timeline
    - Imaging and testing: MRI/CT compatibility, monitoring requirements, diagnostic tools
    - Activity restrictions: permanent limitations, sports, lifting, activities
    - Maintenance and care: cleaning, inspections, replacements, upgrades
    - Cost and insurance: pricing, coverage, financial assistance programs
    - Alternatives: other implants, non-implant options, comparative advantages
    - Patient education: plain language explanations, daily living with implant, misconceptions
"""

import json
import sys
import argparse
import logging
from pathlib import Path
from dataclasses import dataclass, field
from pydantic import BaseModel, Field
from typing import Optional

from medkit.core.medkit_client import MedKitClient
from medkit.core.module_config import get_module_config

from medkit.utils.logging_config import setup_logger

import hashlib
from medkit.utils.lmdb_storage import LMDBStorage, LMDBConfig
from medkit.utils.storage_config import StorageConfig

# Configure logging
logger = setup_logger(__name__)

# Suppress logger output by default (can be overridden via set_verbose)
logger.setLevel(logging.WARNING)

# ============================================================================
# CONFIGURATION
# ============================================================================

@dataclass
class Config(StorageConfig):
    """Configuration for the medical implant info generator."""
    output_dir: Path = field(default_factory=lambda: Path("outputs"))
    log_file: Path = field(default_factory=lambda: Path(__file__).parent / "logs" / f"{Path(__file__).stem}.log")
    specialty: str = "Surgery/Implantology"
    verbosity: int = 2  # Verbosity level: 0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG

    def __post_init__(self):
        """Set default db_path if not provided, then validate."""
        if self.db_path is None:
            self.db_path = str(
                Path(__file__).parent.parent / "storage" / "medical_implant.lmdb"
            )
        # Call parent validation
        super().__post_init__()
# ============================================================================
# PYDANTIC MODELS FOR IMPLANT INFORMATION STRUCTURE
# ============================================================================

class ImplantMetadata(BaseModel):
    """Basic information about the implant."""
    implant_name: str = Field(description="Official name of the implant")
    alternative_names: str = Field(description="Other names or aliases for this implant, comma-separated")
    implant_type: str = Field(description="Type of implant (orthopedic, cardiovascular, dental, neurological, etc)")
    medical_specialty: str = Field(description="Primary medical specialties involved, comma-separated")
    common_manufacturers: str = Field(description="Major manufacturers of this implant type, comma-separated")

class ImplantPurpose(BaseModel):
    primary_purpose: str = Field(description="Main reason this implant is used.")
    therapeutic_uses: str = Field(description="Specific conditions this implant treats, comma-separated.")
    functional_benefits: str = Field(description="Functional improvements provided by this implant, comma-separated.")
    quality_of_life_improvements: str = Field(description="How this implant improves daily functioning and quality of life.")

class ImplantIndications(BaseModel):
    when_recommended: str = Field(description="Clinical situations when this implant is typically recommended, comma-separated.")
    conditions_treated: str = Field(description="Medical conditions this implant addresses, comma-separated.")
    symptom_relief: str = Field(description="Symptoms that lead doctors to recommend this implant, comma-separated.")
    contraindications: str = Field(description="Conditions that make this implant unsafe or inappropriate, comma-separated.")
    age_considerations: str = Field(description="Age-related factors affecting implant suitability.")

class ImplantMaterials(BaseModel):
    primary_materials: str = Field(description="Main materials used in construction, comma-separated.")
    material_properties: str = Field(description="Key properties of materials (strength, flexibility, durability), comma-separated.")
    biocompatibility: str = Field(description="Information about biocompatibility and tissue integration.")
    allergic_considerations: str = Field(description="Potential allergies or sensitivities to materials, comma-separated.")
    corrosion_resistance: str = Field(description="Information about corrosion and long-term material integrity.")

class InstallationProcedure(BaseModel):
    surgical_approach: str = Field(description="Type of surgery needed (open, minimally invasive, endoscopic, etc).")
    surgical_steps: str = Field(description="Detailed steps of the installation procedure, numbered or comma-separated.")
    anesthesia_type: str = Field(description="Type of anesthesia used (general, local, regional, etc).")
    procedure_duration: str = Field(description="How long the installation procedure takes.")
    hospital_requirements: str = Field(description="Hospital or facility requirements for installation.")
    recovery_location: str = Field(description="Where recovery takes place (hospital, outpatient, home).")
    hospitalization_duration: str = Field(description="Length of hospital stay if required.")

class FunctionalityAndPerformance(BaseModel):
    how_it_works: str = Field(description="Explanation of how the implant functions in the body.")
    expected_performance: str = Field(description="Expected functional performance and capabilities.")
    adjustment_requirements: str = Field(description="Whether adjustments or calibration are needed after installation.")
    lifespan: str = Field(description="Expected lifespan or durability of the implant.")
    failure_modes: str = Field(description="Ways the implant might fail or wear out, comma-separated.")

class RecoveryAndHealing(BaseModel):
    immediate_recovery: str = Field(description="What to expect in the immediate post-operative period.")
    healing_timeline: str = Field(description="Typical healing milestones and duration until full integration.")
    pain_management: str = Field(description="How pain is managed during recovery, comma-separated.")
    activity_restrictions: str = Field(description="Physical limitations during healing period, comma-separated.")
    return_to_normal_activities: str = Field(description="Timeline for returning to normal activities.")
    wound_care: str = Field(description="Instructions for wound care and monitoring.")
    warning_signs: str = Field(description="Symptoms requiring immediate medical attention, comma-separated.")

class ComplicationsAndRisks(BaseModel):
    infection_risk: str = Field(description="Risk of surgical site or implant infection.")
    rejection_risk: str = Field(description="Risk of implant rejection or adverse reactions.")
    mechanical_failure: str = Field(description="Risk of implant malfunction or mechanical failure.")
    common_complications: str = Field(description="Common complications and their frequency, comma-separated.")
    serious_complications: str = Field(description="Rare but serious complications, comma-separated.")
    revision_rates: str = Field(description="Percentage needing revision surgery and timeline.")
    mortality_risk: Optional[str] = Field(description="Risk of death from implant or installation if applicable.")

class ImagingAndMonitoring(BaseModel):
    mri_compatibility: str = Field(description="Whether MRI imaging is safe or requires precautions.")
    ct_imaging: str = Field(description="CT scan compatibility and any necessary modifications.")
    x_ray_considerations: str = Field(description="X-ray imaging considerations and artifact effects.")
    monitoring_frequency: str = Field(description="How often implant needs to be monitored or checked.")
    diagnostic_tests: str = Field(description="Tests used to assess implant function, comma-separated.")
    remote_monitoring: Optional[str] = Field(description="If applicable, remote monitoring capabilities and requirements.")

class ActivityRestrictions(BaseModel):
    permanent_restrictions: str = Field(description="Activities permanently limited or prohibited, comma-separated.")
    temporary_restrictions: str = Field(description="Activities restricted during healing period, comma-separated.")
    sports_and_exercise: str = Field(description="Guidelines for sports, exercise, and physical activity.")
    lifting_and_weight_bearing: str = Field(description="Weight lifting and weight-bearing restrictions.")
    occupational_considerations: str = Field(description="Work-related considerations and limitations.")
    travel_considerations: str = Field(description="Special considerations for air travel or international travel.")

class MaintenanceAndCare(BaseModel):
    daily_care: str = Field(description="Daily care and hygiene requirements, comma-separated.")
    periodic_inspections: str = Field(description="Required inspections and their frequency.")
    battery_replacement: Optional[str] = Field(description="If applicable, battery replacement schedule and procedure.")
    component_replacement: str = Field(description="Components that need replacement and typical intervals.")
    maintenance_costs: str = Field(description="Typical costs of maintenance and replacements.")
    long_term_management: str = Field(description="Long-term management strategy and follow-up care.")

class OutcomesAndEffectiveness(BaseModel):
    success_rate: str = Field(description="Percentage of successful implant placements and functionality.")
    functional_outcomes: str = Field(description="Typical functional improvements achieved, comma-separated.")
    pain_relief: str = Field(description="Expected pain relief or improvement timeline.")
    mobility_improvement: str = Field(description="Expected improvements in mobility or physical function.")
    longevity_data: str = Field(description="Data on implant survival rates at 5, 10, 15+ years.")
    patient_satisfaction: str = Field(description="Typical patient satisfaction rates and outcomes.")
    factors_affecting_outcomes: str = Field(description="Factors influencing success (age, health, compliance), comma-separated.")

class FollowUpCare(BaseModel):
    follow_up_schedule: str = Field(description="Recommended follow-up appointments and their frequency.")
    post_operative_visits: str = Field(description="Specific post-operative visit milestones and expectations.")
    long_term_monitoring: str = Field(description="Long-term monitoring requirements and intervals.")
    provider_specialists: str = Field(description="Healthcare providers involved in ongoing care, comma-separated.")
    medications_after: str = Field(description="Medications typically prescribed after implantation, comma-separated.")
    complications_monitoring: str = Field(description="How complications are monitored and managed.")

class CostAndInsurance(BaseModel):
    implant_cost: str = Field(description="Typical cost of the implant itself.")
    surgical_costs: str = Field(description="Typical costs for the surgical procedure.")
    total_cost_range: str = Field(description="General total cost range without insurance.")
    insurance_coverage: str = Field(description="How typically covered by insurance.")
    prior_authorization: str = Field(description="Whether insurance pre-approval is needed.")
    medicare_coverage: str = Field(description="Medicare coverage specifics.")
    medicaid_coverage: str = Field(description="Medicaid coverage information.")
    financial_assistance_programs: str = Field(description="Programs to help with costs, comma-separated.")
    cpt_codes: Optional[str] = Field(description="Current Procedural Terminology codes for billing.")

class Alternatives(BaseModel):
    alternative_implants: str = Field(description="Other implant options for similar purposes, comma-separated.")
    non_implant_alternatives: str = Field(description="Non-surgical or non-implant treatment options, comma-separated.")
    advantages_over_alternatives: str = Field(description="Why this implant may be preferred, comma-separated.")
    when_alternatives_preferred: str = Field(description="Situations where other treatments might be better.")

class ImplantLimitations(BaseModel):
    not_suitable_for: str = Field(description="Patient populations for whom implant is not appropriate, comma-separated.")
    anatomical_limitations: str = Field(description="Anatomical factors that may limit implant success, comma-separated.")
    health_condition_limitations: str = Field(description="Medical conditions that preclude implantation, comma-separated.")
    age_limitations: str = Field(description="Age-related considerations or restrictions.")

class ImplantEducation(BaseModel):
    """Patient education and communication content."""
    plain_language_explanation: str = Field(description="Simple explanation of the implant and its purpose for patients")
    daily_living_tips: str = Field(description="Tips for daily living with the implant, comma-separated")
    common_misconceptions: str = Field(description="Common myths or misconceptions about this implant, comma-separated")
    key_takeaways: str = Field(description="3-5 most important points for patients, comma-separated")

class ImplantEvidence(BaseModel):
    """Evidence-based information and clinical guidelines."""
    evidence_summary: str = Field(description="Summary of major clinical guidelines and evidence quality")
    clinical_trials: str = Field(description="Information about relevant clinical trials and outcomes")
    implant_limitations: ImplantLimitations

class ImplantInfo(BaseModel):
    """
    Comprehensive medical implant information.
    """
    # Core identification
    metadata: ImplantMetadata

    # Clinical purpose and application
    purpose: ImplantPurpose
    indications: ImplantIndications

    # Physical characteristics
    materials: ImplantMaterials

    # Installation and integration
    installation: InstallationProcedure

    # Functionality
    functionality: FunctionalityAndPerformance

    # Recovery phase
    recovery: RecoveryAndHealing
    outcomes: OutcomesAndEffectiveness

    # Clinical considerations
    complications: ComplicationsAndRisks
    imaging: ImagingAndMonitoring

    # Lifestyle considerations
    activity_restrictions: ActivityRestrictions
    maintenance: MaintenanceAndCare

    # Post-operative phase
    follow_up: FollowUpCare

    # Alternative treatment options
    alternatives: Alternatives

    # Advanced clinical information
    evidence: ImplantEvidence

    # Financial and insurance
    cost_and_insurance: CostAndInsurance

    # Patient communication
    education: ImplantEducation

# ============================================================================
# MEDICAL IMPLANT INFO GENERATOR CLASS
# ============================================================================

class MedicalImplantInfoGenerator:
    """Generate comprehensive information for medical implants."""

    def __init__(self, config: Optional[Config] = None):
        """Initialize the generator with a configuration."""
        self.config = config or Config()
        # Load model name from ModuleConfig

        try:

            module_config = get_module_config("medical_implant")

            model_name = module_config.model_name

        except ValueError:

            # Fallback to default if not registered yet

            model_name = "gemini-1.5-flash"

        

        self.client = MedKitClient(model_name=model_name)
        self.implant_name: Optional[str] = None
        self.output_path: Optional[Path] = None

        # Apply verbosity level to logger
        verbosity_levels = {0: "CRITICAL", 1: "ERROR", 2: "WARNING", 3: "INFO", 4: "DEBUG"}
        logger.setLevel(verbosity_levels.get(self.config.verbosity, "WARNING"))

    def generate(self, implant_name: str, output_path: Optional[Path] = None) -> ImplantInfo:
        """
        Generate and save comprehensive medical implant information.

        Args:
            implant_name: Name of the medical implant.
            output_path: Optional path to save the JSON output.

        Returns:
            The generated ImplantInfo object.

        Raises:
            ValueError: If implant_name is empty.
        """
        if not implant_name or not implant_name.strip():
            raise ValueError("Implant name cannot be empty")

        self.implant_name = implant_name

        if output_path is None:
            output_path = self.config.output_dir / f"{implant_name.lower().replace(' ', '_')}_info.json"

        self.output_path = output_path

        logger.info(f"Starting medical implant information generation for: {implant_name}")

        implant_info = self._generate_info()

        self.save(implant_info, self.output_path)
        self.print_summary(implant_info)

        return implant_info

    def _generate_info(self) -> ImplantInfo:
        """Generates the implant information."""
        sys_prompt = f"""You are an expert medical documentation specialist with deep knowledge of medical implants in {self.config.specialty}.

Generate comprehensive, evidence-based implant information ensuring all information is:
- Medically accurate and aligned with current guidelines
- Detailed enough for both patient education and clinical reference
- Supported by authoritative medical sources where applicable
- Clearly distinguished between expected outcomes and rare complications
- Includes statistical data when available (success rates, complication rates, longevity data)
- Addresses both the technical and patient-facing aspects of the implant

Return structured JSON matching the exact schema provided, with all required fields populated."""

        result = self.client.generate_text(
            prompt=f"Generate complete, evidence-based information for the medical implant: {self.implant_name}",
            schema=ImplantInfo,
            sys_prompt=sys_prompt,
        )
        return result

    def save(self, implant_info: ImplantInfo, output_path: Path) -> Path:
        """
        Save the generated implant information to a JSON file.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(implant_info.model_dump(), f, indent=2)

        logger.info(f"✓ Implant information saved to {output_path}")
        return output_path

    def print_summary(self, implant_info: ImplantInfo) -> None:
        """
        Print a summary of the generated implant information.
        """
        if not self.config.verbose:
            return
        print("\n" + "="*70)
        print(f"IMPLANT INFORMATION SUMMARY: {implant_info.metadata.implant_name}")
        print("="*70)
        print(f"  - Type: {implant_info.metadata.implant_type}")
        print(f"  - Specialty: {implant_info.metadata.medical_specialty}")
        print(f"  - Purpose: {implant_info.purpose.primary_purpose}")
        print(f"  - Expected Lifespan: {implant_info.functionality.lifespan}")
        print(f"\n✓ Generation complete. Saved to {self.output_path}")

def get_implant_info(implant_name: str, output_path: Optional[Path] = None, verbose: bool = True) -> ImplantInfo:
    """
    High-level function to generate and optionally save implant information.
    """
    config = Config(verbose=verbose)
    generator = MedicalImplantInfoGenerator(config=config)
    return generator.generate(implant_name, output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate comprehensive information for a medical implant.")
    parser.add_argument("-i", "--implant", type=str, required=True, help="The name of the medical implant to generate information for.")
    parser.add_argument("-o", "--output", type=str, help="Optional: The path to save the output JSON file.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show verbose console output.")

    args = parser.parse_args()
    get_implant_info(args.implant, args.output, args.verbose)


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

"""
surgery_info - Generate comprehensive surgical procedure documentation.

This module generates detailed, evidence-based surgical procedure documentation using
structured Pydantic data models and the MedKit AI client with schema-aware prompting.
Content covers the complete surgical journey from indications through recovery and includes
clinical rationale, patient education, and evidence-based guidelines for each aspect.

QUICK START:
    Get comprehensive information about a surgical procedure:

    >>> from surgery_info import SurgeryInfoGenerator
    >>> generator = SurgeryInfoGenerator()
    >>> result = generator.generate("Knee Replacement")
    >>> print(f"Generated surgical information for {result.metadata.surgery_name}")

    With custom output path:

    >>> result = generator.generate("Coronary Artery Bypass", output_path="cardiac_surgery.json")

    Or use the CLI:

    $ python surgery_info.py "Knee Replacement"
    $ python surgery_info.py "Coronary Artery Bypass" -o cardiac_procedures/

COMMON USES:
    1. Patient education - providing comprehensive, understandable surgical information before procedures
    2. Clinical reference - quick access to surgical indications, contraindications, and techniques
    3. Surgical planning - detailed pre-operative assessment and risk stratification guidance
    4. Medical training - resident and student learning of surgical procedures and techniques
    5. Research compilation - gathering evidence-based surgical practice guidelines and outcomes data

KEY FEATURES AND COVERAGE AREAS:
    - Metadata and procedure identification with CPT/ICD codes and category classification
    - Indications including absolute, relative, and emergency indications with contraindications
    - Historical and anatomical background with epidemiology of the procedure
    - Pre-operative phase with patient evaluation, testing, risk assessment, and counseling
    - Operative phase with surgical approaches, anesthesia, steps, instruments, and duration
    - Operative risks covering intraoperative, early, and late postoperative complications
    - Postoperative management including pain control, monitoring, diet, and discharge criteria
    - Recovery timeline with rehabilitation, return to work, success rates, and long-term outcomes
    - Alternative treatments including medical management, minimally invasive, and conservative approaches
    - Technical details with surgeon qualifications, facility requirements, and technology used
    - Current research and innovations including robotic surgery, AI applications, and clinical trials
    - Special populations considerations for pediatric, geriatric, and pregnant patients
    - Patient education with plain language explanation, key takeaways, and misconception correction
    - Evidence summary with evidence levels and comparative effectiveness research
    - Cost and insurance information including procedures codes and financial assistance programs
"""

import sys
import json
import argparse
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

# ============================================================================ 
# CONFIGURATION
# ============================================================================ 

@dataclass
class Config(StorageConfig):
    """Configuration for the surgery info generator."""
    output_dir: Path = field(default_factory=lambda: Path("outputs"))
    log_file: Path = field(default_factory=lambda: Path(__file__).parent / "logs" / f"{Path(__file__).stem}.log")
    specialty: str = "Surgery/Procedure"
    verbosity: int = 2  # Verbosity level: 0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG

    def __post_init__(self):
        """Set default db_path if not provided, then validate."""
        if self.db_path is None:
            self.db_path = str(
                Path(__file__).parent.parent / "storage" / "surgery_info.lmdb"
            )
        # Call parent validation
        super().__post_init__()
# ============================================================================ 
# PYDANTIC MODELS FOR SURGERY INFORMATION STRUCTURE
# ============================================================================ 

class SurgeryMetadata(BaseModel):
    surgery_name: str = Field(description="Official name of the surgical procedure")
    alternative_names: str = Field(description="Other names for this surgery, comma-separated")
    procedure_code: str = Field(description="CPT or ICD procedure code")
    surgery_category: str = Field(description="Category of surgery (cardiovascular, orthopedic, gastrointestinal, etc.)")
    body_systems_involved: str = Field(description="Body systems affected by this surgery, comma-separated")

class SurgeryIndications(BaseModel):
    absolute_indications: str = Field(description="Conditions where surgery is mandatory or strongly indicated, comma-separated")
    relative_indications: str = Field(description="Conditions where surgery may be beneficial but alternatives exist, comma-separated")
    emergency_indications: str = Field(description="Life-threatening situations requiring immediate surgery, comma-separated")
    absolute_contraindications: str = Field(description="Conditions that completely prohibit the surgery, comma-separated")
    relative_contraindications: str = Field(description="Conditions that increase surgical risk but don't prohibit surgery, comma-separated")

class SurgeryBackground(BaseModel):
    definition: str = Field(description="Clear definition of what the surgery involves and why it's performed")
    surgical_anatomy: str = Field(description="Relevant anatomical structures and their relationships")
    historical_background: str = Field(description="Historical development of this surgical procedure")
    epidemiology: str = Field(description="How common this surgery is, indications prevalence, and population statistics")

class PreoperativePhase(BaseModel):
    patient_evaluation: str = Field(description="Clinical examination and history taking requirements, comma-separated")
    laboratory_tests: str = Field(description="Required blood tests, urine tests, or other lab work, comma-separated")
    imaging_studies: str = Field(description="X-rays, CT scans, MRI, ultrasound needed before surgery, comma-separated")
    specialist_consultations: str = Field(description="Required consultations with other specialists, comma-separated")
    risk_stratification: str = Field(description="Tools and methods to assess surgical risk, comma-separated")
    preoperative_preparation: str = Field(description="Physical and mental preparation steps, comma-separated")
    patient_counseling_points: str = Field(description="Key discussion points with patient before surgery, comma-separated")

class OperativePhase(BaseModel):
    surgical_approaches: str = Field(description="Open, laparoscopic, robotic, or other surgical approaches, comma-separated")
    anesthesia_type: str = Field(description="General, regional, local, or sedation requirements, comma-separated")
    patient_positioning: str = Field(description="How the patient is positioned during surgery")
    surgical_steps: str = Field(description="Step-by-step procedure description, numbered or comma-separated")
    instruments_equipment: str = Field(description="Special instruments or equipment needed, comma-separated")
    duration: str = Field(description="Typical duration of the surgical procedure")

class OperativeRisks(BaseModel):
    intraoperative_complications: str = Field(description="Complications that can occur during surgery, comma-separated")
    early_postoperative_complications: str = Field(description="Complications within first few days/weeks, comma-separated")
    late_postoperative_complications: str = Field(description="Long-term complications and sequelae, comma-separated")
    complication_rates: str = Field(description="Statistical rates of common complications")

class PostoperativePhase(BaseModel):
    immediate_care: str = Field(description="ICU or recovery room management protocols, comma-separated")
    pain_management: str = Field(description="Analgesic protocols and pain control strategies, comma-separated")
    monitoring_parameters: str = Field(description="Vital signs and clinical parameters to monitor, comma-separated")
    diet_progression: str = Field(description="Dietary advancement plan after surgery, comma-separated")
    mobilization_protocol: str = Field(description="Timeline and steps for patient mobilization, comma-separated")
    drain_management: Optional[str] = Field(description="Management of surgical drains if applicable, comma-separated")
    hospital_stay: str = Field(description="Expected length of hospitalization")
    discharge_criteria: str = Field(description="Requirements for safe discharge from hospital, comma-separated")

class RecoveryAndOutcomes(BaseModel):
    recovery_timeline: str = Field(description="Recovery milestones and expected duration")
    rehabilitation_protocol: str = Field(description="Physical therapy or rehabilitation plan, comma-separated")
    return_to_work: str = Field(description="When patients can typically return to work")
    return_to_normal_activities: str = Field(description="When patients can resume normal activities")
    success_rates: str = Field(description="Statistical success rates of the procedure")
    functional_outcomes: str = Field(description="Expected functional recovery and quality of life, comma-separated")
    recurrence_rates: Optional[str] = Field(description="Rates of condition recurrence if applicable")
    long_term_outcomes: str = Field(description="Long-term results and patient outcomes, comma-separated")

class FollowUp(BaseModel):
    follow_up_schedule: str = Field(description="When and how often follow-up appointments are needed")
    monitoring_required: str = Field(description="Tests or evaluations needed after surgery, comma-separated")
    lifestyle_modifications: str = Field(description="Lifestyle changes and precautions needed after surgery, comma-separated")
    warning_signs: str = Field(description="Symptoms requiring immediate medical attention, comma-separated")

class Alternatives(BaseModel):
    medical_management: str = Field(description="Non-surgical treatment options, comma-separated")
    minimally_invasive_procedures: str = Field(description="Less invasive alternatives to open surgery, comma-separated")
    conservative_approaches: str = Field(description="Observation or expectant management options, comma-separated")
    advantages_over_alternatives: str = Field(description="Why this surgery may be preferred, comma-separated")

class TechnicalDetails(BaseModel):
    surgical_approach_variations: str = Field(description="Different variations or modifications of the procedure, comma-separated")
    surgeon_qualifications: str = Field(description="Required training and certifications for performing surgeon")
    facility_requirements: str = Field(description="Hospital or facility requirements for performing procedure")
    technology_used: str = Field(description="Advanced technology or robotics involved")

class SurgeryResearch(BaseModel):
    recent_innovations: str = Field(description="New surgical techniques, technologies, or approaches developed in recent years, comma-separated")
    robotic_ai_applications: str = Field(description="Use of robotic surgery, AI assistance, or machine learning in this procedure, comma-separated")
    emerging_technologies: str = Field(description="New devices, instruments, or tools being developed or tested, comma-separated")
    clinical_trials: str = Field(description="Ongoing or recent clinical trials related to this surgery, comma-separated")
    future_directions: str = Field(description="Potential future developments and research areas, comma-separated")
    quality_improvement_initiatives: str = Field(description="Programs or protocols to improve surgical outcomes, comma-separated")

class SpecialPopulations(BaseModel):
    pediatric_considerations: Optional[str] = Field(description="Special considerations for pediatric patients if applicable")
    geriatric_considerations: Optional[str] = Field(description="Special considerations for elderly patients")
    pregnancy_considerations: Optional[str] = Field(description="Safety and considerations during pregnancy if applicable")

class SurgeryEducation(BaseModel):
    plain_language_explanation: str = Field(description="Simple explanation of the surgery for patients")
    key_takeaways: str = Field(description="3-5 most important points about the surgery, comma-separated")
    common_misconceptions: str = Field(description="Common myths or misconceptions about this surgery, comma-separated")

class SurgeryEvidence(BaseModel):
    evidence_level: str = Field(description="Level of evidence supporting this surgery (high, moderate, low)")
    evidence_summary: str = Field(description="Summary of major guidelines and evidence quality")
    comparative_effectiveness: Optional[str] = Field(description="Research comparing different surgical approaches or techniques")

class CostAndInsurance(BaseModel):
    typical_cost_range: str = Field(description="General cost range without insurance")
    insurance_coverage: str = Field(description="How typically covered by insurance")
    medicare_coverage: str = Field(description="Medicare coverage specifics")
    medicaid_coverage: str = Field(description="Medicaid coverage information")
    prior_authorization: str = Field(description="Whether insurance pre-approval is needed")
    financial_assistance_programs: str = Field(description="Programs to help with costs, comma-separated")

class SurgeryInfo(BaseModel):
    metadata: SurgeryMetadata
    background: SurgeryBackground
    indications: SurgeryIndications
    preoperative: PreoperativePhase
    operative: OperativePhase
    operative_risks: OperativeRisks
    postoperative: PostoperativePhase
    recovery_outcomes: RecoveryAndOutcomes
    follow_up: FollowUp
    alternatives: Alternatives
    special_populations: SpecialPopulations
    technical: TechnicalDetails
    research: SurgeryResearch
    evidence: SurgeryEvidence
    education: SurgeryEducation
    cost_and_insurance: CostAndInsurance

# ============================================================================ 
# SURGERY INFO GENERATOR CLASS
# ============================================================================ 

class SurgeryInfoGenerator:
    """Generate comprehensive information for surgical procedures."""

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        # Load model name from ModuleConfig

        try:

            module_config = get_module_config("surgery_info")

            model_name = module_config.model_name

        except ValueError:

            # Fallback to default if not registered yet

            model_name = "gemini-1.5-flash"

        

        self.client = MedKitClient(model_name=model_name)
        self.surgery_name: Optional[str] = None
        self.output_path: Optional[Path] = None

    def generate(self, surgery_name: str, output_path: Optional[Path] = None) -> SurgeryInfo:
        if not surgery_name or not surgery_name.strip():
            raise ValueError("Surgery name cannot be empty")

        self.surgery_name = surgery_name

        if output_path is None:
            output_path = self.config.output_dir / f"{surgery_name.lower().replace(' ', '_')}_info.json"
        
        self.output_path = output_path

        logger.info(f"Starting surgical information generation for: {surgery_name}")

        surgery_info = self._generate_info()

        self.save(surgery_info, self.output_path)
        self.print_summary(surgery_info)
        
        return surgery_info

    def _generate_info(self) -> SurgeryInfo:
        sys_prompt = f"""You are an expert medical documentation specialist with deep knowledge of surgical procedures and clinical practice in {self.config.specialty}.

Generate comprehensive, evidence-based procedure information ensuring all information is:
- Medically accurate and aligned with current guidelines
- Detailed enough for both patient education and clinical reference
- Supported by authoritative medical sources where applicable
- Clearly distinguished between common/expected outcomes and rare complications
- Includes statistical data when available (success rates, complication rates)

Return structured JSON matching the exact schema provided, with all required fields populated."""

        result = self.client.generate_text(
            prompt=f"Generate complete, evidence-based information for the surgical procedure: {self.surgery_name}",
            schema=SurgeryInfo,
            sys_prompt=sys_prompt,
        )
        return result

    def save(self, surgery_info: SurgeryInfo, output_path: Path) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(surgery_info.model_dump(), f, indent=2)
        
        logger.info(f"✓ Surgical information saved to {output_path}")
        return output_path

    def print_summary(self, surgery_info: SurgeryInfo) -> None:
        if self.config.verbosity < 3:
            return
        print("\n" + "="*70)
        print(f"SURGERY INFORMATION SUMMARY: {surgery_info.metadata.surgery_name}")
        print("="*70)
        print(f"  - Category: {surgery_info.metadata.surgery_category}")
        print(f"  - Body Systems: {surgery_info.metadata.body_systems_involved}")
        print(f"\n✓ Generation complete. Saved to {self.output_path}")

def get_surgery_info(surgery_name: str, output_path: Optional[Path] = None, verbosity: int = 2) -> SurgeryInfo:
    """
    High-level function to generate and optionally save surgery information.
    """
    config = Config(verbosity=verbosity)
    generator = SurgeryInfoGenerator(config=config)
    return generator.generate(surgery_name, output_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate comprehensive surgical procedure information.")
    parser.add_argument("surgery", nargs='+', help="Name of the surgical procedure")
    parser.add_argument("-o", "--output", type=Path, help="Path to save JSON output.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbosity level (default: 2=WARNING)")

    args = parser.parse_args()

    try:
        surgery_name = " ".join(args.surgery)
        config = Config(quiet=not args.verbose)
        generator = SurgeryInfoGenerator(config=config)
        generator.generate(surgery_name=surgery_name, output_path=args.output)
        if args.verbose:
            print("✓ Success!")

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


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

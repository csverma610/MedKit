"""
surgical_tool_info - Generate comprehensive surgical instrument documentation.

This module generates detailed, evidence-based surgical tool and instrument documentation using
structured Pydantic data models and the MedKit AI client. Coverage includes physical specifications,
operational characteristics, safety features, maintenance requirements, and clinical applications
with emphasis on user value and practical operational guidance.

QUICK START:
    Get comprehensive information about a surgical instrument:

    >>> from surgical_tool_info import SurgicalToolInfoGenerator
    >>> generator = SurgicalToolInfoGenerator()
    >>> result = generator.generate("Surgical Scalpel")
    >>> print(f"Generated tool information for {result.tool_basics.tool_name}")

    With custom output path:

    >>> result = generator.generate("Surgical Forceps", output_path="instruments/forceps.json")

    Or use the CLI:

    $ python surgical_tool_info.py "Surgical Scalpel"
    $ python surgical_tool_info.py "Hemostatic Clamp" -o surgical_instruments/

COMMON USES:
    1. Surgeon training - comprehensive learning resources for safe and effective tool use
    2. Instrument procurement - specifications and comparisons for OR equipment purchasing decisions
    3. Operating room management - maintenance schedules, sterilization protocols, and inventory tracking
    4. Surgical safety - identifying risks, complications, and best practices for tool usage
    5. Equipment evaluation - comparing alternatives and understanding advantages/disadvantages

KEY FEATURES AND COVERAGE AREAS:
    - Tool basics with official names, categories, surgical specialties, and instrument families
    - Purpose and applications including surgical use, anatomical targets, tissue types, and advantages
    - Physical specifications including dimensions, weight, material composition, finish, and design
    - Operational characteristics with cutting/grasping force, actuation, precision level, and range
    - Safety features including locks, guards, quick-release mechanisms, and damage prevention
    - Pre-operative preparation with inspection, cleaning, sterilization, and quality assurance
    - Intraoperative use with positioning, handling technique, hand position, and coordination with other tools
    - Complications and risks including surgeon fatigue, common errors, tissue damage, and infections
    - Maintenance and care with post-operative cleaning, lubrication, inspection, and lifespan
    - Sterilization and disinfection with approved methods, incompatible procedures, and validation standards
    - Alternatives and comparisons with similar tools, advantages, disadvantages, and cost analysis
    - Historical context with invention history, evolution, clinical evidence, and current role in surgery
    - Specialty-specific considerations for general surgery, orthopedics, cardiac, neuro, and vascular
    - Training and certification requirements with proficiency indicators and mentoring best practices
    - Regulatory and standards compliance including FDA classification, ISO standards, and quality certifications
    - Cost and procurement information including single-use/reusable costs, vendors, and inventory recommendations
"""
import json
import sys
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
    """Configuration for the surgical tool info generator."""
    output_dir: Path = field(default_factory=lambda: Path("outputs"))
    log_file: Path = field(default_factory=lambda: Path(__file__).parent / "logs" / f"{Path(__file__).stem}.log")
    specialty: str = "Surgery/Surgical Instruments"
    verbosity: int = 2  # Verbosity level: 0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG

    def __post_init__(self):
        """Set default db_path if not provided, then validate."""
        if self.db_path is None:
            self.db_path = str(
                Path(__file__).parent.parent / "storage" / "surgical_tool_info.lmdb"
            )
        # Call parent validation
        super().__post_init__()
# ============================================================================ 
# PYDANTIC MODELS FOR SURGICAL TOOL INFORMATION STRUCTURE
# ============================================================================ 

class ToolBasics(BaseModel):
    tool_name: str = Field(description="Official name of the surgical tool")
    alternative_names: str = Field(description="Other names or abbreviations for this tool, comma-separated")
    tool_category: str = Field(description="Category (cutting, grasping, retracting, cautery, etc)")
    surgical_specialties: str = Field(description="Medical specialties that use this tool, comma-separated")
    instrument_family: str = Field(description="Family or group this tool belongs to (e.g., scissor family, clamp family)")

class ToolPurpose(BaseModel):
    primary_purpose: str = Field(description="Main function of this surgical tool")
    surgical_applications: str = Field(description="Specific surgical procedures where this tool is used, comma-separated")
    anatomical_targets: str = Field(description="Anatomical structures this tool is typically used on, comma-separated")
    tissue_types: str = Field(description="Types of tissue this tool is designed to work with (soft tissue, bone, vascular), comma-separated")
    unique_advantages: str = Field(description="What makes this tool superior to alternatives for its intended use, comma-separated")

class PhysicalSpecifications(BaseModel):
    dimensions: str = Field(description="Overall length and dimensions with specific measurements in cm or inches")
    weight: str = Field(description="Tool weight if relevant with specific values in grams or ounces")
    material_composition: str = Field(description="Materials used (stainless steel grades, titanium, tungsten carbide), comma-separated")
    finish_type: str = Field(description="Surface finish (polished, electropolished, serrated, textured)")
    blade_or_tip_specifications: str = Field(description="Specific details about working edge (blade angle, tip curvature, point geometry) with measurements")
    handle_design: str = Field(description="Handle characteristics (ergonomic curve, textured grip, material, weight distribution)")
    sterility_type: str = Field(description="Single-use or reusable, and sterilization method (autoclavable, ETO gas, etc)")

class OperationalCharacteristics(BaseModel):
    cutting_or_grasping_force: str = Field(description="Force specifications with numerical values if applicable")
    actuation_mechanism: str = Field(description="How the tool is activated (manual, mechanical, powered, articulated)")
    degrees_of_freedom: str = Field(description="Range of motion or articulation (fixed, single axis, multi-axis with specific angles)")
    precision_level: str = Field(description="Precision capability (gross, fine, micro-level) with specific measurements")
    engagement_depth: str = Field(description="Depth of cut, grasp, or working depth with specific values")
    working_distance: str = Field(description="Distance from tool tip to handle/body, optimal working distance from patient")

class SafetyFeatures(BaseModel):
    safety_mechanisms: str = Field(description="Built-in safety features (locks, guards, quick-release), comma-separated")
    slip_resistance: str = Field(description="Grip and handling safety features to prevent slipping")
    wear_considerations: str = Field(description="Signs of tool wear that indicate replacement need")
    maximum_safe_force: str = Field(description="Specifications on maximum force that should be applied without damage")
    emergency_protocols: str = Field(description="What to do if tool becomes stuck or breaks during use, comma-separated")
    tissue_damage_prevention: str = Field(description="Design features to minimize inadvertent tissue damage, comma-separated")

class PreOperativePreperation(BaseModel):
    inspection_requirements: str = Field(description="Pre-use inspection checklist (sharp test, functional test, damage check), comma-separated")
    cleaning_protocols: str = Field(description="How to properly clean before surgery with specific cleaning agents and duration")
    sterilization_requirements: str = Field(description="Sterilization method (autoclave temperature/time, chemical), specific parameters")
    quality_assurance_tests: str = Field(description="Tests to verify tool functionality before use, comma-separated")
    storage_requirements: str = Field(description="Proper storage conditions (temperature, humidity, protective cases)")
    preparation_time: str = Field(description="Time required for complete preparation and sterilization")

class IntraOperativeUse(BaseModel):
    positioning_in_field: str = Field(description="How tool is positioned relative to surgical field and anatomy")
    handling_technique: str = Field(description="Proper handling and technique for effective use")
    hand_position_requirements: str = Field(description="Specific hand grip and positioning for optimal control and visibility")
    coordination_with_other_tools: str = Field(description="How this tool is coordinated with other instruments, comma-separated")
    common_movements: str = Field(description="Typical motions performed with this tool during surgery (cutting angle, retraction direction, etc)")
    visibility_requirements: str = Field(description="Visual field needed to safely use this tool")
    ergonomic_considerations: str = Field(description="Ergonomic aspects of prolonged use (fatigue risk, repetitive strain prevention)")

class DiscomfortRisksAndComplications(BaseModel):
    surgeon_fatigue_factors: str = Field(description="Design aspects that might cause surgeon fatigue or strain with prolonged use")
    common_handling_errors: str = Field(description="Frequent mistakes surgeons make with this tool, comma-separated")
    tissue_damage_risks: str = Field(description="Potential unintended tissue damage (perforation, crushing, charring), comma-separated")
    instrument_complications: str = Field(description="Breakage, dulling, or malfunction risks, comma-separated")
    cross_contamination_risks: str = Field(description="Infection control concerns if not properly handled or sterilized")
    material_reactions: str = Field(description="Potential reactions with specific implants or materials in patient")
    electrical_safety: str = Field(description="For powered tools: electrical hazards, grounding, safety interlocks")

class MaintenanceAndCare(BaseModel):
    post_operative_cleaning: str = Field(description="Cleaning protocol after surgery with specific solutions and duration")
    lubrication_schedule: str = Field(description="When and with what lubricant to maintain tool function")
    inspection_frequency: str = Field(description="How often tool should be inspected with specific timeframes")
    wear_indicators: str = Field(description="Signs that tool needs replacement or sharpening, comma-separated")
    sharpening_protocol: str = Field(description="For cutting tools: sharpening method, frequency, specifications when sharp")
    repair_guidelines: str = Field(description="When tool can be repaired vs must be replaced")
    expected_lifespan: str = Field(description="Typical lifespan in number of uses or years with specific parameters")

class SterilizationAndDisinfection(BaseModel):
    approved_sterilization_methods: str = Field(description="Approved methods with temperature/pressure/time specifications, comma-separated")
    incompatible_sterilization: str = Field(description="Methods that should NOT be used and why, comma-separated")
    disinfection_alternatives: str = Field(description="If high-level disinfection acceptable, methods and conditions")
    packaging_requirements: str = Field(description="Packaging standards for sterilization (wrap type, labeling)")
    validation_standards: str = Field(description="Standards for validating sterilization (biological indicators, etc)")
    reprocessing_manufacturer_protocols: str = Field(description="Manufacturer-specific reprocessing guidelines to follow")

class AlternativesAndComparisons(BaseModel):
    similar_alternative_tools: str = Field(description="Other tools that serve similar function, comma-separated")
    advantages_over_alternatives: str = Field(description="Specific advantages of this tool compared to alternatives, comma-separated")
    disadvantages_vs_alternatives: str = Field(description="When alternatives might be preferred, comma-separated reasons")
    cost_comparison: str = Field(description="Relative cost compared to alternatives (if single-use, cost per use)")
    when_to_use_this_tool: str = Field(description="Specific clinical/anatomical scenarios where this tool is optimal")
    complementary_tools: str = Field(description="Tools often used alongside this one, comma-separated")

class HistoricalContext(BaseModel):
    invention_history: str = Field(description="History of tool development and key innovators")
    evolution_timeline: str = Field(description="Major design improvements over time with dates if applicable")
    clinical_evidence: str = Field(description="Key studies demonstrating effectiveness or safety")
    widespread_adoption: str = Field(description="When and why this tool became standard in practice")
    current_status: str = Field(description="Current role in modern surgery (standard, transitioning out, emerging)")

class SpecialtySpecificConsiderations(BaseModel):
    general_surgery_specific: str = Field(description="Specific uses and considerations in general surgery")
    orthopedic_specific: str = Field(description="Specific uses and considerations in orthopedic surgery")
    cardiac_specific: str = Field(description="Specific uses and considerations in cardiac surgery")
    neurosurgery_specific: str = Field(description="Specific uses and considerations in neurosurgery")
    vascular_specific: str = Field(description="Specific uses and considerations in vascular surgery")
    laparoscopic_considerations: str = Field(description="Modifications or special considerations for minimally invasive use")
    robotic_integration: str = Field(description="If applicable: use with robotic surgical systems")

class TrainingAndCertification(BaseModel):
    training_requirements: str = Field(description="Training needed to safely use this tool")
    proficiency_indicators: str = Field(description="Signs of mastery and competency with tool use, comma-separated")
    common_learning_mistakes: str = Field(description="Typical errors made during training period, comma-separated")
    skill_development_timeline: str = Field(description="Typical time to proficiency for experienced vs novice surgeons")
    formal_education_resources: str = Field(description="Textbooks, courses, or programs that teach this tool, comma-separated")
    mentoring_best_practices: str = Field(description="Best practices for teaching others to use this tool")

class RegulatoryAndStandards(BaseModel):
    fda_classification: str = Field(description="FDA classification (Class I, II, III) if applicable")
    fda_status: str = Field(description="FDA approval/clearance status with approval date if applicable")
    iso_standards: str = Field(description="Relevant ISO standards the tool must meet, comma-separated")
    country_approvals: str = Field(description="Countries where tool is approved for use")
    quality_certifications: str = Field(description="Quality and manufacturing certifications (ISO 13485, CE mark, etc)")
    traceability_requirements: str = Field(description="Labeling and tracking requirements for patient safety and recalls")

class CostAndProcurement(BaseModel):
    single_use_cost: Optional[str] = Field(description="Cost per use for single-use instruments")
    reusable_initial_cost: Optional[str] = Field(description="Initial purchase cost for reusable instruments")
    lifecycle_cost: str = Field(description="Total cost of ownership including maintenance, sterilization, replacement")
    vendor_options: str = Field(description="Major manufacturers and suppliers, comma-separated")
    procurement_lead_time: str = Field(description="Typical ordering and delivery timeframe")
    inventory_recommendations: str = Field(description="How many should be stocked based on usage")
    insurance_coverage: str = Field(description="Typical insurance/hospital coverage for this tool")

class EducationalContent(BaseModel):
    plain_language_explanation: str = Field(description="Simple explanation of what this tool does and why")
    key_takeaways: str = Field(description="3-5 most important points about this tool, comma-separated")
    common_misconceptions: str = Field(description="Common myths or misunderstandings about this tool, comma-separated")
    patient_communication: str = Field(description="How to explain use of this tool to patients seeking informed consent")
    video_demonstration_topics: str = Field(description="Key aspects that should be covered in training videos, comma-separated")

class SurgicalToolInfo(BaseModel):
    tool_basics: ToolBasics
    tool_purpose: ToolPurpose
    physical_specifications: PhysicalSpecifications
    operational_characteristics: OperationalCharacteristics
    safety_features: SafetyFeatures
    preparation: PreOperativePreperation
    intraoperative_use: IntraOperativeUse
    discomfort_risks_and_complications: DiscomfortRisksAndComplications
    maintenance_and_care: MaintenanceAndCare
    sterilization_and_disinfection: SterilizationAndDisinfection
    alternatives_and_comparisons: AlternativesAndComparisons
    historical_context: HistoricalContext
    specialty_specific_considerations: SpecialtySpecificConsiderations
    training_and_certification: TrainingAndCertification
    regulatory_and_standards: RegulatoryAndStandards
    cost_and_procurement: CostAndProcurement
    educational_content: EducationalContent

# ============================================================================ 
# SURGICAL TOOL INFO GENERATOR CLASS
# ============================================================================ 

class SurgicalToolInfoGenerator:
    """Generate comprehensive information for surgical tools."""

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        # Load model name from ModuleConfig

        try:

            module_config = get_module_config("surgical_tool_info")

            model_name = module_config.model_name

        except ValueError:

            # Fallback to default if not registered yet

            model_name = "gemini-1.5-flash"

        

        self.client = MedKitClient(model_name=model_name)
        self.tool_name: Optional[str] = None
        self.output_path: Optional[Path] = None

    def generate(self, tool_name: str, output_path: Optional[Path] = None) -> SurgicalToolInfo:
        if not tool_name or not tool_name.strip():
            raise ValueError("Tool name cannot be empty")

        self.tool_name = tool_name

        if output_path is None:
            output_path = self.config.output_dir / f"{tool_name.lower().replace(' ', '_')}_info.json"
        
        self.output_path = output_path

        logger.info(f"Starting surgical tool information generation for: {tool_name}")

        tool_info = self._generate_info()

        self.save(tool_info, self.output_path)
        self.print_summary(tool_info)
        
        return tool_info

    def _generate_info(self) -> SurgicalToolInfo:
        sys_prompt = f"""You are an expert medical documentation specialist with deep knowledge of surgical procedures and clinical practice in {self.config.specialty}.

Generate comprehensive, evidence-based procedure information ensuring all information is:
- Medically accurate and aligned with current guidelines
- Detailed enough for both patient education and clinical reference
- Supported by authoritative medical sources where applicable
- Clearly distinguished between common/expected outcomes and rare complications
- Includes statistical data when available (success rates, complication rates)

Return structured JSON matching the exact schema provided, with all required fields populated."""

        result = self.client.generate_text(
            prompt=f"Generate complete, evidence-based information for the surgical tool: {self.tool_name}",
            schema=SurgicalToolInfo,
            sys_prompt=sys_prompt,
        )
        return result

    def save(self, tool_info: SurgicalToolInfo, output_path: Path) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(tool_info.model_dump(), f, indent=2)
        
        logger.info(f"✓ Surgical tool information saved to {output_path}")
        return output_path

    def print_summary(self, tool_info: SurgicalToolInfo) -> None:
        if self.config.verbosity < 3:
            return

        print("\n" + "="*70)
        print(f"SURGICAL TOOL INFORMATION SUMMARY: {tool_info.tool_basics.tool_name}")
        print("="*70)
        print(f"  - Category: {tool_info.tool_basics.tool_category}")
        print(f"  - Specialties: {tool_info.tool_basics.surgical_specialties}")
        print(f"\n✓ Generation complete. Saved to {self.output_path}")

def get_surgical_tool_info(tool_name: str, output_path: Optional[Path] = None, verbosity: int = 2) -> SurgicalToolInfo:
    """
    High-level function to generate and optionally save surgical tool information.

    Args:
        tool_name: Name of the surgical tool to generate information for.
        output_path: Optional path to save the output JSON file.
        quiet: If True, suppress console output (only save to file and logs).
    """
    config = Config(verbosity=verbosity)
    generator = SurgicalToolInfoGenerator(config=config)
    return generator.generate(tool_name, output_path)


def main():
    parser = argparse.ArgumentParser(description="Generate comprehensive surgical tool information.")
    parser.add_argument("-i", "--tool", nargs='+', help="Name of the surgical tool")
    parser.add_argument("-o", "--output", type=Path, help="Path to save JSON output.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbosity level (default: 2=WARNING)")

    args = parser.parse_args()

    try:
        tool_name = " ".join(args.tool)
        config = Config(quiet=not args.verbose)
        generator = SurgicalToolInfoGenerator(config=config)
        generator.generate(tool_name=tool_name, output_path=args.output)
        if args.verbose:
            print("✓ Success!")

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
   main()

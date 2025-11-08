"""
medical_anatomy - Generate comprehensive anatomical structure documentation.

This module generates detailed, evidence-based anatomical information for any human
anatomical structure. It provides complete anatomical documentation including location,
structure, function, clinical significance, and imaging characteristics using the MedKit
AI client with structured Pydantic schemas. Output includes embryological origin, normal
variations, clinical pathologies, imaging appearance across modalities, and surgical
approaches organized into 12 comprehensive sections.

QUICK START:
    Generate anatomy information for a structure:

    >>> from medical_anatomy import MedicalAnatomyGenerator
    >>> generator = MedicalAnatomyGenerator()
    >>> result = generator.generate("Heart")
    >>> print(result.overview.structure_name)
    Heart

    Or use the CLI:

    $ python medical_anatomy.py -i "Femur"
    $ python medical_anatomy.py -i "Biceps brachii" -o custom_output.json

COMMON USES:
    1. Medical student reference - detailed anatomical descriptions for study and exams
    2. Clinical documentation - comprehensive anatomy for medical records and reports
    3. Patient education - generating understandable anatomy summaries for informed consent
    4. Surgical planning - accessing landmarks, approaches, and anatomy at risk
    5. Teaching materials - creating standardized anatomy content for courses

KEY FEATURES AND COVERAGE AREAS:
    - Anatomical Overview: official names, classification, body system, embryological origin
    - Anatomical Position: location, landmarks, anatomical planes, surface anatomy
    - Gross Morphology: shape, dimensions, color, surface features, attachments
    - Microscopic Structure: tissue types, cellular components, histological layers
    - Anatomical Function: primary/secondary functions, mechanism of action
    - Vascular/Innervation: arterial supply, venous drainage, nerve supply, dermatomes
    - Variations/Anomalies: normal variants, congenital conditions, age/sex differences
    - Clinical Significance: pathologies, injury vulnerability, pain patterns, examination
    - Imaging Characteristics: X-ray, ultrasound, CT, MRI appearance
    - Developmental Anatomy: embryological development, growth timeline, maturation
    - Surgical Landmarks: surface anatomy, surgical approaches, risk structures
    - Cross-References: related structures and anatomical relationships
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
    """Configuration for the medical anatomy generator."""
    output_dir: Path = field(default_factory=lambda: Path("outputs"))
    log_file: Path = field(default_factory=lambda: Path(__file__).parent / "logs" / f"{Path(__file__).stem}.log")
    verbosity: int = 2  # Verbosity level: 0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG

    def __post_init__(self):
        """Set default db_path if not provided, then validate."""
        if self.db_path is None:
            self.db_path = str(
                Path(__file__).parent.parent / "storage" / "medical_anatomy.lmdb"
            )
        # Call parent validation
        super().__post_init__()
# ============================================================================ 
# PYDANTIC MODELS FOR ANATOMY STRUCTURE
# ============================================================================ 

class AnatomyOverview(BaseModel):
    """Basic information about the anatomical structure."""
    structure_name: str = Field(description="Official anatomical name of the structure")
    common_names: str = Field(description="Common or alternative names, comma-separated")
    anatomical_classification: str = Field(description="Classification (bone, muscle, organ, vessel, nerve, etc)")
    body_system: str = Field(description="Primary body system this structure belongs to")
    embryological_origin: str = Field(description="Germ layer or embryological origin")
    prevalence_variation: str = Field(description="How common this structure is (universal, variable, or rare)")


class AnatomicalPosition(BaseModel):
    """Location and orientation of the structure."""
    anatomical_location: str = Field(description="Specific location in the body")
    body_regions: str = Field(description="Body regions or quadrants, comma-separated")
    surface_landmarks: str = Field(description="Palpable surface landmarks for identification")
    anatomical_planes: str = Field(description="Position relative to anatomical planes (anterior, posterior, medial, lateral, etc)")
    depth: str = Field(description="Depth in relation to skin surface (superficial, deep, etc)")
    relationships_to_other_structures: str = Field(description="How this structure relates to nearby structures, comma-separated")


class GrossMorphology(BaseModel):
    """Structural form and external appearance."""
    shape_description: str = Field(description="Overall shape and form of the structure")
    dimensions: str = Field(description="Typical size measurements (length, width, diameter, volume)")
    color_and_appearance: str = Field(description="Gross appearance including color and texture")
    surface_features: str = Field(description="Notable surface features or markings")
    attachment_points: str = Field(description="Where structure attaches to other structures, comma-separated")
    borders_and_margins: str = Field(description="Description of borders and anatomical margins")


class MicroscopicStructure(BaseModel):
    """Histological and cellular composition."""
    tissue_type: str = Field(description="Primary tissue types present, comma-separated")
    cellular_components: str = Field(description="Types of cells found in structure, comma-separated")
    histological_layers: str = Field(description="Distinct histological layers if applicable")
    special_structures: str = Field(description="Special microscopic features or organelles, comma-separated")
    staining_characteristics: str = Field(description="Appearance under different histological stains")


class AnatomicalFunction(BaseModel):
    """Functions and roles of the structure."""
    primary_functions: str = Field(description="Main functions of this structure, comma-separated")
    secondary_functions: str = Field(description="Secondary or supporting functions, comma-separated")
    mechanism_of_action: str = Field(description="How the structure performs its functions")
    functional_relationships: str = Field(description="Relationships with other structures for function, comma-separated")
    functional_significance: str = Field(description="Clinical importance of this structure's function")


class VascularInnervation(BaseModel):
    """Blood supply and nerve supply."""
    arterial_supply: str = Field(description="Major arteries supplying this structure")
    venous_drainage: str = Field(description="Major veins draining this structure")
    lymphatic_drainage: str = Field(description="Lymphatic drainage pathways if applicable")
    nerve_supply: str = Field(description="Cranial or spinal nerves innervating structure")
    nerve_types: str = Field(description="Types of innervation (somatic, autonomic, sensory, motor, etc)")
    dermatome_or_myotome: str = Field(description="Associated dermatome or myotome if applicable")


class VariationsAndAnomalies(BaseModel):
    """Normal variations and developmental anomalies."""
    anatomical_variations: str = Field(description="Normal anatomical variations, comma-separated")
    variation_frequency: str = Field(description="How common variations are in population")
    congenital_anomalies: str = Field(description="Congenital anomalies if applicable, comma-separated")
    age_related_changes: str = Field(description="How structure changes with age")
    sex_differences: str = Field(description="Differences between males and females if applicable")
    ethnic_or_genetic_variants: str = Field(description="Variations across populations if applicable")


class ClinicalSignificance(BaseModel):
    """Medical and clinical relevance."""
    clinical_importance: str = Field(description="Why this structure is clinically important")
    common_pathologies: str = Field(description="Common diseases affecting this structure, comma-separated")
    injury_vulnerability: str = Field(description="Susceptibility to injury and trauma")
    pain_and_referred_pain: str = Field(description="Pain patterns and referred pain associated with structure")
    diagnostic_palpation: str = Field(description="How structure is examined clinically")
    surgical_considerations: str = Field(description="Important considerations during surgery or procedures")


class ImagingCharacteristics(BaseModel):
    """How structure appears on imaging studies."""
    radiographic_appearance: str = Field(description="Appearance on X-ray")
    ultrasound_appearance: str = Field(description="Appearance on ultrasound")
    ct_appearance: str = Field(description="Appearance on CT scan")
    mri_appearance: str = Field(description="Appearance on MRI")
    imaging_techniques: str = Field(description="Best imaging modalities for visualization, comma-separated")
    radiodensity_or_signal: str = Field(description="Radiodensity, signal intensity, or echogenicity")


class DevelopmentalAnatomy(BaseModel):
    """Growth and development of the structure."""
    embryological_development: str = Field(description="How structure develops embryologically")
    fetal_development: str = Field(description="Development stages during fetal period")
    postnatal_growth: str = Field(description="Growth and development after birth")
    maturation_timeline: str = Field(description="Timeline of when structure reaches maturity")
    growth_patterns: str = Field(description="Growth patterns or growth spurts if applicable")


class AnatomicalLandmarksAndApproaches(BaseModel):
    """Clinical landmarks and surgical approaches."""
    surface_landmarks: str = Field(description="Palpable landmarks for identification")
    surface_anatomy_techniques: str = Field(description="Techniques for identifying structure clinically")
    surgical_approaches: str = Field(description="Common surgical approaches to access structure, comma-separated")
    anatomical_borders: str = Field(description="Important anatomical borders for surgical approach")
    risk_structures: str = Field(description="Nearby structures at risk during surgical access, comma-separated")


class SeeAlso(BaseModel):
    """Cross-references to related anatomical structures."""
    related_structures: str = Field(description="Related anatomical structures, comma-separated")
    connection_types: str = Field(description="Types of connections (adjacent, continuous, functionally related, innervated by, supplied by, etc), comma-separated")
    reason: str = Field(description="Brief explanation of how these structures relate to main structure")


class AnatomyMetadata(BaseModel):
    """Metadata and information structure."""
    last_updated: str = Field(description="When this information was last reviewed")
    information_sources: str = Field(description="Primary sources of information (anatomical textbooks, databases), comma-separated")
    confidence_level: str = Field(description="Confidence in provided information (high, medium, low)")
    complexity_level: str = Field(description="Complexity of topic (basic, intermediate, advanced)")


class MedicalAnatomy(BaseModel):
    """
    Comprehensive anatomical structure information.
    """
    # Basic identification
    overview: AnatomyOverview

    # Location and positioning
    anatomical_position: AnatomicalPosition

    # Structure and form
    gross_morphology: GrossMorphology
    microscopic_structure: MicroscopicStructure

    # Function and relationships
    anatomical_function: AnatomicalFunction
    vascular_innervation: VascularInnervation

    # Variations and development
    variations_and_anomalies: VariationsAndAnomalies
    developmental_anatomy: DevelopmentalAnatomy

    # Clinical aspects
    clinical_significance: ClinicalSignificance
    imaging_characteristics: ImagingCharacteristics
    anatomical_landmarks_and_approaches: AnatomicalLandmarksAndApproaches

    # Cross-references
    see_also: SeeAlso

    # Metadata
    metadata: AnatomyMetadata

# ============================================================================ 
# MEDICAL ANATOMY GENERATOR CLASS
# ============================================================================ 

class MedicalAnatomyGenerator:
    """Generate comprehensive information for anatomical structures."""

    def __init__(self, config: Optional[Config] = None):
        """Initialize the generator with a configuration."""
        self.config = config or Config()
        # Load model name from ModuleConfig

        try:

            module_config = get_module_config("medical_anatomy")

            model_name = module_config.model_name

        except ValueError:

            # Fallback to default if not registered yet

            model_name = "gemini-1.5-flash"

        

        self.client = MedKitClient(model_name=model_name)
        self.structure_name: Optional[str] = None
        self.output_path: Optional[Path] = None

    def generate(self, structure_name: str, output_path: Optional[Path] = None) -> MedicalAnatomy:
        """
        Generate and save comprehensive anatomical information.

        Args:
            structure_name: Name of the anatomical structure.
            output_path: Optional path to save the JSON output.

        Returns:
            The generated MedicalAnatomy object.
        
        Raises:
            ValueError: If structure_name is empty.
        """
        if not structure_name or not structure_name.strip():
            raise ValueError("Structure name cannot be empty")

        self.structure_name = structure_name

        if output_path is None:
            output_path = self.config.output_dir / f"{structure_name.lower().replace(' ', '_')}_anatomy.json"
        
        self.output_path = output_path

        logger.info(f"Starting anatomical information generation for: {structure_name}")

        anatomy_info = self._generate_info()

        self.save(anatomy_info, self.output_path)
        self.print_summary(anatomy_info)
        
        return anatomy_info

    def _generate_info(self) -> MedicalAnatomy:
        """Generates the anatomical information."""
        prompt = f"""Generate comprehensive anatomical information for: {self.structure_name}

Include:
1. Anatomical overview and classification
2. Location and anatomical position
3. Gross morphology and structure
4. Microscopic/histological structure
5. Functions and roles
6. Vascular supply and innervation
7. Anatomical variations and anomalies
8. Developmental anatomy
9. Clinical significance and pathologies
10. Imaging characteristics
11. Surface anatomy and surgical approaches
12. Cross-references to related structures (see_also) - include adjacent structures, functionally related structures, structures with shared innervation, and structures in same system

For see_also cross-references, identify:
- Related anatomical structures that help readers understand anatomical relationships
- Types of connections (adjacent, continuous, functionally related, innervated by, supplied by, part of same system, etc.)
- Brief explanation of anatomical relationships

Provide accurate, detailed anatomical information based on standard anatomical references."""

        result = self.client.generate_text(
            prompt,
            schema=MedicalAnatomy
        )
        return result

    def save(self, anatomy_info: MedicalAnatomy, output_path: Path) -> Path:
        """
        Save the generated anatomical information to a JSON file.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(anatomy_info.model_dump(), f, indent=2)
        
        logger.info(f"✓ Anatomical information saved to {output_path}")
        return output_path

    def print_summary(self, anatomy_info: MedicalAnatomy) -> None:
        """
        Print a summary of the generated anatomical information.
        """
        if self.config.verbosity < 3:
            return
        print("\n" + "="*70)
        print(f"ANATOMY INFORMATION SUMMARY: {anatomy_info.overview.structure_name}")
        print("="*70)
        print(f"  - Body System: {anatomy_info.overview.body_system}")
        print(f"  - Location: {anatomy_info.anatomical_position.anatomical_location}")
        print(f"  - Classification: {anatomy_info.overview.anatomical_classification}")
        print(f"\n✓ Generation complete. Saved to {self.output_path}")

def get_anatomy_info(structure_name: str, output_path: Optional[Path] = None, verbosity: int = 2) -> MedicalAnatomy:
    """
    High-level function to generate and optionally save anatomy information.
    """
    config = Config(verbosity=verbosity)
    generator = MedicalAnatomyGenerator(config=config)
    return generator.generate(structure_name, output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate comprehensive information for an anatomical structure.")
    parser.add_argument("-i", "--anatomy", type=str, required=True, help="The name of the anatomical structure to generate information for.")
    parser.add_argument("-o", "--output", type=str, help="Optional: The path to save the output JSON file.")
    parser.add_argument("-v", "--verbosity", type=int, default=2, choices=[0, 1, 2, 3, 4], help="Verbosity level: 0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG")

    args = parser.parse_args()

    get_anatomy_info(args.anatomy, args.output, args.verbosity)


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

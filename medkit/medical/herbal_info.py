"""
herbal_info - Generate comprehensive herbal remedy documentation.

This module generates detailed, evidence-based information about herbal remedies and
medicinal plants. It provides complete herbal documentation including botanical information,
traditional uses, mechanisms of action, dosing, safety profiles, interactions, and clinical
evidence using the MedKit AI client with structured Pydantic schemas.

QUICK START:
    Generate herbal information:

    >>> from herbal_info import HerbalInfoGenerator
    >>> generator = HerbalInfoGenerator()
    >>> result = generator.generate("Ginger")
    >>> print(result.metadata.common_name)
    Ginger

    Or use the CLI:

    $ python herbal_info.py -i "Turmeric"
    $ python herbal_info.py -i "Chamomile" -o custom_output.json

COMMON USES:
    1. Integrative medicine - evidence-based herbal recommendations for practitioners
    2. Patient education - helping patients understand herbal safety and efficacy
    3. Herbal databases - comprehensive reference library for herbalists and naturopaths
    4. Clinical decision-making - contraindications, interactions, and indications
    5. Pharmaceutical research - phytochemistry and bioactive compound information

KEY FEATURES AND COVERAGE AREAS:
    - Botanical identification: common names, scientific names, plant family
    - Traditional uses: historical applications across multiple medicine systems
    - Active constituents: phytochemicals and identified therapeutic compounds
    - Mechanism of action: biochemical pathways and therapeutic effects
    - Forms and preparation: tea, tincture, extract, topical, culinary applications
    - Dosage and administration: age-specific dosing with administration guidance
    - Safety and side effects: common and serious adverse effects
    - Interactions: drug, herb, food, caffeine, and alcohol interactions
    - Contraindications and precautions: when herb should be avoided
    - Special populations: pediatric, pregnancy, breastfeeding, kidney/liver considerations
    - Efficacy: traditional claims, clinical evidence, onset and duration of action
    - Alternatives: similar herbs and complementary therapies
    - Cost and availability: pricing, regulatory status, sourcing information
    - Clinical evidence: research quality, studies, FDA/regulatory classification
"""

import argparse
import json
import sys
import logging
from pathlib import Path
from dataclasses import dataclass, field
from pydantic import BaseModel, Field
from typing import Optional

from medkit.utils.logging_config import setup_logger

import hashlib
from medkit.utils.lmdb_storage import LMDBStorage, LMDBConfig

# Configure logging
logger = setup_logger(__name__)

# Logging will be configured based on verbosity level in __init__

from medkit.utils.storage_config import StorageConfig

try:
    from medkit.core.medkit_client import MedKitClient
    from medkit.core.module_config import get_module_config
except ImportError as e:
    raise ImportError("MedKitClient not found. Install medkit-client package.") from e

# ============================================================================ 
# CONFIGURATION
# ============================================================================ 

@dataclass
class Config(StorageConfig):
    """Configuration for the herbal info generator."""
    output_dir: Path = field(default_factory=lambda: Path("outputs"))
    log_file: Path = field(default_factory=lambda: Path(__file__).parent / "logs" / f"{Path(__file__).stem}.log")
    verbosity: int = 2  # Verbosity level: 0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG

    def __post_init__(self):
        """Set default db_path if not provided, then validate."""
        if self.db_path is None:
            self.db_path = str(
                Path(__file__).parent.parent / "storage" / "herbal_info.lmdb"
            )
        # Call parent validation
        super().__post_init__()
# ============================================================================ 
# PYDANTIC MODELS FOR HERBAL INFORMATION STRUCTURE
# ============================================================================ 

class HerbalMetadata(BaseModel):
    """Basic information about the herbal remedy."""
    common_name: str = Field(description="Common name of the herb")
    botanical_name: str = Field(description="Scientific/botanical name (Latin nomenclature)")
    other_names: str = Field(description="Alternative common names and local names, comma-separated")
    plant_family: str = Field(description="Plant family classification (e.g., Asteraceae, Lamiaceae)")
    active_constituents: str = Field(description="Primary active compounds and phytochemicals, comma-separated")
    forms_available: str = Field(description="Available herbal forms (dried leaf, extract, tincture, essential oil, capsule, tea, etc.), comma-separated")


class HerbalClassification(BaseModel):
    """Classification and traditional use categories."""
    traditional_system: str = Field(description="Traditional medicine systems (Ayurveda, Traditional Chinese Medicine, Western Herbalism, etc.), comma-separated")
    primary_uses: str = Field(description="Primary traditional and contemporary uses, comma-separated")
    energetics: str = Field(description="Traditional energetic properties (warming, cooling, drying, moistening, etc.)")
    taste_profile: str = Field(description="Traditional taste attributes (bitter, sweet, pungent, etc.)")


class HerbalBackground(BaseModel):
    """Historical and botanical information."""
    origin_and_habitat: str = Field(description="Geographic origin and natural growing regions")
    history_and_traditional_use: str = Field(description="Historical use patterns and cultural significance across different traditions")
    botanical_description: str = Field(description="Physical characteristics of the plant including appearance, growth patterns, and harvesting information")


class HerbalMechanism(BaseModel):
    """How the herb works in the body."""
    mechanism_of_action: str = Field(description="Proposed biochemical mechanisms of how the herb exerts therapeutic effects")
    active_constituents_effects: str = Field(description="Specific effects of identified active compounds, comma-separated")
    body_systems_affected: str = Field(description="Primary body systems and organs targeted (nervous, digestive, immune, etc.), comma-separated")


class Dosage(BaseModel):
    """Age-specific dosing recommendations."""
    children_dosage: str = Field(description="Dosage for children, often adjusted by age or weight, comma-separated")
    adult_dosage: str = Field(description="Standard dosage for adult use, comma-separated")
    elderly_dosage: str = Field(description="Dosage considerations for elderly or sensitive individuals, comma-separated")


class AdministrationGuidance(BaseModel):
    """Instructions for different forms of administration."""
    tea_infusion: Optional[str] = Field(default=None, description="Instructions for preparing tea: steeping time, water temperature, frequency")
    tincture: Optional[str] = Field(default=None, description="Instructions for tincture use: dilution, dosing, frequency")
    extract: Optional[str] = Field(default=None, description="Instructions for extract or concentrated forms: measuring, mixing, timing")
    topical: Optional[str] = Field(default=None, description="Instructions for external application: preparation, application method, frequency")
    culinary_use: Optional[str] = Field(default=None, description="Instructions for culinary applications and food preparation")


class UsageAndAdministration(BaseModel):
    """Dosing and administration information."""
    suitable_conditions: str = Field(description="Health conditions and situations where this herb is traditionally used")
    preparation_methods: str = Field(description="Common preparation techniques and which forms work best")
    age_specific_dosage: Dosage
    administration_guidance: AdministrationGuidance
    storage_instruction: str = Field(description="Storage requirements, temperature ranges, shelf life, and preservation methods")
    quality_indicators: str = Field(description="What to look for in high-quality herbal products, comma-separated")


class HerbalInteractions(BaseModel):
    """Herb and substance interactions."""
    drug_interactions: str = Field(description="Known interactions with pharmaceutical medications, comma-separated")
    herb_interactions: str = Field(description="Interactions with other herbs and supplements, comma-separated")
    food_interactions: str = Field(description="Known interactions with specific foods, comma-separated")
    caffeine_interactions: str = Field(description="Effects of combining with caffeine or stimulants")
    alcohol_interactions: str = Field(description="Effects of combining with alcohol")


class SafetyInformation(BaseModel):
    """Safety, side effects, and warnings."""
    common_side_effects: str = Field(description="Mild, temporary effects sometimes experienced, comma-separated")
    serious_adverse_effects: str = Field(description="Rare but serious adverse effects to be aware of, comma-separated")
    interactions: HerbalInteractions
    contraindications: str = Field(description="Conditions or situations where herb should be avoided, comma-separated")
    precautions: str = Field(description="Special precautions for specific populations or conditions, comma-separated")
    toxicity_concerns: Optional[str] = Field(default=None, description="Any known toxicity issues or overdose concerns")


class SpecialInstructions(BaseModel):
    """Special situation guidance."""
    discontinuation_guidance: str = Field(description="How to safely stop using the herb and any withdrawal considerations")
    overdose_information: str = Field(description="Symptoms and management if excessive amounts are consumed")
    quality_concerns: str = Field(description="Potential adulterants, contamination risks, and how to verify authenticity")


class SpecialPopulations(BaseModel):
    """Considerations for special populations."""
    pregnancy_use: str = Field(description="Safety and traditional use during pregnancy")
    breastfeeding_use: str = Field(description="Safety and traditional use while breastfeeding")
    pediatric_use: str = Field(description="Age-appropriate use and special considerations for pediatric use")
    kidney_disease_considerations: Optional[str] = Field(default=None, description="Considerations for patients with kidney dysfunction")
    liver_disease_considerations: Optional[str] = Field(default=None, description="Considerations for patients with liver dysfunction")


class Efficacy(BaseModel):
    """Effectiveness and clinical outcomes."""
    traditional_efficacy_claims: str = Field(description="Traditional effectiveness claims and cultural evidence")
    clinical_evidence: str = Field(description="Summary of scientific studies and clinical trial findings")
    onset_of_action: str = Field(description="Expected timeframe for noticing effects")
    duration_of_effect: str = Field(description="How long effects typically last")
    expected_outcomes: str = Field(description="Expected health improvements and benefits, comma-separated")


class Alternatives(BaseModel):
    """Alternative treatment options."""
    similar_herbs: str = Field(description="Other herbs with similar uses and properties, comma-separated")
    complementary_herbs: str = Field(description="Herbs commonly combined with this one, comma-separated")
    non_herbal_alternatives: str = Field(description="Non-herbal treatment alternatives, comma-separated")
    when_to_seek_conventional_care: str = Field(description="Situations where conventional medical care should be prioritized")


class HerbalEducation(BaseModel):
    """Patient education content."""
    plain_language_explanation: str = Field(description="Simple explanation of what this herb does and how it works")
    key_takeaways: str = Field(description="3-5 most important points about using this herb safely and effectively, comma-separated")
    common_misconceptions: str = Field(description="Common myths or misunderstandings about this herb, comma-separated")
    sustainability_notes: str = Field(description="Information about sustainable harvesting and conservation status if relevant")


class CostAndAvailability(BaseModel):
    """Financial and availability information."""
    typical_cost_range: str = Field(description="General cost range for quality products")
    availability: str = Field(description="Regulatory status and availability by region (OTC, dietary supplement, etc.)")
    quality_considerations: str = Field(description="How to identify quality products and reputable sources")
    organic_availability: str = Field(description="Whether organic versions are available and cost differences")
    sourcing_information: str = Field(description="Information about ethical sourcing and fair trade options")


class HerbalEvidence(BaseModel):
    """Evidence-based information."""
    evidence_level: str = Field(description="Quality of scientific evidence (well-established, traditional use only, emerging research, etc.)")
    clinical_studies: str = Field(description="Summary of major scientific studies and research findings")
    regulatory_status: str = Field(description="Regulatory approval status in different countries and FDA classification if applicable")


class HerbalResearch(BaseModel):
    """Current research and innovations."""
    recent_research: str = Field(description="Recent scientific studies and findings, comma-separated")
    ongoing_studies: str = Field(description="Current clinical trials and research areas, comma-separated")
    future_applications: str = Field(description="Potential future uses and research directions, comma-separated")


class HerbalInfo(BaseModel):
    """
    Comprehensive herbal remedy information.
    """
    # Core identification
    metadata: HerbalMetadata

    # Classification and background
    classification: HerbalClassification
    background: HerbalBackground

    # Mechanism and chemistry
    mechanism: HerbalMechanism

    # Usage and administration
    usage_and_administration: UsageAndAdministration

    # Safety and interactions
    safety: SafetyInformation
    special_instructions: SpecialInstructions

    # Specific populations
    special_populations: SpecialPopulations

    # Efficacy and alternatives
    efficacy: Efficacy
    alternatives: Alternatives

    # Patient communication
    education: HerbalEducation

    # Financial and availability
    cost_and_availability: CostAndAvailability

    # Evidence-based information
    evidence: HerbalEvidence

    # Research and innovation
    research: HerbalResearch

# ============================================================================ 
# HERBAL INFO GENERATOR CLASS
# ============================================================================ 

class HerbalInfoGenerator:
    """Generate comprehensive information for herbal remedies."""

    def __init__(self, config: Optional[Config] = None):
        """Initialize the generator with a configuration."""
        self.config = config or Config()

        # Apply verbosity level to logger
        verbosity_levels = {0: "CRITICAL", 1: "ERROR", 2: "WARNING", 3: "INFO", 4: "DEBUG"}
        level = verbosity_levels.get(self.config.verbosity, "WARNING")
        logger.setLevel(level)
        logging.getLogger().setLevel(level)
        logging.getLogger("medkit").setLevel(level)
        logging.getLogger("medkit.core.gemini_client").setLevel(level)

        # Load model name from ModuleConfig


        try:


            module_config = get_module_config("herbal_info")


            model_name = module_config.model_name


        except ValueError:


            # Fallback to default if not registered yet


            model_name = "gemini-1.5-flash"


        


        self.client = MedKitClient(model_name=model_name)
        self.herb_name: Optional[str] = None
        self.output_path: Optional[Path] = None

    def generate(self, herb_name: str, output_path: Optional[Path] = None) -> HerbalInfo:
        """
        Generate and save comprehensive herbal information.

        Args:
            herb_name: Name of the herb.
            output_path: Optional path to save the JSON output.

        Returns:
            The generated HerbalInfo object.
        
        Raises:
            ValueError: If herb_name is empty.
        """
        if not herb_name or not herb_name.strip():
            raise ValueError("Herb name cannot be empty")

        self.herb_name = herb_name

        if output_path is None:
            output_path = self.config.output_dir / f"{herb_name.lower().replace(' ', '_')}_info.json"
        
        self.output_path = output_path

        logger.info(f"Starting herbal information generation for: {herb_name}")

        herbal_info = self._generate_info()

        self.save(herbal_info, self.output_path)
        self.print_summary(herbal_info)
        
        return herbal_info

    def _generate_info(self) -> HerbalInfo:
        """Generates the herbal information."""
        prompt = f"""Generate comprehensive herbal information for: {self.herb_name}

Include detailed information about:
1. Herb name (common and botanical names)
2. Plant family and active constituents
3. Traditional uses and classification
4. Mechanism of action and energetics
5. Forms and preparation methods
6. Dosage and usage guidelines
7. Safety, side effects, and contraindications
8. Interactions with medicines and foods
9. Special populations and precautions
10. Research evidence and efficacy
11. Cost and availability information

Provide accurate, evidence-based herbal remedy information."""

        result = self.client.generate_text(
            prompt,
            schema=HerbalInfo
        )
        return result

    def save(self, herbal_info: HerbalInfo, output_path: Path) -> Path:
        """
        Save the generated herbal information to a JSON file.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(herbal_info.model_dump(), f, indent=2)
        
        logger.info(f"✓ Herbal information saved to {output_path}")
        return output_path

    def print_summary(self, herbal_info: HerbalInfo) -> None:
        """
        Print a summary of the generated herbal information.
        """
        if not self.config.verbose:
            return

        print("\n" + "="*70)
        print(f"HERBAL INFORMATION SUMMARY: {herbal_info.metadata.common_name}")
        print("="*70)
        print(f"  - Botanical Name: {herbal_info.metadata.botanical_name}")
        print(f"  - Plant Family: {herbal_info.metadata.plant_family}")
        print(f"  - Primary Uses: {herbal_info.classification.primary_uses}")
        print(f"\n✓ Generation complete. Saved to {self.output_path}")

def get_herbal_info(herb_name: str, output_path: Optional[Path] = None, verbose: bool = False) -> HerbalInfo:
    """
    High-level function to generate and optionally save herbal information.

    Args:
        herb_name: Name of the herb to generate information for.
        output_path: Optional path to save the output JSON file.
        verbose: If True, show console output and logging.
    """
    config = Config(verbose=verbose)
    generator = HerbalInfoGenerator(config)
    return generator.generate(herb_name, output_path)


def main():
    parser = argparse.ArgumentParser(description="Generate comprehensive information for an herbal remedy.")
    parser.add_argument("-i", "--herbal", type=str, required=True, help="The name of the herb to generate information for.")
    parser.add_argument("-o", "--output", type=str, help="Optional: The path to save the output JSON file.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show verbose console output and logging.")

    args = parser.parse_args()

    print(f"Herbal:{args.herbal}")
    get_herbal_info(args.herbal, args.output, verbose=args.verbose)
    print(f"Successful: output stored in output/{args.output}")
   
if __name__ == "__main__":
   main()

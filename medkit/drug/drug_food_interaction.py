"""Drug-Food Interaction Checker - Comprehensive medication-food interaction analysis.

Analyzes potential interactions between medicines and food/beverage categories with severity
assessment, clinical mechanisms, management recommendations, and patient-friendly guidance
for safe medication-diet coordination.

QUICK START:
    from drug_food_interaction import DrugFoodInteraction, DrugFoodInteractionConfig

    config = DrugFoodInteractionConfig(medicine_name="Warfarin", age=65)
    interaction = DrugFoodInteraction(config).analyze()

    print(f"Severity: {interaction.interaction_details.overall_severity}")
    print(f"Foods to avoid: {interaction.interaction_details.foods_to_avoid}")

COMMON USES:
    - Check medicines for harmful food/beverage interactions
    - Generate patient education materials on safe food-drug combinations
    - Provide clinical recommendations for timing medicine with meals
    - Assess interaction severity (NONE, MINOR, MILD, MODERATE, SIGNIFICANT, CONTRAINDICATED)
    - Create interaction reports for dietary counseling and pharmacy review

KEY CONCEPTS:
    - FoodCategory covers 10 categories (citrus, dairy, alcohol, caffeine, leafy greens, etc.)
    - InteractionSeverity levels with mechanism explanation and timing recommendations
    - FoodCategoryInteraction provides specific foods and absorption/metabolism effects
    - PatientFriendlySummary with plain-language explanation and warning signs
"""

import logging
import sys
import json
import argparse
from enum import Enum
from pathlib import Path
from pydantic import BaseModel, Field, validator
from typing import Optional

from medkit.core.medkit_client import MedKitClient
from medkit.core.module_config import get_module_config
from medkit.utils.storage_config import StorageConfig
from medkit.utils.pydantic_prompt_generator import PromptStyle
from medkit.utils.logging_config import setup_logger

import hashlib
from medkit.utils.lmdb_storage import LMDBStorage, LMDBConfig
from dataclasses import dataclass, field

# Configure logging
logger = setup_logger(__name__)
logger.info("="*80)
logger.info("Drug-Food Interaction Module Initialized")
logger.info("="*80)


class FoodCategory(str, Enum):
    """Food and beverage categories for interaction analysis."""
    CITRUS_FRUITS = "Citrus Fruits"
    BERRIES_OTHER_FRUITS = "Berries & Other Fruits"
    DAIRY_CALCIUM = "Dairy & Calcium-rich Foods"
    HIGH_FAT_FOODS = "High-Fat Foods"
    LEAFY_GREENS = "Leafy Greens (Vitamin K)"
    ALCOHOL = "Alcohol"
    CAFFEINE = "Caffeine"
    HERBAL_SUPPLEMENTS = "Herbal Supplements & Teas"
    NUTS_SEEDS = "Nuts & Seeds"
    SPICES_SEASONINGS = "Spices & Seasonings"


class InteractionSeverity(str, Enum):
    """Severity levels for drug-food interactions."""
    NONE = "NONE"
    MINOR = "MINOR"
    MILD = "MILD"
    MODERATE = "MODERATE"
    SIGNIFICANT = "SIGNIFICANT"
    CONTRAINDICATED = "CONTRAINDICATED"


class ConfidenceLevel(str, Enum):
    """Confidence levels in interaction assessment."""
    HIGH = "HIGH"
    MODERATE = "MODERATE"
    LOW = "LOW"


class DataSourceType(str, Enum):
    """Types of data sources for interaction information."""
    CLINICAL_STUDIES = "Clinical Studies"
    PHARMACOKINETIC_ANALYSIS = "Pharmacokinetic Analysis"
    FDA_WARNINGS = "FDA Warnings"
    MANUFACTURER_DATA = "Manufacturer Data"
    AI_GENERATED = "AI-Generated"


class FoodCategoryInteraction(BaseModel):
    """Detailed interaction information for a specific food category."""
    category: FoodCategory = Field(description="Food category being analyzed")
    has_interaction: bool = Field(description="Whether an interaction exists with this food category")
    severity: InteractionSeverity = Field(
        description="Severity of interaction if present (NONE if no interaction)"
    )
    specific_foods: str = Field(
        description="Specific foods/beverages in this category that interact, comma-separated"
    )
    mechanism: Optional[str] = Field(
        default=None,
        description="How the food affects the medicine (absorption, metabolism, elimination)"
    )
    timing_recommendation: Optional[str] = Field(
        default=None,
        description="Recommended timing (e.g., 'take 2 hours before food', 'take with meals')"
    )


class DrugFoodInteractionDetails(BaseModel):
    """Comprehensive drug-food interaction analysis."""
    medicine_name: str = Field(description="Name of the medicine")
    overall_severity: InteractionSeverity = Field(
        description="Overall severity considering all food interactions"
    )
    mechanism_of_interaction: str = Field(
        description="Detailed explanation of how food affects drug absorption, metabolism, or efficacy"
    )
    clinical_effects: str = Field(
        description="Observable clinical effects of food-drug interactions, comma-separated"
    )
    food_category_interactions: list[FoodCategoryInteraction] = Field(
        description="Detailed interactions for each food category"
    )
    management_recommendations: str = Field(
        description="Clinical recommendations for managing interactions (timing, food avoidance, monitoring), comma-separated"
    )
    foods_to_avoid: str = Field(
        description="Specific foods and beverages to avoid or limit, comma-separated"
    )
    foods_safe_to_consume: str = Field(
        description="Foods and beverages that are generally safe or beneficial, comma-separated"
    )
    confidence_level: ConfidenceLevel = Field(
        description="Confidence level in this interaction assessment (HIGH, MODERATE, LOW)"
    )
    data_source_type: DataSourceType = Field(
        description="Primary source of this interaction data"
    )
    references: Optional[str] = Field(
        default=None,
        description="Citations or references supporting this interaction data, comma-separated"
    )


class PatientFriendlySummary(BaseModel):
    """Patient-friendly explanation of drug-food interactions."""
    simple_explanation: str = Field(
        description="Simple, non-technical explanation of how food affects this medicine"
    )
    what_patient_should_do: str = Field(
        description="Clear action steps for safe food and medicine use"
    )
    foods_to_avoid_simple: str = Field(
        description="Patient-friendly list of foods/drinks to avoid"
    )
    meal_timing_guidance: str = Field(
        description="Guidance on when to take medicine relative to meals"
    )
    warning_signs: str = Field(
        description="Symptoms indicating the interaction may be problematic, comma-separated"
    )


class DataAvailabilityInfo(BaseModel):
    """Information about data availability."""
    data_available: bool = Field(
        description="Whether food interaction data is available"
    )
    reason: Optional[str] = Field(
        default=None,
        description="Explanation if data is not available"
    )


class DrugFoodInteractionResult(BaseModel):
    """
    Comprehensive drug-food interaction analysis result.

    Combines clinical data, patient education, and detailed category information
    in a structured format for healthcare professionals and patients.
    """
    interaction_details: Optional[DrugFoodInteractionDetails] = Field(
        default=None,
        description="Detailed interaction information (None if data not available)"
    )
    technical_summary: str = Field(
        description="Technical summary of the interactions suitable for healthcare professionals"
    )
    patient_friendly_summary: Optional[PatientFriendlySummary] = Field(
        default=None,
        description="Patient-friendly explanation (None if no interactions)"
    )
    data_availability: DataAvailabilityInfo = Field(
        description="Status of data availability for this interaction check"
    )


@dataclass
class DrugFoodInteractionConfig(StorageConfig):
    """
    Configuration for drug_food_interaction.

    Inherits from StorageConfig for LMDB database settings:
    - db_path: Auto-generated path to drug_food_interaction.lmdb
    - db_capacity_mb: Database capacity (default 500 MB)
    - db_store: Whether to cache results (default True)
    - db_overwrite: Whether to refresh cache (default False)
    """
    """Configuration for drug-food interaction analysis."""
    output_path: Optional[Path] = None
    verbosity: bool = False
    prompt_style: PromptStyle = PromptStyle.DETAILED
    enable_cache: bool = True

    def __post_init__(self):
        """Set default db_path if not provided, then validate."""
        if self.db_path is None:
            self.db_path = str(
                Path(__file__).parent.parent / "storage" / "drug_food_interaction.lmdb"
            )
        # Call parent validation
        super().__post_init__()

class DrugFoodInteraction:
    """Analyzes drug-food interactions based on provided configuration."""

    def __init__(self, config: DrugFoodInteractionConfig):
        self.config = config

        # Load model name from ModuleConfig
        try:
            module_config = get_module_config("drug_food_interaction")
            model_name = module_config.model_name
        except ValueError:
            # Fallback to default if not registered yet
            model_name = "gemini-1.5-flash"

        self.client = MedKitClient(model_name=model_name)

    def analyze(
        self,
        medicine_name: str,
        diet_type: Optional[str] = None,
        medical_conditions: Optional[str] = None,
        age: Optional[int] = None,
        specific_food: Optional[str] = None,
    ) -> DrugFoodInteractionResult:
        """
        Analyzes how food and beverages interact with a medicine.

        Args:
            medicine_name: Name of the medicine
            diet_type: Patient's diet type (optional)
            medical_conditions: Patient's medical conditions (optional, comma-separated)
            age: Patient's age in years (optional, 0-150)
            specific_food: Specific food(s) to check for interactions (optional, comma-separated)

        Returns:
            DrugFoodInteractionResult: Comprehensive interaction analysis with management recommendations
        """
        # Validate inputs
        if not medicine_name or not medicine_name.strip():
            raise ValueError("Medicine name cannot be empty")
        if age is not None and (age < 0 or age > 150):
            raise ValueError("Age must be between 0 and 150 years")

        logger.info("-" * 80)
        logger.info(f"Starting drug-food interaction analysis")
        logger.info(f"Medicine: {medicine_name}")
        logger.info(f"Prompt Style: {self.config.prompt_style.value if hasattr(self.config.prompt_style, 'value') else self.config.prompt_style}")

        output_path = self.config.output_path
        if output_path is None:
            medicine_clean = medicine_name.lower().replace(' ', '_')
            output_path = Path("outputs") / f"{medicine_clean}_food_interaction.json"

        output_path.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Output path: {output_path}")

        context_parts = [f"Analyzing food interactions for {medicine_name}"]
        if specific_food:
            context_parts.append(f"Specific foods to check: {specific_food}")
            logger.info(f"Specific foods: {specific_food}")
        if diet_type:
            context_parts.append(f"Patient diet type: {diet_type}")
            logger.info(f"Diet type: {diet_type}")
        if age is not None:
            context_parts.append(f"Patient age: {age} years")
            logger.info(f"Patient age: {age}")
        if medical_conditions:
            context_parts.append(f"Patient conditions: {medical_conditions}")
            logger.info(f"Medical conditions: {medical_conditions}")

        context = ". ".join(context_parts) + "."
        logger.debug(f"Context: {context}")

        logger.info("Calling MedKitClient.generate_text()...")
        try:
            result = self.client.generate_text(
                prompt=f"{medicine_name} food and beverage interactions analysis. {context}",
                schema=DrugFoodInteractionResult,
            )

            logger.info(f"✓ Successfully analyzed food interactions")
            logger.info(f"Overall Severity: {result.interaction_details.overall_severity if result.interaction_details else 'N/A'}")
            logger.info(f"Data Available: {result.data_availability.data_available}")
            logger.info("-" * 80)
            return result
        except Exception as e:
            logger.error(f"✗ Error analyzing food interactions: {e}")
            logger.exception("Full exception details:")
            logger.info("-" * 80)
            raise


def get_drug_food_interaction(
    medicine_name: str,
    config: DrugFoodInteractionConfig,
    diet_type: Optional[str] = None,
    medical_conditions: Optional[str] = None,
    age: Optional[int] = None,
    specific_food: Optional[str] = None,
) -> DrugFoodInteractionResult:
    """
    Get drug-food interaction analysis.

    This is a convenience function that instantiates and runs the
    DrugFoodInteraction analyzer.

    Args:
        medicine_name: Name of the medicine
        config: Configuration object for the analysis
        diet_type: Patient's diet type (optional)
        medical_conditions: Patient's medical conditions (optional)
        age: Patient's age in years (optional)
        specific_food: Specific food(s) to check for interactions (optional)

    Returns:
        DrugFoodInteractionResult: The result of the analysis
    """
    analyzer = DrugFoodInteraction(config)
    return analyzer.analyze(
        medicine_name=medicine_name,
        diet_type=diet_type,
        medical_conditions=medical_conditions,
        age=age,
        specific_food=specific_food,
    )


def get_user_options():
    """
    Get user options through interactive prompts.

    Returns:
        dict: Dictionary containing user-provided options
    """
    print("=" * 80)
    print("DRUG-FOOD INTERACTION CHECKER")
    print("=" * 80 + "\n")

    # Get medicine name (required)
    while True:
        medicine_name = input("Enter medicine name (required): ").strip()
        if medicine_name:
            break
        print("Medicine name cannot be empty. Please try again.\n")

    # Get optional parameters
    diet_type = input("Enter patient's diet type (optional, e.g., vegetarian): ").strip() or None

    age = None
    while True:
        age_input = input("Enter patient's age in years (optional, 0-150): ").strip()
        if not age_input:
            break
        try:
            age = int(age_input)
            if 0 <= age <= 150:
                break
            print("Age must be between 0 and 150. Please try again.\n")
        except ValueError:
            print("Please enter a valid number.\n")

    medical_conditions = input("Enter patient's medical conditions (optional, comma-separated): ").strip() or None

    output_path = input("Enter output file path (optional): ").strip() or None
    output_path = Path(output_path) if output_path else None

    prompt_style_input = input("Enter prompt style (detailed/concise/balanced, default: detailed): ").strip().lower() or "detailed"

    verbose = input("Enable verbose logging? (y/n, default: n): ").strip().lower() == "y"
    json_output = input("Output results as JSON to stdout? (y/n, default: n): ").strip().lower() == "y"

    return {
        "medicine_name": medicine_name,
        "diet_type": diet_type,
        "age": age,
        "medical_conditions": medical_conditions,
        "output_path": output_path,
        "prompt_style": prompt_style_input,
        "verbose": verbose,
        "json_output": json_output,
    }


def create_cli_parser() -> argparse.ArgumentParser:
    """
    Create and configure the argument parser for the CLI.

    Returns:
        argparse.ArgumentParser: Configured parser for command-line arguments
    """
    parser = argparse.ArgumentParser(
        description="Drug-Food Interaction Checker - Analyze interactions between medicines and foods",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic analysis
  python drug_food_interaction.py "Warfarin"

  # With patient details
  python drug_food_interaction.py "Metformin" --age 65 --conditions "kidney disease"

  # With diet type
  python drug_food_interaction.py "Aspirin" --diet-type vegetarian --age 45

  # With custom output
  python drug_food_interaction.py "Simvastatin" --output results.json --verbose
        """,
    )

    # Required arguments
    parser.add_argument(
        "medicine_name",
        type=str,
        help="Name of the medicine to analyze",
    )

    # Optional arguments
    parser.add_argument(
        "--diet-type",
        dest="diet_type",
        type=str,
        default=None,
        help="Patient's diet type (e.g., vegetarian, vegan, kosher)",
    )

    parser.add_argument(
        "--age",
        "-a",
        type=int,
        default=None,
        help="Patient's age in years (0-150)",
    )

    parser.add_argument(
        "--conditions",
        "-c",
        type=str,
        default=None,
        help="Patient's medical conditions (comma-separated)",
    )

    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=None,
        help="Output file path for results",
    )

    parser.add_argument(
        "--prompt-style",
        "-p",
        type=str,
        choices=["detailed", "concise", "balanced"],
        default="detailed",
        help="Prompt style for analysis (default: detailed)",
    )

    parser.add_argument(
        "--no-schema",
        action="store_true",
        help="Disable schema-based prompt generation",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    parser.add_argument(
        "--json-output",
        action="store_true",
        help="Output results as JSON to stdout",
    )

    return parser


def parse_prompt_style(style_str: str) -> PromptStyle:
    """
    Parse prompt style string to PromptStyle enum.

    Args:
        style_str: String representation of prompt style

    Returns:
        PromptStyle: The corresponding enum value

    Raises:
        ValueError: If style string is not a valid prompt style
    """
    style_mapping = {
        "detailed": PromptStyle.DETAILED,
        "concise": PromptStyle.CONCISE,
        "balanced": PromptStyle.BALANCED,
    }

    if style_str.lower() not in style_mapping:
        raise ValueError(
            f"Invalid prompt style: {style_str}. "
            f"Choose from: {', '.join(style_mapping.keys())}"
        )

    return style_mapping[style_str.lower()]


def print_results(result: DrugFoodInteractionResult, verbose: bool = False) -> None:
    """
    Print interaction analysis results in a formatted manner.

    Args:
        result: The analysis result to print
        verbose: Whether to print detailed information
    """
    print("\n" + "=" * 80)
    print("DRUG-FOOD INTERACTION ANALYSIS RESULTS")
    print("=" * 80 + "\n")

    # Print data availability
    if not result.data_availability.data_available:
        print(f"⚠️  Data Availability: {result.data_availability.reason}")
        print("=" * 80 + "\n")
        return

    # Print interaction details
    if result.interaction_details:
        details = result.interaction_details
        print(f"Medicine: {details.medicine_name}")
        print(f"Overall Severity: {details.overall_severity.value}")
        print(f"Confidence Level: {details.confidence_level.value}")
        print(f"Data Source: {details.data_source_type.value}\n")

        # Print mechanism of interaction
        print("MECHANISM OF INTERACTION:")
        print("-" * 80)
        print(f"{details.mechanism_of_interaction}\n")

        # Print clinical effects
        print("CLINICAL EFFECTS:")
        print("-" * 80)
        effects = [f"  • {effect.strip()}" for effect in details.clinical_effects.split(",")]
        print("\n".join(effects) + "\n")

        # Print foods to avoid
        print("FOODS TO AVOID:")
        print("-" * 80)
        foods_avoid = [f"  • {food.strip()}" for food in details.foods_to_avoid.split(",")]
        print("\n".join(foods_avoid) + "\n")

        # Print safe foods
        print("FOODS SAFE TO CONSUME:")
        print("-" * 80)
        foods_safe = [f"  • {food.strip()}" for food in details.foods_safe_to_consume.split(",")]
        print("\n".join(foods_safe) + "\n")

        # Print management recommendations
        print("MANAGEMENT RECOMMENDATIONS:")
        print("-" * 80)
        recommendations = [f"  • {rec.strip()}" for rec in details.management_recommendations.split(",")]
        print("\n".join(recommendations) + "\n")

        # Print detailed category interactions if verbose
        if verbose:
            print("DETAILED CATEGORY INTERACTIONS:")
            print("-" * 80)
            for interaction in details.food_category_interactions:
                if interaction.has_interaction:
                    print(f"\n{interaction.category.value}:")
                    print(f"  Severity: {interaction.severity.value}")
                    print(f"  Foods: {interaction.specific_foods}")
                    if interaction.mechanism:
                        print(f"  Mechanism: {interaction.mechanism}")
                    if interaction.timing_recommendation:
                        print(f"  Timing: {interaction.timing_recommendation}")

    # Print patient-friendly summary
    if result.patient_friendly_summary:
        summary = result.patient_friendly_summary
        print("\n" + "=" * 80)
        print("PATIENT-FRIENDLY GUIDANCE")
        print("=" * 80 + "\n")

        print("SIMPLE EXPLANATION:")
        print("-" * 80)
        print(f"{summary.simple_explanation}\n")

        print("WHAT YOU SHOULD DO:")
        print("-" * 80)
        print(f"{summary.what_patient_should_do}\n")

        print("MEAL TIMING GUIDANCE:")
        print("-" * 80)
        print(f"{summary.meal_timing_guidance}\n")

        print("WARNING SIGNS:")
        print("-" * 80)
        warning_signs = [f"  • {sign.strip()}" for sign in summary.warning_signs.split(",")]
        print("\n".join(warning_signs) + "\n")

    # Print technical summary
    print("\n" + "=" * 80)
    print("TECHNICAL SUMMARY")
    print("=" * 80 + "\n")
    print(result.technical_summary + "\n")

    print("=" * 80)


def main() -> int:
    """
    Main entry point for the drug-food interaction CLI.

    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    parser = create_cli_parser()
    args = parser.parse_args()

    # Configure logging verbosity
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    try:
        # Parse prompt style
        prompt_style = parse_prompt_style(args.prompt_style)

        # Create configuration
        config = DrugFoodInteractionConfig(
            medicine_name=args.medicine_name,
            diet_type=args.diet_type,
            medical_conditions=args.conditions,
            age=args.age,
            output_path=args.output,
            use_schema_prompt=not args.no_schema,
            prompt_style=prompt_style,
        )

        logger.info(f"Configuration created successfully")

        # Run analysis
        analyzer = DrugFoodInteraction(config)
        result = analyzer.analyze()

        # Print results
        print_results(result, verbose=args.verbose)

        # Save results to file
        if args.output:
            output_path = args.output
        else:
            medicine_clean = args.medicine_name.lower().replace(' ', '_')
            output_path = Path("outputs") / f"{medicine_clean}_food_interaction.json"

        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w") as f:
            f.write(result.model_dump_json(indent=2))

        logger.info(f"✓ Results saved to {output_path}")
        print(f"\n✓ Results saved to: {output_path}")

        # Output JSON to stdout if requested
        if args.json_output:
            print(f"\n{result.model_dump_json(indent=2)}")

        return 0

    except ValueError as e:
        print(f"\n❌ Invalid input: {e}", file=sys.stderr)
        logger.error(f"Invalid input: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        logger.error(f"Unexpected error: {e}")
        logger.exception("Full exception details:")
        return 1


if __name__ == "__main__":
    sys.exit(main())

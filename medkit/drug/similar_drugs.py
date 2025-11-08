"""
similar_drugs.py - Similar Medicines Finder and Comparator

Find alternative medicines with similar active ingredients, therapeutic classes, and
mechanisms of action. Provides detailed comparisons of top 10-15 alternatives to help
identify suitable substitutes using structured data and MedKit AI analysis.

This module helps identify appropriate alternative medications when the primary drug is
unavailable, contraindicated, or causing adverse effects.

QUICK START:
    from similar_drugs import SimilarDrugs, SimilarDrugsConfig

    # Configure the analysis (settings only)
    config = SimilarDrugsConfig(
        output_path=None,  # optional
        verbosity=False,
        prompt_style="DETAILED"
    )

    # Create an analyzer and get the alternatives
    alternatives = SimilarDrugs(config).find(
        medicine_name="ibuprofen",
        include_generics=True
    )

    # Review similar options
    for category in alternatives.categorized_results:
        for drug in category.medicines[:3]:
            print(f"{drug.medicine_name}: {drug.similarity_category.value}")
            print(f"  Efficacy: {drug.efficacy_comparison.value}")

COMMON USES:
    1. Find alternative medications when primary drug is unavailable
    2. Identify options when patient has contraindications
    3. Compare efficacy and side effects of similar drugs
    4. Support medication selection decisions
    5. Generate patient education on medication alternatives
    6. Manage drug allergies with suitable substitutes

SIMILARITY BASIS:
    - SAME_INGREDIENT: Contains the same active ingredient
    - SAME_THERAPEUTIC_CLASS: Treats the same conditions similarly
    - SIMILAR_MECHANISM: Works through similar pharmacological mechanisms

KEY INFORMATION PROVIDED:
    - Alternative medicine names
    - Similarity basis and strength
    - Efficacy comparison to original drug
    - Availability and cost considerations
    - Substitutability rating
    - Important considerations for switching
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
logger.info("Similar Drugs Module Initialized")
logger.info("="*80)


class SimilarityCategory(str, Enum):
    """Categories of similarity between medicines."""
    SAME_INGREDIENT = "Same Active Ingredient"
    SAME_THERAPEUTIC_CLASS = "Same Therapeutic Class"
    SIMILAR_MECHANISM = "Similar Mechanism of Action"


class EfficacyComparison(str, Enum):
    """Efficacy comparison relative to original drug."""
    LESS_EFFECTIVE = "Less Effective"
    SIMILAR_EFFICACY = "Similar Efficacy"
    MORE_EFFECTIVE = "More Effective"
    EFFICACY_VARIES = "Varies by Indication"


class SimilarMedicineDetail(BaseModel):
    """Detailed information about a similar medicine."""
    rank: int = Field(description="Ranking of similarity (1 being most similar)")
    medicine_name: str = Field(description="Name of the similar medicine")
    brand_names: Optional[str] = Field(
        default=None,
        description="Brand names or trade names, comma-separated"
    )
    active_ingredients: str = Field(
        description="Active pharmaceutical ingredients, comma-separated"
    )
    available_strengths: str = Field(
        description="Available dosage strengths, comma-separated"
    )
    available_forms: str = Field(
        description="Available pharmaceutical forms (tablet, capsule, liquid, etc.), comma-separated"
    )
    similarity_category: SimilarityCategory = Field(
        description="Category of similarity (same ingredient, class, or mechanism)"
    )
    similarity_score: float = Field(
        description="Similarity score (0-100) indicating how similar to original drug",
        ge=0,
        le=100
    )
    efficacy_comparison: EfficacyComparison = Field(
        description="How efficacy compares to original medicine"
    )
    onset_of_action: str = Field(
        description="How quickly the medicine starts working"
    )
    duration_of_effect: str = Field(
        description="How long the effects typically last"
    )
    common_side_effects: str = Field(
        description="Most commonly reported side effects, comma-separated"
    )
    typical_cost_range: str = Field(
        description="Typical cost range without insurance"
    )
    generic_available: bool = Field(
        description="Whether generic version is available"
    )
    key_advantages: str = Field(
        description="Key advantages compared to original drug, comma-separated"
    )
    key_disadvantages: str = Field(
        description="Key disadvantages compared to original drug, comma-separated"
    )
    when_to_prefer: str = Field(
        description="Clinical situations or patient types where this medicine might be preferred"
    )


class SimilarMedicinesCategory(BaseModel):
    """Grouped similar medicines by category."""
    category: SimilarityCategory = Field(description="Category of similarity")
    count: int = Field(description="Number of similar medicines in this category (from top 10-15)")
    medicines: list[SimilarMedicineDetail] = Field(
        description="List of similar medicines in this category (ranked by similarity)"
    )
    category_summary: str = Field(
        description="Summary of this category and its relevance"
    )


class SwitchingGuidance(BaseModel):
    """Guidance for switching from original medicine to alternative."""
    switching_considerations: str = Field(
        description="Important factors to consider when switching, comma-separated"
    )
    transition_recommendations: str = Field(
        description="How to transition from original to alternative medicine"
    )
    monitoring_during_switch: str = Field(
        description="What to monitor during transition, comma-separated"
    )
    contraindications_for_switch: str = Field(
        description="Situations where switching should be avoided or done carefully, comma-separated"
    )


class SimilarMedicinesResult(BaseModel):
    """
    Complete results of similar medicines search (top 10-15 alternatives).

    Provides alternatives organized by similarity category with detailed
    information for each alternative and switching guidance.
    """
    original_medicine: str = Field(description="Name of the original medicine being analyzed")
    original_active_ingredients: str = Field(
        description="Active ingredients in original medicine"
    )
    original_therapeutic_use: str = Field(
        description="Primary therapeutic indication of original medicine"
    )
    total_similar_medicines_found: int = Field(
        description="Total number of top similar medicines identified (10-15)"
    )
    categorized_results: list[SimilarMedicinesCategory] = Field(
        description="Similar medicines organized by similarity category, ranked by similarity score"
    )
    switching_guidance: SwitchingGuidance = Field(
        description="General guidance for switching medicines"
    )
    top_recommended: str = Field(
        description="Top 3 most recommended alternatives with brief rationale"
    )
    summary_analysis: str = Field(
        description="Overall analysis of top alternatives and key considerations"
    )
    clinical_notes: str = Field(
        description="Important clinical notes and evidence-based considerations for switching"
    )


@dataclass
class SimilarDrugsConfig(StorageConfig):
    """
    Configuration for similar_drugs.

    Inherits from StorageConfig for LMDB database settings:
    - db_path: Auto-generated path to similar_drugs.lmdb
    - db_capacity_mb: Database capacity (default 500 MB)
    - db_store: Whether to cache results (default True)
    - db_overwrite: Whether to refresh cache (default False)
    """
    """Configuration for finding similar drugs."""
    output_path: Optional[Path] = None
    verbosity: bool = False
    prompt_style: PromptStyle = PromptStyle.DETAILED
    enable_cache: bool = True

    def __post_init__(self):
        """Set default db_path if not provided, then validate."""
        if self.db_path is None:
            self.db_path = str(
                Path(__file__).parent.parent / "storage" / "similar_drugs.lmdb"
            )
        # Call parent validation
        super().__post_init__()

class SimilarDrugs:
    """Finds similar drugs based on provided configuration."""

    def __init__(self, config: SimilarDrugsConfig):
        self.config = config

        # Load model name from ModuleConfig
        try:
            module_config = get_module_config("similar_drugs")
            model_name = module_config.model_name
        except ValueError:
            # Fallback to default if not registered yet
            model_name = "gemini-1.5-flash"

        self.client = MedKitClient(model_name=model_name)

    def find(
        self,
        medicine_name: str,
        include_generics: bool = True,
        patient_age: Optional[int] = None,
        patient_conditions: Optional[str] = None,
    ) -> SimilarMedicinesResult:
        """
        Finds top 10-15 medicines similar to a given medicine.

        Args:
            medicine_name: Name of the medicine to find alternatives for
            include_generics: Whether to include generic formulations (default: True)
            patient_age: Patient's age in years (optional, 0-150)
            patient_conditions: Patient's medical conditions (optional, comma-separated)

        Returns:
            SimilarMedicinesResult: Top 10-15 similar medicines with detailed information
        """
        # Validate inputs
        if not medicine_name or not medicine_name.strip():
            raise ValueError("Medicine name cannot be empty")
        if patient_age is not None and (patient_age < 0 or patient_age > 150):
            raise ValueError("Age must be between 0 and 150 years")

        output_path = self.config.output_path
        if output_path is None:
            medicine_clean = medicine_name.lower().replace(' ', '_')
            output_path = Path("outputs") / f"{medicine_clean}_similar_medicines.json"

        output_path.parent.mkdir(parents=True, exist_ok=True)

        context_parts = [f"Finding top 10-15 medicines similar to {medicine_name}"]
        if include_generics:
            context_parts.append("Include generic formulations")
        if patient_age is not None:
            context_parts.append(f"Patient age: {patient_age} years")
        if patient_conditions:
            context_parts.append(f"Patient conditions: {patient_conditions}")

        context = ". ".join(context_parts) + "."

        result = self.client.generate_text(
            prompt=f"Find the top 10-15 most similar medicines to {medicine_name} - prioritize same active ingredients, then therapeutic class, then similar mechanism. {context}",
            schema=SimilarMedicinesResult,
        )

        return result


def get_similar_medicines(
    medicine_name: str,
    config: SimilarDrugsConfig,
    include_generics: bool = True,
    patient_age: Optional[int] = None,
    patient_conditions: Optional[str] = None,
) -> SimilarMedicinesResult:
    """
    Get similar medicines.

    This is a convenience function that instantiates and runs the
    SimilarDrugs finder.

    Args:
        medicine_name: Name of the medicine to find alternatives for
        config: Configuration object for the analysis
        include_generics: Whether to include generic formulations (default: True)
        patient_age: Patient's age in years (optional)
        patient_conditions: Patient's medical conditions (optional)

    Returns:
        SimilarMedicinesResult: The result of the analysis
    """
    finder = SimilarDrugs(config)
    return finder.find(
        medicine_name=medicine_name,
        include_generics=include_generics,
        patient_age=patient_age,
        patient_conditions=patient_conditions,
    )


def create_cli_parser() -> argparse.ArgumentParser:
    """
    Create and configure the argument parser for the CLI.

    Returns:
        argparse.ArgumentParser: Configured parser for command-line arguments
    """
    parser = argparse.ArgumentParser(
        description="Similar Drugs Finder - Find alternative medicines and similar drug options",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic analysis
  python similar_drugs.py "Ibuprofen"

  # Include generics
  python similar_drugs.py "Aspirin" --include-generics

  # With patient details
  python similar_drugs.py "Metformin" --age 65 --conditions "kidney disease, hypertension"

  # With custom output
  python similar_drugs.py "Simvastatin" --output alternatives.json --verbose
        """,
    )

    # Required arguments
    parser.add_argument(
        "medicine_name",
        type=str,
        help="Name of the medicine to find similar alternatives for",
    )

    # Optional arguments
    parser.add_argument(
        "--include-generics",
        action="store_true",
        default=True,
        help="Include generic formulations (default: True)",
    )

    parser.add_argument(
        "--no-generics",
        dest="include_generics",
        action="store_false",
        help="Exclude generic formulations",
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
        type=Path,
        default=None,
        help="Output file path for results (default: outputs/{medicine}_similar_medicines.json)",
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
        "--verbose",
        "-v",
        action="store_true",
        default=False,
        help="Enable verbose logging output",
    )

    parser.add_argument(
        "--json-output",
        "-j",
        action="store_true",
        default=False,
        help="Output results as JSON to stdout (in addition to file)",
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


def print_results(result: SimilarMedicinesResult, verbose: bool = False) -> None:
    """
    Print similar medicines results in a formatted manner.

    Args:
        result: The analysis result to print
        verbose: Whether to print detailed information
    """
    print("\n" + "=" * 80)
    print("SIMILAR MEDICINES ANALYSIS RESULTS")
    print("=" * 80 + "\n")

    # Print original medicine info
    print(f"Original Medicine: {result.original_medicine}")
    print(f"Active Ingredients: {result.original_active_ingredients}")
    print(f"Therapeutic Use: {result.original_therapeutic_use}")
    print(f"Total Similar Medicines Found: {result.total_similar_medicines_found}\n")

    # Print top recommended
    print("TOP RECOMMENDED ALTERNATIVES:")
    print("-" * 80)
    print(f"{result.top_recommended}\n")

    # Print categorized results
    print("SIMILAR MEDICINES BY CATEGORY:")
    print("-" * 80)
    for category in result.categorized_results:
        print(f"\n{category.category.value}:")
        print(f"  Count: {category.count}")
        print(f"  Summary: {category.category_summary}\n")

        if verbose:
            for medicine in category.medicines:
                print(f"  #{medicine.rank} - {medicine.medicine_name}")
                print(f"     Similarity Score: {medicine.similarity_score}%")
                print(f"     Efficacy: {medicine.efficacy_comparison.value}")
                if medicine.brand_names:
                    print(f"     Brand Names: {medicine.brand_names}")
                print(f"     Cost Range: {medicine.typical_cost_range}")
                if medicine.generic_available:
                    print(f"     Generic Available: Yes")

    # Print switching guidance
    print("\n" + "=" * 80)
    print("SWITCHING GUIDANCE")
    print("=" * 80 + "\n")

    print("SWITCHING CONSIDERATIONS:")
    print("-" * 80)
    considerations = [f"  • {c.strip()}" for c in result.switching_guidance.switching_considerations.split(",")]
    print("\n".join(considerations) + "\n")

    print("TRANSITION RECOMMENDATIONS:")
    print("-" * 80)
    print(f"{result.switching_guidance.transition_recommendations}\n")

    print("MONITORING DURING SWITCH:")
    print("-" * 80)
    monitoring = [f"  • {m.strip()}" for m in result.switching_guidance.monitoring_during_switch.split(",")]
    print("\n".join(monitoring) + "\n")

    # Print summary analysis
    print("\n" + "=" * 80)
    print("ANALYSIS SUMMARY")
    print("=" * 80 + "\n")
    print(result.summary_analysis + "\n")

    print("CLINICAL NOTES:")
    print("-" * 80)
    print(result.clinical_notes + "\n")

    print("=" * 80)


def main() -> int:
    """
    Main entry point for the similar drugs CLI.

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
        config = SimilarDrugsConfig(
            output_path=args.output,
            verbosity=args.verbose,
            prompt_style=prompt_style,
        )

        logger.info(f"Configuration created successfully")

        # Run analysis
        analyzer = SimilarDrugs(config)
        result = analyzer.find(
            medicine_name=args.medicine_name,
            include_generics=args.include_generics,
            patient_age=args.age,
            patient_conditions=args.conditions,
        )

        # Print results
        print_results(result, verbose=args.verbose)

        # Save results to file
        if args.output:
            output_path = args.output
        else:
            medicine_clean = args.medicine_name.lower().replace(' ', '_')
            output_path = Path("outputs") / f"{medicine_clean}_similar_medicines.json"

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
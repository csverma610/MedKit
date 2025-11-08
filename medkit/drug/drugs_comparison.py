"""drugs_comparison - Compare medicines side-by-side across clinical, regulatory, and practical metrics.

This module enables comprehensive comparison of two medicines to help healthcare professionals
and patients make informed treatment decisions. It generates structured comparison matrices
with clinical effectiveness data, safety profiles, regulatory information, cost analysis, and
contextual recommendations. All comparisons are powered by the MedKit AI client with validated
Pydantic schemas.

QUICK START:
    from drugs_comparison import DrugsComparison, DrugsComparisonConfig

    config = DrugsComparisonConfig(
        medicine1="Aspirin",
        medicine2="Ibuprofen",
        use_case="pain relief"
    )
    comparison = DrugsComparison(config).compare()
    print(comparison.comparison_summary.more_effective)

COMMON USES:
    1. Drug selection guidance - comparing treatment options with efficacy and safety data
    2. Cost-benefit analysis - evaluating affordability and insurance coverage patterns
    3. Patient education - explaining differences between medication alternatives
    4. Clinical decision support - contextual recommendations by patient age and conditions
    5. Regulatory comparison - comparing FDA approval status and safety warnings

KEY FEATURES AND COVERAGE AREAS:
    - Clinical Metrics: effectiveness ratings, efficacy rates, onset of action, side effects
    - Regulatory Metrics: FDA approval status, approval type, black box warnings, alerts
    - Practical Metrics: availability status, cost ranges, insurance coverage, formulations
    - Comparison Summary: side-by-side analysis of effectiveness, safety, cost, accessibility
    - Contextual Recommendations: tailored guidance for acute/chronic use, age groups, cost-sensitive patients
    - Narrative Analysis: detailed prose comparison of similarities and differences
    - Evidence Quality: assessment of supporting evidence strength
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
logger.info("Drugs Comparison Module Initialized")
logger.info("="*80)


class EffectivenessRating(str, Enum):
    """Effectiveness ratings for a medicine."""
    VERY_LOW = "Very Low"
    LOW = "Low"
    MODERATE = "Moderate"
    HIGH = "High"
    VERY_HIGH = "Very High"


class SafetyRating(str, Enum):
    """Safety ratings for a medicine."""
    VERY_HIGH_RISK = "Very High Risk"
    HIGH_RISK = "High Risk"
    MODERATE_RISK = "Moderate Risk"
    LOW_RISK = "Low Risk"
    VERY_LOW_RISK = "Very Low Risk"


class AvailabilityStatus(str, Enum):
    """Availability status of a medicine."""
    PRESCRIPTION_ONLY = "Prescription Only (Rx)"
    OVER_THE_COUNTER = "Over-the-Counter (OTC)"
    CONTROLLED_SUBSTANCE = "Controlled Substance"
    RESTRICTED_DISTRIBUTION = "Restricted Distribution"
    DISCONTINUED = "Discontinued"


class ClinicalMetrics(BaseModel):
    """Clinical effectiveness and safety metrics for a medicine."""
    medicine_name: str = Field(description="Name of the medicine")
    effectiveness_rating: EffectivenessRating = Field(description="Overall effectiveness rating")
    efficacy_rate: str = Field(description="Clinical efficacy percentage or success rate from studies")
    onset_of_action: str = Field(description="How quickly the medicine starts working")
    duration_of_effect: str = Field(description="How long the effects typically last")
    safety_rating: SafetyRating = Field(description="Overall safety rating")
    common_side_effects: str = Field(description="Most commonly reported side effects, comma-separated")
    serious_side_effects: str = Field(description="Rare but serious adverse effects, comma-separated")
    black_box_warning: Optional[str] = Field(
        default=None,
        description="FDA black box warning if applicable"
    )
    contraindications: str = Field(description="Key contraindications, comma-separated")


class RegulatoryMetrics(BaseModel):
    """Regulatory and approval information for a medicine."""
    medicine_name: str = Field(description="Name of the medicine")
    fda_approval_status: str = Field(description="FDA approval status and indication")
    approval_date: str = Field(description="Date FDA approved the medicine")
    approval_type: str = Field(description="Approval type (e.g., Standard, Accelerated, Breakthrough, Priority)")
    has_black_box_warning: bool = Field(description="Whether medicine has FDA black box warning")
    fda_alerts: str = Field(description="Current FDA alerts or safety warnings, comma-separated")
    generic_available: bool = Field(description="Whether generic version is available")
    generic_date: Optional[str] = Field(
        default=None,
        description="When generic became available (if applicable)"
    )
    patent_expiration: Optional[str] = Field(
        default=None,
        description="Patent expiration date if still under patent"
    )


class PracticalMetrics(BaseModel):
    """Cost, availability, and practical information for a medicine."""
    medicine_name: str = Field(description="Name of the medicine")
    availability_status: AvailabilityStatus = Field(description="Prescription, OTC, controlled, etc.")
    typical_cost_range: str = Field(description="Typical cost range without insurance")
    insurance_coverage: str = Field(description="How typically covered by major insurance")
    available_formulations: str = Field(description="Available pharmaceutical forms, comma-separated")
    dosage_strengths: str = Field(description="Available dosage strengths, comma-separated")
    generic_cost: Optional[str] = Field(
        default=None,
        description="Typical cost of generic version if available"
    )
    patient_assistance_programs: str = Field(
        description="Available manufacturer assistance programs, comma-separated"
    )


class ComparisonSummary(BaseModel):
    """Summary of key differences between two medicines."""
    more_effective: str = Field(description="Which medicine is more effective and why")
    safer_option: str = Field(description="Which medicine has better safety profile and why")
    more_affordable: str = Field(description="Which medicine is more affordable and cost analysis")
    easier_access: str = Field(description="Which medicine is easier to access/obtain")
    key_differences: str = Field(
        description="Top 3-5 key differences between the medicines, comma-separated"
    )


class RecommendationContext(BaseModel):
    """Contextual recommendations for medicine selection."""
    for_acute_conditions: Optional[str] = Field(
        default=None,
        description="Which medicine is better for acute/short-term use and why"
    )
    for_chronic_conditions: Optional[str] = Field(
        default=None,
        description="Which medicine is better for chronic/long-term use and why"
    )
    for_elderly_patients: Optional[str] = Field(
        default=None,
        description="Which medicine is better for elderly patients and why"
    )
    for_cost_sensitive: Optional[str] = Field(
        default=None,
        description="Which medicine is better for cost-sensitive patients and why"
    )
    overall_recommendation: str = Field(
        description="Overall recommendation summary for typical patients"
    )


class MedicinesComparisonResult(BaseModel):
    """
    Comprehensive side-by-side comparison of two medicines.

    Includes clinical, regulatory, and practical metrics with detailed
    narrative analysis and contextual recommendations.
    """
    medicine1_clinical: ClinicalMetrics = Field(description="Clinical metrics for first medicine")
    medicine2_clinical: ClinicalMetrics = Field(description="Clinical metrics for second medicine")

    medicine1_regulatory: RegulatoryMetrics = Field(description="Regulatory metrics for first medicine")
    medicine2_regulatory: RegulatoryMetrics = Field(description="Regulatory metrics for second medicine")

    medicine1_practical: PracticalMetrics = Field(description="Practical metrics for first medicine")
    medicine2_practical: PracticalMetrics = Field(description="Practical metrics for second medicine")

    comparison_summary: ComparisonSummary = Field(description="Summary of key differences")
    recommendations: RecommendationContext = Field(description="Contextual recommendations")

    narrative_analysis: str = Field(
        description="Detailed narrative comparison analyzing similarities and differences"
    )

    evidence_quality: str = Field(
        description="Quality of evidence supporting comparison (high, moderate, low)"
    )

    limitations: str = Field(
        description="Limitations of this comparison and factors to consider, comma-separated"
    )


@dataclass
class DrugsComparisonConfig(StorageConfig):
    """
    Configuration for drugs_comparison.

    Inherits from StorageConfig for LMDB database settings:
    - db_path: Auto-generated path to drugs_comparison.lmdb
    - db_capacity_mb: Database capacity (default 500 MB)
    - db_store: Whether to cache results (default True)
    - db_overwrite: Whether to refresh cache (default False)
    """
    """Configuration for drugs comparison."""
    output_path: Optional[Path] = None
    verbosity: bool = False
    prompt_style: PromptStyle = PromptStyle.DETAILED
    enable_cache: bool = True

    def __post_init__(self):
        """Set default db_path if not provided, then validate."""
        if self.db_path is None:
            self.db_path = str(
                Path(__file__).parent.parent / "storage" / "drugs_comparison.lmdb"
            )
        # Call parent validation
        super().__post_init__()

class DrugsComparison:
    """Compares two medicines based on provided configuration."""

    def __init__(self, config: DrugsComparisonConfig):
        self.config = config

        # Load model name from ModuleConfig
        try:
            module_config = get_module_config("drugs_comparison")
            model_name = module_config.model_name
        except ValueError:
            # Fallback to default if not registered yet
            model_name = "gemini-1.5-flash"

        self.client = MedKitClient(model_name=model_name)

    def compare(
        self,
        medicine1: str,
        medicine2: str,
        use_case: Optional[str] = None,
        patient_age: Optional[int] = None,
        patient_conditions: Optional[str] = None,
    ) -> MedicinesComparisonResult:
        """
        Compares two medicines across clinical, regulatory, and practical metrics.

        Args:
            medicine1: Name of the first medicine
            medicine2: Name of the second medicine
            use_case: Use case or indication for comparison (optional)
            patient_age: Patient's age in years (optional, 0-150)
            patient_conditions: Patient's medical conditions (optional, comma-separated)

        Returns:
            MedicinesComparisonResult: Comprehensive side-by-side comparison
        """
        # Validate inputs
        if not medicine1 or not medicine1.strip():
            raise ValueError("Medicine 1 name cannot be empty")
        if not medicine2 or not medicine2.strip():
            raise ValueError("Medicine 2 name cannot be empty")
        if patient_age is not None and (patient_age < 0 or patient_age > 150):
            raise ValueError("Age must be between 0 and 150 years")

        logger.info("-" * 80)
        logger.info(f"Starting drugs comparison analysis")
        logger.info(f"Medicine 1: {medicine1}")
        logger.info(f"Medicine 2: {medicine2}")
        logger.info(f"Prompt Style: {self.config.prompt_style.value if hasattr(self.config.prompt_style, 'value') else self.config.prompt_style}")

        output_path = self.config.output_path
        if output_path is None:
            medicine1_clean = medicine1.lower().replace(' ', '_')
            medicine2_clean = medicine2.lower().replace(' ', '_')
            output_path = Path("outputs") / f"{medicine1_clean}_vs_{medicine2_clean}_comparison.json"

        output_path.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Output path: {output_path}")

        context_parts = [f"Comparing {medicine1} and {medicine2}"]
        if use_case:
            context_parts.append(f"Use case: {use_case}")
            logger.info(f"Use case: {use_case}")
        if patient_age is not None:
            context_parts.append(f"Patient age: {patient_age} years")
            logger.info(f"Patient age: {patient_age}")
        if patient_conditions:
            context_parts.append(f"Patient conditions: {patient_conditions}")
            logger.info(f"Patient conditions: {patient_conditions}")

        context = ". ".join(context_parts) + "."
        logger.debug(f"Context: {context}")

        logger.info("Calling MedKitClient.generate_text()...")
        try:
            result = self.client.generate_text(
                prompt=f"Detailed side-by-side comparison between {medicine1} and {medicine2}. {context}",
                schema=MedicinesComparisonResult,
            )

            logger.info(f"✓ Successfully compared medicines")
            logger.info(f"More Effective: {result.comparison_summary.more_effective[:100] if result.comparison_summary.more_effective else 'N/A'}...")
            logger.info(f"More Affordable: {result.comparison_summary.more_affordable[:100] if result.comparison_summary.more_affordable else 'N/A'}...")
            logger.info("-" * 80)
            return result
        except Exception as e:
            logger.error(f"✗ Error comparing medicines: {e}")
            logger.exception("Full exception details:")
            logger.info("-" * 80)
            raise


def get_drugs_comparison(
    medicine1: str,
    medicine2: str,
    config: DrugsComparisonConfig,
    use_case: Optional[str] = None,
    patient_age: Optional[int] = None,
    patient_conditions: Optional[str] = None,
) -> MedicinesComparisonResult:
    """
    Get drugs comparison.

    This is a convenience function that instantiates and runs the
    DrugsComparison analyzer.

    Args:
        medicine1: Name of the first medicine
        medicine2: Name of the second medicine
        config: Configuration object for the analysis
        use_case: Use case or indication for comparison (optional)
        patient_age: Patient's age in years (optional)
        patient_conditions: Patient's medical conditions (optional)

    Returns:
        MedicinesComparisonResult: The result of the analysis
    """
    analyzer = DrugsComparison(config)
    return analyzer.compare(
        medicine1=medicine1,
        medicine2=medicine2,
        use_case=use_case,
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
        description="Medicines Comparison Tool - Compare two medicines side-by-side",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic comparison
  python drugs_comparison.py "Aspirin" "Ibuprofen"

  # With use case
  python drugs_comparison.py "Lisinopril" "Losartan" --use-case "hypertension management"

  # With patient details
  python drugs_comparison.py "Metformin" "Glipizide" --age 68 --conditions "type-2 diabetes, kidney disease"

  # With custom output
  python drugs_comparison.py "Atorvastatin" "Simvastatin" --output comparison.json --verbose
        """,
    )

    # Required arguments
    parser.add_argument(
        "medicine1",
        type=str,
        help="Name of the first medicine to compare",
    )

    parser.add_argument(
        "medicine2",
        type=str,
        help="Name of the second medicine to compare",
    )

    # Optional arguments
    parser.add_argument(
        "--use-case",
        "-u",
        type=str,
        default=None,
        help="Use case or indication for the comparison (e.g., 'pain relief', 'hypertension')",
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
        help="Output file path for results (default: outputs/{medicine1}_vs_{medicine2}_comparison.json)",
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


def print_results(result: MedicinesComparisonResult, verbose: bool = False) -> None:
    """
    Print comparison results in a formatted manner.

    Args:
        result: The analysis result to print
        verbose: Whether to print detailed information
    """
    print("\n" + "=" * 80)
    print("MEDICINES COMPARISON RESULTS")
    print("=" * 80 + "\n")

    # Print comparison summary
    print("COMPARISON SUMMARY:")
    print("-" * 80)
    print(f"More Effective: {result.comparison_summary.more_effective}\n")
    print(f"Safer Option: {result.comparison_summary.safer_option}\n")
    print(f"More Affordable: {result.comparison_summary.more_affordable}\n")
    print(f"Easier Access: {result.comparison_summary.easier_access}\n")
    print(f"Key Differences:")
    differences = [f"  • {diff.strip()}" for diff in result.comparison_summary.key_differences.split(",")]
    print("\n".join(differences) + "\n")

    # Print clinical metrics
    print("=" * 80)
    print("CLINICAL METRICS")
    print("=" * 80 + "\n")

    for clinical in [result.medicine1_clinical, result.medicine2_clinical]:
        print(f"Medicine: {clinical.medicine_name}")
        print(f"  Effectiveness: {clinical.effectiveness_rating.value}")
        print(f"  Efficacy Rate: {clinical.efficacy_rate}")
        print(f"  Onset of Action: {clinical.onset_of_action}")
        print(f"  Safety Rating: {clinical.safety_rating.value}")
        if clinical.black_box_warning:
            print(f"  Black Box Warning: {clinical.black_box_warning}")
        print()

    # Print regulatory metrics
    print("=" * 80)
    print("REGULATORY INFORMATION")
    print("=" * 80 + "\n")

    for regulatory in [result.medicine1_regulatory, result.medicine2_regulatory]:
        print(f"Medicine: {regulatory.medicine_name}")
        print(f"  FDA Status: {regulatory.fda_approval_status}")
        print(f"  Approval Date: {regulatory.approval_date}")
        print(f"  Approval Type: {regulatory.approval_type}")
        print(f"  Generic Available: {'Yes' if regulatory.generic_available else 'No'}")
        print()

    # Print practical metrics
    print("=" * 80)
    print("PRACTICAL INFORMATION")
    print("=" * 80 + "\n")

    for practical in [result.medicine1_practical, result.medicine2_practical]:
        print(f"Medicine: {practical.medicine_name}")
        print(f"  Availability: {practical.availability_status.value}")
        print(f"  Typical Cost: {practical.typical_cost_range}")
        print(f"  Insurance Coverage: {practical.insurance_coverage}")
        print()

    # Print recommendations
    print("=" * 80)
    print("RECOMMENDATIONS")
    print("=" * 80 + "\n")

    recs = result.recommendations
    if recs.for_acute_conditions:
        print(f"For Acute Conditions:\n{recs.for_acute_conditions}\n")
    if recs.for_chronic_conditions:
        print(f"For Chronic Conditions:\n{recs.for_chronic_conditions}\n")
    if recs.for_elderly_patients:
        print(f"For Elderly Patients:\n{recs.for_elderly_patients}\n")
    if recs.for_cost_sensitive:
        print(f"For Cost-Sensitive Patients:\n{recs.for_cost_sensitive}\n")
    print(f"Overall Recommendation:\n{recs.overall_recommendation}\n")

    # Print narrative analysis
    print("=" * 80)
    print("DETAILED ANALYSIS")
    print("=" * 80 + "\n")
    print(result.narrative_analysis + "\n")

    # Print evidence quality and limitations
    print("=" * 80)
    print("EVIDENCE QUALITY & LIMITATIONS")
    print("=" * 80 + "\n")
    print(f"Evidence Quality: {result.evidence_quality}\n")
    print("Limitations:")
    limitations = [f"  • {lim.strip()}" for lim in result.limitations.split(",")]
    print("\n".join(limitations) + "\n")

    print("=" * 80)


def main() -> int:
    """
    Main entry point for the drugs comparison CLI.

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
        config = DrugsComparisonConfig(
            output_path=args.output,
            verbosity=args.verbose,
            prompt_style=prompt_style,
        )

        logger.info(f"Configuration created successfully")

        # Run analysis
        analyzer = DrugsComparison(config)
        result = analyzer.compare(
            medicine1=args.medicine1,
            medicine2=args.medicine2,
            use_case=args.use_case,
            patient_age=args.age,
            patient_conditions=args.conditions,
        )

        # Print results
        print_results(result, verbose=args.verbose)

        # Save results to file
        if args.output:
            output_path = args.output
        else:
            medicine1_clean = args.medicine1.lower().replace(' ', '_')
            medicine2_clean = args.medicine2.lower().replace(' ', '_')
            output_path = Path("outputs") / f"{medicine1_clean}_vs_{medicine2_clean}_comparison.json"

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

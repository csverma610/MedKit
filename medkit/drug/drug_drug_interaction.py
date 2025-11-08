"""
drug_drug_interaction.py - Drug-Drug Interaction Analysis

Analyze potential harmful interactions between two medicines and provide comprehensive
clinical recommendations using structured data models and the MedKit AI client
with schema-aware prompting.

This module helps healthcare providers identify dangerous drug combinations and
understand the mechanisms, clinical effects, and management strategies for interactions.

QUICK START:
    from drug_drug_interaction import DrugDrugInteraction, DrugDrugInteractionConfig

    # Configure the analysis
    config = DrugDrugInteractionConfig(medicine1="aspirin", medicine2="ibuprofen")

    # Create an analyzer and get the interaction
    interaction = DrugDrugInteraction(config).analyze()

    # Check severity
    if interaction.severity_level.value in ["SIGNIFICANT", "CONTRAINDICATED"]:
        print(f"⚠️ Serious interaction: {interaction.mechanism_of_interaction}")

    # Get management recommendations
    print(f"Recommendations: {interaction.management_recommendations}")

COMMON USES:
    1. Identify dangerous drug combinations before prescribing
    2. Counsel patients on medication compatibility
    3. Review patient medications for interactions
    4. Support polypharmacy management in elderly patients
    5. Generate clinical decision support recommendations
    6. Create interaction reports for healthcare providers

KEY CONCEPTS:
    - DrugInteractionSeverity: How serious the interaction is (NONE to CONTRAINDICATED)
    - ConfidenceLevel: Strength of evidence (HIGH, MODERATE, LOW)
    - DataSourceType: Where the interaction evidence comes from
    - DrugInteractionDetails: Complete information about the interaction

INTERACTION INFORMATION:
    - Mechanism of interaction: How drugs interact chemically/pharmacologically
    - Clinical effects: Observable symptoms and complications
    - Management recommendations: How to handle the interaction
    - Timing considerations: Spacing between doses
    - Monitoring requirements: What to watch for
"""

import logging
import sys
import json
import argparse
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from pydantic import BaseModel, Field, validator
from typing import Optional

from medkit.core.medkit_client import MedKitClient
from medkit.core.module_config import get_module_config
from medkit.utils.pydantic_prompt_generator import PromptStyle
from medkit.utils.logging_config import setup_logger
from medkit.utils.storage_config import StorageConfig

import hashlib
from medkit.utils.lmdb_storage import LMDBStorage, LMDBConfig

# Configure logging
logger = setup_logger(__name__)
logger.info("="*80)
logger.info("Drug-Drug Interaction Module Initialized")
logger.info("="*80)


class DrugInteractionSeverity(str, Enum):
    """
    Severity levels for drug-drug interactions.

    Indicates how serious the interaction is and what clinical action is needed.

    Attributes:
        NONE: No clinically significant interaction
        MINOR: Minimal clinical significance, usually no action needed
        MILD: Small clinical effect, may need minor monitoring
        MODERATE: Notable clinical effect, usually requires intervention
        SIGNIFICANT: Major clinical concern, careful management required
        CONTRAINDICATED: Absolute contraindication, drugs should not be combined

    Example:
        severity = DrugInteractionSeverity.SIGNIFICANT
    """
    NONE = "NONE"
    MINOR = "MINOR"
    MILD = "MILD"
    MODERATE = "MODERATE"
    SIGNIFICANT = "SIGNIFICANT"
    CONTRAINDICATED = "CONTRAINDICATED"


class ConfidenceLevel(str, Enum):
    """
    Confidence levels in interaction assessment.

    Indicates strength of evidence supporting the interaction claim.

    Attributes:
        HIGH: Strong evidence from clinical studies and guidelines
        MODERATE: Adequate evidence from research or case reports
        LOW: Limited evidence, theoretical basis, or anecdotal reports

    Example:
        confidence = ConfidenceLevel.HIGH
    """
    HIGH = "HIGH"
    MODERATE = "MODERATE"
    LOW = "LOW"


class DataSourceType(str, Enum):
    """
    Types of data sources for interaction information.

    Specifies where the interaction evidence originates.

    Attributes:
        CLINICAL_STUDIES: Peer-reviewed clinical trial data
        PHARMACOKINETIC_ANALYSIS: Derived from drug metabolism studies
        AI_GENERATED: Generated using AI analysis
        CASE_REPORTS: Individual case reports in medical literature
        REGULATORY_DATA: FDA or other regulatory agency data

    Example:
        source = DataSourceType.CLINICAL_STUDIES
    """
    CLINICAL_STUDIES = "Clinical Studies"
    PHARMACOKINETIC_ANALYSIS = "Pharmacokinetic Analysis"
    AI_GENERATED = "AI-Generated"
    CASE_REPORTS = "Case Reports"
    REGULATORY_DATA = "Regulatory Data"


class DrugInteractionDetails(BaseModel):
    """
    Detailed information about a drug-drug interaction.

    Includes comprehensive analysis of how two drugs interact, clinical effects,
    and management recommendations for healthcare providers.

    Attributes:
        drug1_name (str): Name of the first medicine
        drug2_name (str): Name of the second medicine
        severity_level (DrugInteractionSeverity): How serious the interaction is
        mechanism_of_interaction (str): How drugs interact chemically/pharmacologically
        clinical_effects (str): Observable clinical effects and symptoms
        management_recommendations (str): How to handle the interaction

    Example:
        interaction = DrugInteractionDetails(
            drug1_name="Warfarin",
            drug2_name="Aspirin",
            severity_level=DrugInteractionSeverity.SIGNIFICANT,
            mechanism_of_interaction="Both drugs inhibit hemostasis...",
            clinical_effects="Increased bleeding risk",
            management_recommendations="Monitor INR, avoid if possible"
        )
    """
    drug1_name: str = Field(description="Name of the first medicine")
    drug2_name: str = Field(description="Name of the second medicine")
    severity_level: DrugInteractionSeverity = Field(
        description="Severity of the interaction (NONE, MINOR, MILD, MODERATE, SIGNIFICANT, CONTRAINDICATED)"
    )
    mechanism_of_interaction: str = Field(
        description="Detailed explanation of how the two drugs interact at the molecular/cellular level"
    )
    clinical_effects: str = Field(
        description="Observable clinical effects and symptoms of the interaction, comma-separated"
    )
    management_recommendations: str = Field(
        description="Clinical recommendations for managing the interaction (dose adjustments, monitoring, spacing, etc.), comma-separated"
    )
    alternative_medicines: str = Field(
        description="Alternative medicines that could be substituted for safer combinations, comma-separated"
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
    """Patient-friendly explanation of the interaction."""
    simple_explanation: str = Field(
        description="Simple, non-technical explanation of what happens when these medicines interact"
    )
    what_patient_should_do: str = Field(
        description="Clear action steps for the patient (e.g., inform doctor, take at different times, etc.)"
    )
    warning_signs: str = Field(
        description="Symptoms or signs the patient should watch for, comma-separated"
    )
    when_to_seek_help: str = Field(
        description="Clear guidance on when to seek immediate medical attention"
    )


class DataAvailabilityInfo(BaseModel):
    """Information about data availability."""
    data_available: bool = Field(
        description="Whether interaction data is available"
    )
    reason: Optional[str] = Field(
        default=None,
        description="Explanation if data is not available (e.g., 'No interactions found in database', 'Limited research available', etc.)"
    )


class DrugInteractionResult(BaseModel):
    """
    Comprehensive drug-drug interaction analysis result.

    Combines clinical data, patient education, and availability information
    in a structured format for healthcare professionals and patients.
    """
    interaction_details: Optional[DrugInteractionDetails] = Field(
        default=None,
        description="Detailed interaction information (None if no interaction or data not available)"
    )
    technical_summary: str = Field(
        description="Technical summary of the interaction suitable for healthcare professionals"
    )
    patient_friendly_summary: Optional[PatientFriendlySummary] = Field(
        default=None,
        description="Patient-friendly explanation (None if no interaction)"
    )
    data_availability: DataAvailabilityInfo = Field(
        description="Status of data availability for this interaction check"
    )


@dataclass
class DrugDrugInteractionConfig(StorageConfig):
    """
    Configuration for drug-drug interaction analysis.

    Inherits from StorageConfig for LMDB database settings:
    - db_path: Auto-generated path to drug_drug_interaction.lmdb
    - db_capacity_mb: Database capacity (default 500 MB)
    - db_store: Whether to cache results (default True)
    - db_overwrite: Whether to refresh cache (default False)
    """
    output_path: Optional[Path] = None
    verbosity: bool = False
    prompt_style: PromptStyle = PromptStyle.DETAILED
    enable_cache: bool = True

    def __post_init__(self):
        """Set default db_path if not provided, then validate."""
        if self.db_path is None:
            self.db_path = str(
                Path(__file__).parent.parent / "storage" / "drug_drug_interaction.lmdb"
            )
        # Call parent validation
        super().__post_init__()


class DrugDrugInteraction:
    """Analyzes drug-drug interactions based on provided configuration."""

    def __init__(self, config: DrugDrugInteractionConfig):
        self.config = config

        # Load model name from ModuleConfig
        try:
            module_config = get_module_config("drug_drug_interaction")
            model_name = module_config.model_name
        except ValueError:
            # Fallback to default if not registered yet
            model_name = "gemini-1.5-pro"

        self.client = MedKitClient(model_name=model_name)

    def analyze(
        self,
        medicine1: str,
        medicine2: str,
        age: Optional[int] = None,
        dosage1: Optional[str] = None,
        dosage2: Optional[str] = None,
        medical_conditions: Optional[str] = None,
    ) -> DrugInteractionResult:
        """
        Analyzes how two drugs interact.

        Args:
            medicine1: Name of the first medicine
            medicine2: Name of the second medicine
            age: Patient's age in years (optional, 0-150)
            dosage1: Dosage information for first medicine (optional)
            dosage2: Dosage information for second medicine (optional)
            medical_conditions: Patient's medical conditions (optional, comma-separated)

        Returns:
            DrugInteractionResult: Comprehensive interaction analysis with management recommendations
        """
        # Validate inputs
        if not medicine1 or not medicine1.strip():
            raise ValueError("Medicine 1 name cannot be empty")
        if not medicine2 or not medicine2.strip():
            raise ValueError("Medicine 2 name cannot be empty")
        if age is not None and (age < 0 or age > 150):
            raise ValueError("Age must be between 0 and 150 years")

        logger.info("-" * 80)
        logger.info(f"Starting drug-drug interaction analysis")
        logger.info(f"Drug 1: {medicine1}")
        logger.info(f"Drug 2: {medicine2}")
        logger.info(f"Prompt Style: {self.config.prompt_style.value if hasattr(self.config.prompt_style, 'value') else self.config.prompt_style}")

        output_path = self.config.output_path
        if output_path is None:
            medicine1_clean = medicine1.lower().replace(' ', '_')
            medicine2_clean = medicine2.lower().replace(' ', '_')
            output_path = Path("outputs") / f"{medicine1_clean}_{medicine2_clean}_interaction.json"

        output_path.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Output path: {output_path}")

        context_parts = [f"Checking interaction between {medicine1} and {medicine2}"]
        if age is not None:
            context_parts.append(f"Patient age: {age} years")
            logger.info(f"Patient age: {age}")
        if dosage1:
            context_parts.append(f"{medicine1} dosage: {dosage1}")
            logger.info(f"{medicine1} dosage: {dosage1}")
        if dosage2:
            context_parts.append(f"{medicine2} dosage: {dosage2}")
            logger.info(f"{medicine2} dosage: {dosage2}")
        if medical_conditions:
            context_parts.append(f"Patient conditions: {medical_conditions}")
            logger.info(f"Medical conditions: {medical_conditions}")

        context = ". ".join(context_parts) + "."
        logger.debug(f"Context: {context}")

        logger.info("Calling MedKitClient.generate_text()...")
        try:
            result = self.client.generate_text(
                prompt=f"{medicine1} and {medicine2} interaction analysis. {context}",
                schema=DrugInteractionResult,
            )

            logger.info(f"✓ Successfully analyzed interaction")
            logger.info(f"Severity: {result.interaction_details.severity_level if result.interaction_details else 'N/A'}")
            logger.info(f"Data Available: {result.data_availability.data_available}")
            logger.info("-" * 80)
            return result
        except Exception as e:
            logger.error(f"✗ Error analyzing drug interaction: {e}")
            logger.exception("Full exception details:")
            logger.info("-" * 80)
            raise


def get_drug_drug_interaction(
    medicine1: str,
    medicine2: str,
    config: DrugDrugInteractionConfig,
    age: Optional[int] = None,
    dosage1: Optional[str] = None,
    dosage2: Optional[str] = None,
    medical_conditions: Optional[str] = None,
) -> DrugInteractionResult:
    """
    Get drug-drug interaction analysis.

    This is a convenience function that instantiates and runs the
    DrugDrugInteraction analyzer.

    Args:
        medicine1: Name of the first medicine
        medicine2: Name of the second medicine
        config: Configuration object for the analysis
        age: Patient's age in years (optional)
        dosage1: Dosage information for first medicine (optional)
        dosage2: Dosage information for second medicine (optional)
        medical_conditions: Patient's medical conditions (optional)

    Returns:
        DrugInteractionResult: The result of the analysis
    """
    analyzer = DrugDrugInteraction(config)
    return analyzer.analyze(
        medicine1=medicine1,
        medicine2=medicine2,
        age=age,
        dosage1=dosage1,
        dosage2=dosage2,
        medical_conditions=medical_conditions,
    )


def create_cli_parser() -> argparse.ArgumentParser:
    """
    Create and configure the argument parser for the CLI.

    Returns:
        argparse.ArgumentParser: Configured parser for command-line arguments
    """
    parser = argparse.ArgumentParser(
        description="Drug-Drug Interaction Analyzer - Check interactions between two medicines",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic analysis
  python drug_drug_interaction.py "Warfarin" "Aspirin"

  # With patient details
  python drug_drug_interaction.py "Metformin" "Lisinopril" --age 65 --dosage1 "500mg twice daily"

  # With medical conditions and custom output
  python drug_drug_interaction.py "Ibuprofen" "Aspirin" --conditions "hypertension, diabetes" --output interaction.json

  # With detailed prompt style
  python drug_drug_interaction.py "Simvastatin" "Clarithromycin" --prompt-style detailed --verbose
        """,
    )

    # Required arguments
    parser.add_argument(
        "medicine1",
        type=str,
        help="Name of the first medicine",
    )

    parser.add_argument(
        "medicine2",
        type=str,
        help="Name of the second medicine",
    )

    # Optional arguments
    parser.add_argument(
        "--age",
        "-a",
        type=int,
        default=None,
        help="Patient's age in years (0-150)",
    )

    parser.add_argument(
        "--dosage1",
        "-d1",
        type=str,
        default=None,
        help="Dosage information for first medicine",
    )

    parser.add_argument(
        "--dosage2",
        "-d2",
        type=str,
        default=None,
        help="Dosage information for second medicine",
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
        help="Output file path for results (default: outputs/{medicine1}_{medicine2}_interaction.json)",
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
        default=False,
        help="Disable schema-based prompt generation",
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


def print_results(result: DrugInteractionResult, verbose: bool = False) -> None:
    """
    Print interaction analysis results in a formatted manner.

    Args:
        result: The analysis result to print
        verbose: Whether to print detailed information
    """
    print("\n" + "=" * 80)
    print("DRUG-DRUG INTERACTION ANALYSIS RESULTS")
    print("=" * 80 + "\n")

    # Print data availability
    if not result.data_availability.data_available:
        print(f"⚠️  Data Availability: {result.data_availability.reason}")
        print("=" * 80 + "\n")
        return

    # Print interaction details
    if result.interaction_details:
        details = result.interaction_details
        print(f"Drug 1: {details.drug1_name}")
        print(f"Drug 2: {details.drug2_name}")
        print(f"Severity Level: {details.severity_level.value}")
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

        # Print management recommendations
        print("MANAGEMENT RECOMMENDATIONS:")
        print("-" * 80)
        recommendations = [f"  • {rec.strip()}" for rec in details.management_recommendations.split(",")]
        print("\n".join(recommendations) + "\n")

        # Print alternative medicines
        print("ALTERNATIVE MEDICINES:")
        print("-" * 80)
        alternatives = [f"  • {alt.strip()}" for alt in details.alternative_medicines.split(",")]
        print("\n".join(alternatives) + "\n")

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

        print("WARNING SIGNS:")
        print("-" * 80)
        warning_signs = [f"  • {sign.strip()}" for sign in summary.warning_signs.split(",")]
        print("\n".join(warning_signs) + "\n")

        print("WHEN TO SEEK HELP:")
        print("-" * 80)
        print(f"{summary.when_to_seek_help}\n")

    # Print technical summary
    print("\n" + "=" * 80)
    print("TECHNICAL SUMMARY")
    print("=" * 80 + "\n")
    print(result.technical_summary + "\n")

    print("=" * 80)


def main() -> int:
    """
    Main entry point for the drug-drug interaction CLI.

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
        config = DrugDrugInteractionConfig(
            medicine1=args.medicine1,
            medicine2=args.medicine2,
            age=args.age,
            dosage1=args.dosage1,
            dosage2=args.dosage2,
            medical_conditions=args.conditions,
            output_path=args.output,
            use_schema_prompt=not args.no_schema,
            prompt_style=prompt_style,
        )

        logger.info(f"Configuration created successfully")

        # Run analysis
        analyzer = DrugDrugInteraction(config)
        result = analyzer.analyze()

        # Print results
        print_results(result, verbose=args.verbose)

        # Save results to file
        if args.output:
            output_path = args.output
        else:
            medicine1_clean = args.medicine1.lower().replace(' ', '_')
            medicine2_clean = args.medicine2.lower().replace(' ', '_')
            output_path = Path("outputs") / f"{medicine1_clean}_{medicine2_clean}_interaction.json"

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
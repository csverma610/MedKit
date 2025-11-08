"""
drug_disease_interaction.py - Drug-Disease Interaction Analysis

Analyze how medical conditions affect drug efficacy and safety, providing
comprehensive clinical guidance using structured data models and the MedKit AI client
with schema-aware prompting.

This module helps clinicians understand whether a patient's existing medical conditions
might affect how a drug works, its safety profile, or whether it's contraindicated.

QUICK START:
    from drug_disease_interaction import DrugDiseaseInteraction, DrugDiseaseInteractionConfig

    # Configure the analysis (settings only)
    config = DrugDiseaseInteractionConfig(
        output_path=None,  # optional
        verbosity=False,
        prompt_style="DETAILED"
    )

    # Create an analyzer and get the interaction with user parameters
    result = DrugDiseaseInteraction(config).analyze(
        medicine_name="metformin",
        condition_name="kidney disease"
    )

    # Access different aspects of the interaction
    if result.interaction_details:
        efficacy = result.interaction_details.efficacy_impact
        safety = result.interaction_details.safety_impact
        adjustments = result.interaction_details.dosage_adjustment

COMMON USES:
    1. Check if a condition affects drug efficacy
    2. Assess safety risks when prescribing to patients with comorbidities
    3. Determine if dose adjustments are needed
    4. Identify monitoring requirements
    5. Understand whether a drug is contraindicated
    6. Generate patient education materials about their medications

KEY CONCEPTS:
    - InteractionSeverity: How serious the interaction is (NONE to CONTRAINDICATED)
    - ConfidenceLevel: Strength of evidence (HIGH, MODERATE, LOW)
    - ImpactType: What type of impact occurs (efficacy, toxicity, metabolism, etc.)
    - DataSourceType: Where the interaction evidence comes from

ANALYSIS DIMENSIONS:
    - Efficacy Impact: Does the condition reduce or enhance drug effectiveness?
    - Safety Impact: Does the condition increase the risk of side effects?
    - Dosage Adjustments: Is the dose or frequency needed to be changed?
    - Monitoring Requirements: What should be monitored during treatment?
    - Clinical Considerations: Additional contextual information
"""

import sys
import argparse
import logging
import json
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
logger.info("Drug-Disease Interaction Module Initialized")
logger.info("="*80)


class InteractionSeverity(str, Enum):
    """
    Severity levels for drug-disease interactions.

    Severity scale from no interaction to absolute contraindication.

    Attributes:
        NONE: No clinically significant interaction
        MINOR: Minimal clinical significance, usually no action needed
        MILD: Small clinical effect, may need minor monitoring
        MODERATE: Notable clinical effect, usually requires intervention
        SIGNIFICANT: Major clinical concern, careful management required
        CONTRAINDICATED: Absolute contraindication, drug should not be used

    Example:
        severity = InteractionSeverity.MODERATE
        if severity in [InteractionSeverity.SIGNIFICANT, InteractionSeverity.CONTRAINDICATED]:
            print("High-risk interaction detected")
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

    Indicates the strength of evidence supporting the interaction claim.

    Attributes:
        HIGH: Strong evidence from multiple clinical studies and guidelines
        MODERATE: Adequate evidence from clinical studies or case reports
        LOW: Limited evidence, anecdotal reports, or theoretical basis

    Example:
        if interaction.confidence == ConfidenceLevel.LOW:
            print("Use caution - limited evidence for this interaction")
    """
    HIGH = "HIGH"
    MODERATE = "MODERATE"
    LOW = "LOW"


class DataSourceType(str, Enum):
    """
    Types of data sources for interaction information.

    Specifies where the interaction evidence originates.

    Attributes:
        CLINICAL_STUDIES: Data from peer-reviewed clinical trials
        PHARMACOKINETIC_ANALYSIS: Derived from drug metabolism studies
        FDA_WARNINGS: From FDA adverse event reports or black box warnings
        CASE_REPORTS: Individual case reports in medical literature
        CLINICAL_GUIDELINES: From professional clinical guidelines (AMA, ASAM, etc.)

    Example:
        source = DataSourceType.FDA_WARNINGS
    """
    CLINICAL_STUDIES = "Clinical Studies"
    PHARMACOKINETIC_ANALYSIS = "Pharmacokinetic Analysis"
    FDA_WARNINGS = "FDA Warnings"
    CASE_REPORTS = "Case Reports"
    CLINICAL_GUIDELINES = "Clinical Guidelines"


class ImpactType(str, Enum):
    """
    Type of impact the condition has on drug use.

    Categorizes how the disease/condition affects the drug therapy.

    Attributes:
        EFFICACY_REDUCTION: Drug becomes less effective
        EFFICACY_ENHANCEMENT: Drug becomes more effective (usually concerning)
        INCREASED_TOXICITY: Risk of adverse effects increases
        ALTERED_METABOLISM: Drug is processed differently by the body
        CONTRAINDICATED: Drug should not be used at all
        REQUIRES_MONITORING: Enhanced clinical monitoring needed
        REQUIRES_DOSE_ADJUSTMENT: Dose or frequency must be changed

    Example:
        impact = ImpactType.ALTERED_METABOLISM
    """
    EFFICACY_REDUCTION = "Reduced Drug Efficacy"
    EFFICACY_ENHANCEMENT = "Enhanced Drug Efficacy"
    INCREASED_TOXICITY = "Increased Toxicity Risk"
    ALTERED_METABOLISM = "Altered Drug Metabolism"
    CONTRAINDICATED = "Contraindicated"
    REQUIRES_MONITORING = "Requires Enhanced Monitoring"
    REQUIRES_DOSE_ADJUSTMENT = "Requires Dose Adjustment"


class EfficacyImpact(BaseModel):
    """Information about how the condition affects drug effectiveness."""
    has_impact: bool = Field(description="Whether the condition affects drug efficacy")
    impact_description: Optional[str] = Field(
        default=None,
        description="How the condition reduces, enhances, or otherwise affects drug effectiveness"
    )
    clinical_significance: Optional[str] = Field(
        default=None,
        description="The clinical importance of the efficacy impact"
    )
    monitoring_for_efficacy: Optional[str] = Field(
        default=None,
        description="How to monitor for adequate drug response, comma-separated"
    )


class SafetyImpact(BaseModel):
    """Information about how the condition affects drug safety."""
    has_impact: bool = Field(description="Whether the condition increases safety risks")
    impact_description: Optional[str] = Field(
        default=None,
        description="How the condition increases adverse effects or toxicity"
    )
    increased_side_effects: Optional[str] = Field(
        default=None,
        description="Specific side effects more likely to occur, comma-separated"
    )
    risk_level: Optional[InteractionSeverity] = Field(
        default=None,
        description="Risk severity (MINOR, MILD, MODERATE, SIGNIFICANT, CONTRAINDICATED)"
    )
    monitoring_for_safety: Optional[str] = Field(
        default=None,
        description="Safety monitoring parameters and labs to check, comma-separated"
    )


class DosageAdjustment(BaseModel):
    """Dosage adjustment recommendations based on the condition."""
    adjustment_needed: bool = Field(description="Whether dose adjustment is necessary")
    adjustment_type: Optional[str] = Field(
        default=None,
        description="Type of adjustment (e.g., 'dose reduction', 'dose increase', 'dosing interval change')"
    )
    specific_recommendations: Optional[str] = Field(
        default=None,
        description="Specific dosage adjustment guidance and rationale"
    )
    monitoring_parameters: Optional[str] = Field(
        default=None,
        description="Labs or parameters to check when adjusting dose, comma-separated"
    )


class ManagementStrategy(BaseModel):
    """Overall management strategy for the drug-disease interaction."""
    impact_types: list[ImpactType] = Field(
        description="Types of impacts (efficacy, safety, metabolism, etc.)"
    )
    clinical_recommendations: str = Field(
        description="Comprehensive clinical recommendations for managing the interaction, comma-separated"
    )
    contraindication_status: Optional[str] = Field(
        default=None,
        description="Whether drug is contraindicated, relatively contraindicated, or safe with precautions"
    )
    alternative_treatments: Optional[str] = Field(
        default=None,
        description="Alternative medications or approaches for patients with this condition, comma-separated"
    )


class DrugDiseaseInteractionDetails(BaseModel):
    """Comprehensive drug-disease interaction analysis."""
    medicine_name: str = Field(description="Name of the medicine")
    condition_name: str = Field(description="Name of the medical condition")
    overall_severity: InteractionSeverity = Field(
        description="Overall severity of the interaction"
    )
    mechanism_of_interaction: str = Field(
        description="How the condition affects the drug's action, metabolism, or efficacy at the molecular/physiological level"
    )
    efficacy_impact: EfficacyImpact = Field(
        description="How the condition affects drug effectiveness"
    )
    safety_impact: SafetyImpact = Field(
        description="How the condition affects drug safety"
    )
    dosage_adjustment: DosageAdjustment = Field(
        description="Dosage adjustment recommendations if needed"
    )
    management_strategy: ManagementStrategy = Field(
        description="Overall management strategy and clinical approach"
    )
    confidence_level: ConfidenceLevel = Field(
        description="Confidence level in this interaction assessment"
    )
    data_source_type: DataSourceType = Field(
        description="Primary source of this interaction data"
    )
    references: Optional[str] = Field(
        default=None,
        description="Citations or references supporting this interaction data, comma-separated"
    )


class PatientFriendlySummary(BaseModel):
    """Patient-friendly explanation of drug-disease interactions."""
    simple_explanation: str = Field(
        description="Simple explanation of how the condition affects this medicine"
    )
    what_patient_should_do: str = Field(
        description="Clear action steps for managing the condition-medicine interaction"
    )
    signs_of_problems: str = Field(
        description="Symptoms or signs that indicate the medicine may not be working properly or causing problems, comma-separated"
    )
    when_to_contact_doctor: str = Field(
        description="Clear guidance on when to contact healthcare provider"
    )
    lifestyle_modifications: str = Field(
        description="Lifestyle changes that may help manage the interaction, comma-separated"
    )


class DataAvailabilityInfo(BaseModel):
    """Information about data availability."""
    data_available: bool = Field(
        description="Whether interaction data is available"
    )
    reason: Optional[str] = Field(
        default=None,
        description="Explanation if data is not available"
    )


class DrugDiseaseInteractionResult(BaseModel):
    """
    Comprehensive drug-disease interaction analysis result.

    Combines clinical data, patient education, and management strategies
    in a structured format for healthcare professionals and patients.
    """
    interaction_details: Optional[DrugDiseaseInteractionDetails] = Field(
        default=None,
        description="Detailed interaction information (None if data not available)"
    )
    technical_summary: str = Field(
        description="Technical summary suitable for healthcare professionals"
    )
    patient_friendly_summary: Optional[PatientFriendlySummary] = Field(
        default=None,
        description="Patient-friendly explanation"
    )
    data_availability: DataAvailabilityInfo = Field(
        description="Status of data availability"
    )


@dataclass
class DrugDiseaseInteractionConfig(StorageConfig):
    """
    Configuration for drug_disease_interaction.

    Inherits from StorageConfig for LMDB database settings:
    - db_path: Auto-generated path to drug_disease_interaction.lmdb
    - db_capacity_mb: Database capacity (default 500 MB)
    - db_store: Whether to cache results (default True)
    - db_overwrite: Whether to refresh cache (default False)
    """
    """Configuration for drug-disease interaction analysis."""
    output_path: Optional[Path] = None
    verbosity: bool = False
    prompt_style: PromptStyle = PromptStyle.DETAILED
    enable_cache: bool = True

    def __post_init__(self):
        """Set default db_path if not provided, then validate."""
        if self.db_path is None:
            self.db_path = str(
                Path(__file__).parent.parent / "storage" / "drug_disease_interaction.lmdb"
            )
        # Call parent validation
        super().__post_init__()

class DrugDiseaseInteraction:
    """Analyzes drug-disease interactions based on provided configuration."""

    def __init__(self, config: DrugDiseaseInteractionConfig):
        self.config = config

        # Load model name from ModuleConfig
        try:
            module_config = get_module_config("drug_disease_interaction")
            model_name = module_config.model_name
        except ValueError:
            # Fallback to default if not registered yet
            model_name = "gemini-1.5-pro"

        self.client = MedKitClient(model_name=model_name)

    def analyze(
        self,
        medicine_name: str,
        condition_name: str,
        condition_severity: Optional[str] = None,
        age: Optional[int] = None,
        other_medications: Optional[str] = None,
    ) -> DrugDiseaseInteractionResult:
        """
        Analyzes how a medical condition affects drug efficacy, safety, and metabolism.

        Args:
            medicine_name: Name of the medicine to analyze
            condition_name: Name of the medical condition
            condition_severity: Severity of the condition (optional)
            age: Patient age in years (optional, 0-150)
            other_medications: Other medications patient is taking (optional, comma-separated)

        Returns:
            DrugDiseaseInteractionResult: Comprehensive interaction analysis with management recommendations
        """
        # Validate inputs
        if not medicine_name or not medicine_name.strip():
            raise ValueError("Medicine name cannot be empty")
        if not condition_name or not condition_name.strip():
            raise ValueError("Condition name cannot be empty")
        if age is not None and (age < 0 or age > 150):
            raise ValueError("Age must be between 0 and 150 years")

        logger.info("-" * 80)
        logger.info(f"Starting drug-disease interaction analysis")
        logger.info(f"Medicine: {medicine_name}")
        logger.info(f"Condition: {condition_name}")
        logger.info(f"Prompt Style: {self.config.prompt_style.value if hasattr(self.config.prompt_style, 'value') else self.config.prompt_style}")

        output_path = self.config.output_path
        if output_path is None:
            medicine_clean = medicine_name.lower().replace(' ', '_')
            condition_clean = condition_name.lower().replace(' ', '_')
            output_path = Path("outputs") / f"{medicine_clean}_{condition_clean}_interaction.json"

        output_path.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Output path: {output_path}")

        context_parts = [f"Analyzing interaction between {medicine_name} and {condition_name}"]
        if condition_severity:
            context_parts.append(f"Condition severity: {condition_severity}")
            logger.info(f"Condition severity: {condition_severity}")
        if age is not None:
            context_parts.append(f"Patient age: {age} years")
            logger.info(f"Patient age: {age}")
        if other_medications:
            context_parts.append(f"Other medications: {other_medications}")
            logger.info(f"Other medications: {other_medications}")

        context = ". ".join(context_parts) + "."
        logger.debug(f"Context: {context}")

        logger.info("Calling MedKitClient.generate_text()...")
        try:
            result = self.client.generate_text(
                prompt=f"{medicine_name} use in patients with {condition_name}. {context}",
                schema=DrugDiseaseInteractionResult,
            )

            logger.info(f"✓ Successfully analyzed disease interaction")
            logger.info(f"Overall Severity: {result.interaction_details.overall_severity if result.interaction_details else 'N/A'}")
            logger.info(f"Data Available: {result.data_availability.data_available}")
            logger.info("-" * 80)
            return result
        except Exception as e:
            logger.error(f"✗ Error analyzing disease interaction: {e}")
            logger.exception("Full exception details:")
            logger.info("-" * 80)
            raise


def get_drug_disease_interaction(
    medicine_name: str,
    condition_name: str,
    config: DrugDiseaseInteractionConfig,
    condition_severity: Optional[str] = None,
    age: Optional[int] = None,
    other_medications: Optional[str] = None,
) -> DrugDiseaseInteractionResult:
    """
    Get drug-disease interaction analysis.

    This is a convenience function that instantiates and runs the
    DrugDiseaseInteraction analyzer.

    Args:
        medicine_name: Name of the medicine to analyze
        condition_name: Name of the medical condition
        config: Configuration object for the analysis
        condition_severity: Severity of the condition (optional)
        age: Patient age in years (optional)
        other_medications: Other medications patient is taking (optional)

    Returns:
        DrugDiseaseInteractionResult: The result of the analysis
    """
    analyzer = DrugDiseaseInteraction(config)
    return analyzer.analyze(
        medicine_name=medicine_name,
        condition_name=condition_name,
        condition_severity=condition_severity,
        age=age,
        other_medications=other_medications,
    )


def create_cli_parser() -> argparse.ArgumentParser:
    """
    Create and configure the argument parser for the CLI.

    Returns:
        argparse.ArgumentParser: Configured parser for command-line arguments
    """
    parser = argparse.ArgumentParser(
        description="Drug-Disease Interaction Analyzer - Assess how medical conditions affect medicines",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic analysis
  python drug_disease_interaction.py "Metformin" "Kidney Disease"

  # With condition severity
  python drug_disease_interaction.py "Warfarin" "Liver Disease" --condition-severity severe

  # With patient details and other medications
  python drug_disease_interaction.py "Lisinopril" "Hypertension" --age 72 --other-medications "Atorvastatin, Aspirin"

  # With custom output
  python drug_disease_interaction.py "NSAIDs" "Asthma" --output interaction.json --verbose
        """,
    )

    # Required arguments
    parser.add_argument(
        "medicine_name",
        type=str,
        help="Name of the medicine to analyze",
    )

    parser.add_argument(
        "condition_name",
        type=str,
        help="Name of the medical condition",
    )

    # Optional arguments
    parser.add_argument(
        "--condition-severity",
        "-s",
        type=str,
        default=None,
        help="Severity of the condition (mild, moderate, severe)",
    )

    parser.add_argument(
        "--age",
        "-a",
        type=int,
        default=None,
        help="Patient's age in years (0-150)",
    )

    parser.add_argument(
        "--other-medications",
        "-m",
        type=str,
        default=None,
        help="Other medications the patient is taking (comma-separated)",
    )

    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        help="Output file path for results (default: outputs/{medicine}_{condition}_interaction.json)",
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


def print_results(result: DrugDiseaseInteractionResult, verbose: bool = False) -> None:
    """
    Print interaction analysis results in a formatted manner.

    Args:
        result: The analysis result to print
        verbose: Whether to print detailed information
    """
    print("\n" + "=" * 80)
    print("DRUG-DISEASE INTERACTION ANALYSIS RESULTS")
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
        print(f"Condition: {details.condition_name}")
        print(f"Overall Severity: {details.overall_severity.value}")
        print(f"Confidence Level: {details.confidence_level.value}")
        print(f"Data Source: {details.data_source_type.value}\n")

        # Print mechanism of interaction
        print("MECHANISM OF INTERACTION:")
        print("-" * 80)
        print(f"{details.mechanism_of_interaction}\n")

        # Print efficacy impact
        print("EFFICACY IMPACT:")
        print("-" * 80)
        if details.efficacy_impact.has_impact:
            print(f"  Has Impact: Yes")
            if details.efficacy_impact.impact_description:
                print(f"  Description: {details.efficacy_impact.impact_description}")
            if details.efficacy_impact.clinical_significance:
                print(f"  Significance: {details.efficacy_impact.clinical_significance}")
        else:
            print(f"  Has Impact: No")
        print()

        # Print safety impact
        print("SAFETY IMPACT:")
        print("-" * 80)
        if details.safety_impact.has_impact:
            print(f"  Has Impact: Yes")
            if details.safety_impact.impact_description:
                print(f"  Description: {details.safety_impact.impact_description}")
            if details.safety_impact.risk_level:
                print(f"  Risk Level: {details.safety_impact.risk_level.value}")
        else:
            print(f"  Has Impact: No")
        print()

        # Print dosage adjustments
        print("DOSAGE ADJUSTMENTS:")
        print("-" * 80)
        if details.dosage_adjustment.adjustment_needed:
            print(f"  Adjustment Needed: Yes")
            if details.dosage_adjustment.adjustment_type:
                print(f"  Type: {details.dosage_adjustment.adjustment_type}")
            if details.dosage_adjustment.specific_recommendations:
                print(f"  Recommendations: {details.dosage_adjustment.specific_recommendations}")
        else:
            print(f"  Adjustment Needed: No")
        print()

        # Print management recommendations
        print("MANAGEMENT RECOMMENDATIONS:")
        print("-" * 80)
        recommendations = [f"  • {rec.strip()}" for rec in details.management_strategy.clinical_recommendations.split(",")]
        print("\n".join(recommendations) + "\n")

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

        print("SIGNS OF PROBLEMS:")
        print("-" * 80)
        signs = [f"  • {sign.strip()}" for sign in summary.signs_of_problems.split(",")]
        print("\n".join(signs) + "\n")

        print("WHEN TO CONTACT DOCTOR:")
        print("-" * 80)
        print(f"{summary.when_to_contact_doctor}\n")

    # Print technical summary
    print("\n" + "=" * 80)
    print("TECHNICAL SUMMARY")
    print("=" * 80 + "\n")
    print(result.technical_summary + "\n")

    print("=" * 80)


def main() -> int:
    """
    Main entry point for the drug-disease interaction CLI.

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
        config = DrugDiseaseInteractionConfig(
            output_path=args.output,
            verbosity=args.verbose,
            prompt_style=prompt_style,
        )

        logger.info(f"Configuration created successfully")

        # Run analysis
        analyzer = DrugDiseaseInteraction(config)
        result = analyzer.analyze(
            medicine_name=args.medicine_name,
            condition_name=args.condition_name,
            condition_severity=args.condition_severity,
            age=args.age,
            other_medications=args.other_medications,
        )

        # Print results
        print_results(result, verbose=args.verbose)

        # Save results to file
        if args.output:
            output_path = args.output
        else:
            medicine_clean = args.medicine_name.lower().replace(' ', '_')
            condition_clean = args.condition_name.lower().replace(' ', '_')
            output_path = Path("outputs") / f"{medicine_clean}_{condition_clean}_interaction.json"

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
    main()

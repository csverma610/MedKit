#!/usr/bin/env python
"""
CLI for drug-food interaction checking.

Usage:
    python cli/cli_drug_food_interaction.py <drug_name> <food_name>
    python cli/cli_drug_food_interaction.py <drug_name> <food_name> --output output.json
    python cli/cli_drug_food_interaction.py <drug_name> <food_name> --verbose

Examples:
    python cli/cli_drug_food_interaction.py warfarin "leafy greens"
    python cli/cli_drug_food_interaction.py statin grapefruit --verbose
    python cli/cli_drug_food_interaction.py metronidazole alcohol --output interaction.json
"""

import sys
import json
import argparse
from pathlib import Path
from medkit.drug.drug_food_interaction import get_drug_food_interaction


def main():
    """Main CLI entry point for drug-food interaction checking."""
    parser = argparse.ArgumentParser(
        description='Check interactions between medications and foods/beverages'
    )
    parser.add_argument(
        'drug',
        nargs='?',
        help='Name of the medication'
    )
    parser.add_argument(
        'food',
        nargs='?',
        help='Name of the food or beverage'
    )
    parser.add_argument(
        '--output',
        '-o',
        help='Output file path (JSON format)'
    )
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Show detailed information'
    )

    args = parser.parse_args()

    if not args.drug or not args.food:
        parser.print_help()
        sys.exit(1)

    try:
        # Get drug-food interaction information
        result = get_drug_food_interaction(args.drug, args.food)
        
        if result:
            print(f"\n{'=' * 70}")
            print(f"Drug-Food Interaction Analysis")
            print(f"{'=' * 70}")
            
            print(f"\nMedication: {args.drug.title()}")
            print(f"Food/Beverage: {args.food.title()}")
            
            # Display interaction details
            if hasattr(result, 'drug_name'):
                print(f"\n--- INTERACTION DETAILS ---")
                print(f"Drug: {result.drug_name}")
            
            if hasattr(result, 'food_name'):
                print(f"Food/Beverage: {result.food_name}")
            
            if hasattr(result, 'interaction_severity'):
                print(f"Severity: {result.interaction_severity}")
            
            if hasattr(result, 'clinical_effect'):
                print(f"\n--- CLINICAL EFFECT ---")
                print(f"{result.clinical_effect}")
            
            if hasattr(result, 'mechanism'):
                print(f"\n--- MECHANISM ---")
                print(f"{result.mechanism}")
            
            if hasattr(result, 'timing_considerations'):
                print(f"\n--- TIMING CONSIDERATIONS ---")
                print(f"{result.timing_considerations}")
            
            if hasattr(result, 'risk_factors'):
                print(f"\n--- RISK FACTORS ---")
                print(f"{result.risk_factors}")
            
            if hasattr(result, 'management_recommendations'):
                print(f"\n--- MANAGEMENT RECOMMENDATIONS ---")
                print(f"{result.management_recommendations}")
            
            if hasattr(result, 'monitoring_requirements'):
                print(f"\n--- MONITORING REQUIREMENTS ---")
                print(f"{result.monitoring_requirements}")
            
            if hasattr(result, 'avoidance_guidelines'):
                print(f"\n--- AVOIDANCE GUIDELINES ---")
                print(f"{result.avoidance_guidelines}")
            
            if hasattr(result, 'confidence_level'):
                print(f"\nConfidence Level: {result.confidence_level}")
            
            # Save to file if requested
            if args.output:
                output_path = Path(args.output)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Convert to dict for JSON serialization
                if hasattr(result, 'dict'):
                    result_dict = result.dict()
                else:
                    result_dict = vars(result)
                
                with open(output_path, 'w') as f:
                    json.dump(result_dict, f, indent=2)
                print(f"\n\n✓ Complete analysis saved to: {output_path}")
            
            print(f"\n{'=' * 70}\n")
        
        else:
            print(f"No interaction data found for: {args.drug} and {args.food}")
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

#!/usr/bin/env python
"""
CLI for medical test information queries.

Usage:
    python cli/cli_medical_test.py <test_name>
    python cli/cli_medical_test.py <test_name> --output output.json
    python cli/cli_medical_test.py <test_name> --verbose

Examples:
    python cli/cli_medical_test.py "complete blood count"
    python cli/cli_medical_test.py CBC --verbose
    python cli/cli_medical_test.py "chest X-ray" --output xray_info.json
"""

import sys
import json
import argparse
from pathlib import Path
from medkit.diagnostics.medical_test_info import get_medical_test_info


def main():
    """Main CLI entry point for medical test information."""
    parser = argparse.ArgumentParser(
        description='Get detailed information about medical tests'
    )
    parser.add_argument(
        'test',
        nargs='?',
        help='Name of the medical test (e.g., CBC, blood pressure, MRI)'
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

    if not args.test:
        parser.print_help()
        sys.exit(1)

    try:
        # Get medical test information
        result = get_medical_test_info(args.test)
        
        if result:
            print(f"\nMedical Test: {args.test.title()}")
            print("=" * 70)
            
            # Display overview
            if hasattr(result, 'test_name'):
                print(f"\nTest Name: {result.test_name}")
            
            if hasattr(result, 'test_type'):
                print(f"Type: {result.test_type}")
            
            if hasattr(result, 'what_it_measures'):
                print(f"\nWhat It Measures:")
                print(f"{result.what_it_measures}")
            
            if hasattr(result, 'why_performed'):
                print(f"\nWhy It's Performed:")
                print(f"{result.why_performed}")
            
            if hasattr(result, 'how_performed'):
                print(f"\nHow It's Performed:")
                print(f"{result.how_performed}")
            
            if hasattr(result, 'sample_type'):
                print(f"\nSample Type: {result.sample_type}")
            
            if hasattr(result, 'preparation'):
                print(f"\nPreparation:")
                print(f"{result.preparation}")
            
            if hasattr(result, 'duration'):
                print(f"\nDuration: {result.duration}")
            
            if hasattr(result, 'normal_range'):
                print(f"\nNormal Range:")
                print(f"{result.normal_range}")
            
            if hasattr(result, 'abnormal_findings'):
                print(f"\nAbnormal Findings:")
                print(f"{result.abnormal_findings}")
            
            if hasattr(result, 'risks_and_side_effects'):
                print(f"\nRisks and Side Effects:")
                print(f"{result.risks_and_side_effects}")
            
            if hasattr(result, 'cost'):
                print(f"\nTypical Cost: {result.cost}")
            
            if hasattr(result, 'results_timeline'):
                print(f"\nResults Timeline: {result.results_timeline}")
            
            if hasattr(result, 'accuracy_and_reliability'):
                print(f"\nAccuracy and Reliability:")
                print(f"{result.accuracy_and_reliability}")
            
            if hasattr(result, 'when_to_get_tested'):
                print(f"\nWhen to Get Tested:")
                print(f"{result.when_to_get_tested}")
            
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
                print(f"\n\n✓ Complete data saved to: {output_path}")
        
        else:
            print(f"No information found for test: {args.test}")
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

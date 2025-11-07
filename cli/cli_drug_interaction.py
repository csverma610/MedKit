#!/usr/bin/env python
"""
CLI for drug-drug interaction checking.

Usage:
    python cli/cli_drug_interaction.py <drug1> <drug2>

Example:
    python cli/cli_drug_interaction.py aspirin ibuprofen
    python cli/cli_drug_interaction.py warfarin aspirin --verbose
"""

import sys
import argparse
from medkit.drug.drug_drug_interaction import get_drug_interaction


def main():
    """Main CLI entry point for drug-drug interaction checking."""
    parser = argparse.ArgumentParser(
        description='Check interactions between two drugs'
    )
    parser.add_argument(
        'drug1',
        nargs='?',
        help='First drug name'
    )
    parser.add_argument(
        'drug2',
        nargs='?',
        help='Second drug name'
    )
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Show detailed information'
    )
    parser.add_argument(
        '--severity',
        '-s',
        action='store_true',
        help='Show severity level'
    )

    args = parser.parse_args()

    if not args.drug1 or not args.drug2:
        parser.print_help()
        sys.exit(1)

    try:
        result = get_drug_interaction(args.drug1, args.drug2)
        if result:
            print(f"\nDrug-Drug Interaction: {args.drug1.title()} + {args.drug2.title()}")
            print("=" * 60)
            if args.severity:
                print(f"Severity: {result.get('severity', 'Unknown')}")
            print(result)
        else:
            print(f"No interaction data found for: {args.drug1} + {args.drug2}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

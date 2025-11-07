#!/usr/bin/env python
"""
CLI for herbal medicine information.

Usage:
    python cli/cli_herbal_info.py <herb_name>

Example:
    python cli/cli_herbal_info.py turmeric
    python cli/cli_herbal_info.py ginger --benefits
    python cli/cli_herbal_info.py echinacea --interactions
"""

import sys
import argparse
from medkit.medical.herbal_info import get_herbal_information


def main():
    """Main CLI entry point for herbal medicine information."""
    parser = argparse.ArgumentParser(
        description='Get information about herbal medicines and remedies'
    )
    parser.add_argument(
        'herb',
        nargs='?',
        help='Name of the herb/herbal remedy'
    )
    parser.add_argument(
        '--benefits',
        '-b',
        action='store_true',
        help='Show traditional benefits'
    )
    parser.add_argument(
        '--interactions',
        '-i',
        action='store_true',
        help='Show drug-herb interactions'
    )
    parser.add_argument(
        '--dosage',
        '-d',
        action='store_true',
        help='Show dosage information'
    )
    parser.add_argument(
        '--safety',
        '-s',
        action='store_true',
        help='Show safety information'
    )
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Show all information'
    )

    args = parser.parse_args()

    if not args.herb:
        parser.print_help()
        sys.exit(1)

    try:
        result = get_herbal_information(args.herb)
        if result:
            print(f"\nHerbal Medicine Information: {args.herb.title()}")
            print("=" * 60)
            print(result)

            print("\n⚠️  IMPORTANT DISCLAIMER")
            print("-" * 60)
            print("Herbal remedies should be used with caution.")
            print("Consult a healthcare provider before use, especially if:")
            print("  - You are pregnant or breastfeeding")
            print("  - You are taking medications")
            print("  - You have allergies or sensitivities")
            print("  - You have chronic health conditions")
        else:
            print(f"No information found for: {args.herb}")
            print("Tip: Try using common herb names (e.g., 'turmeric', 'ginger')")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

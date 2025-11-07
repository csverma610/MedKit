#!/usr/bin/env python
"""
CLI for medical terminology and dictionary lookups.

Usage:
    python cli/cli_medical_dictionary.py <term>

Example:
    python cli/cli_medical_dictionary.py hypertension
    python cli/cli_medical_dictionary.py "myocardial infarction" --verbose
"""

import sys
import argparse
from medkit.medical.medical_dictionary import get_medical_definition


def main():
    """Main CLI entry point for medical dictionary."""
    parser = argparse.ArgumentParser(
        description='Look up medical terms and definitions'
    )
    parser.add_argument(
        'term',
        nargs='?',
        help='Medical term to look up'
    )
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Show detailed information'
    )
    parser.add_argument(
        '--synonyms',
        '-syn',
        action='store_true',
        help='Show synonyms and related terms'
    )

    args = parser.parse_args()

    if not args.term:
        parser.print_help()
        sys.exit(1)

    try:
        result = get_medical_definition(args.term)
        if result:
            print(f"\nMedical Term: {args.term.title()}")
            print("=" * 60)
            print(result)
            if args.synonyms:
                print("\n[Use --verbose for more details]")
        else:
            print(f"No definition found for: {args.term}")
            print("Tip: Try a more specific medical term")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

#!/usr/bin/env python
"""
CLI for medical specialties and specialists information.

Usage:
    python cli/cli_medical_speciality.py <specialty>

Example:
    python cli/cli_medical_speciality.py cardiology
    python cli/cli_medical_speciality.py psychiatry --doctors
    python cli/cli_medical_speciality.py neurology --conditions
"""

import sys
import argparse
from medkit.medical.medical_speciality import get_speciality_info


def main():
    """Main CLI entry point for medical specialties."""
    parser = argparse.ArgumentParser(
        description='Get information about medical specialties and specialists'
    )
    parser.add_argument(
        'specialty',
        nargs='?',
        help='Name of medical specialty'
    )
    parser.add_argument(
        '--doctors',
        '-d',
        action='store_true',
        help='Show specialist types in this field'
    )
    parser.add_argument(
        '--conditions',
        '-c',
        action='store_true',
        help='Show conditions treated by specialists'
    )
    parser.add_argument(
        '--procedures',
        '-p',
        action='store_true',
        help='Show procedures in this specialty'
    )
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Show detailed information'
    )

    args = parser.parse_args()

    if not args.specialty:
        parser.print_help()
        print("\nCommon Specialties:")
        print("  - cardiology      (Heart and cardiovascular system)")
        print("  - neurology       (Nervous system)")
        print("  - orthopedics     (Bones and joints)")
        print("  - dermatology     (Skin conditions)")
        print("  - psychiatry      (Mental health)")
        print("  - oncology        (Cancer treatment)")
        print("  - pediatrics      (Children's medicine)")
        sys.exit(1)

    try:
        result = get_speciality_info(args.specialty)
        if result:
            print(f"\nMedical Specialty: {args.specialty.title()}")
            print("=" * 60)
            print(result)

            if args.doctors:
                print("\n[Specialist types and sub-specialties]")
            if args.conditions:
                print("\n[Conditions and disorders treated]")
            if args.procedures:
                print("\n[Common procedures and interventions]")
        else:
            print(f"No information found for specialty: {args.specialty}")
            print("Tip: Try common specialty names like 'cardiology', 'neurology'")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

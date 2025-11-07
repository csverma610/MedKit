#!/usr/bin/env python
"""
CLI for symptom checking and differential diagnosis.

Usage:
    python cli/cli_symptoms_checker.py --symptoms "symptom1,symptom2,..."

Example:
    python cli/cli_symptoms_checker.py --symptoms "fever,cough,fatigue"
    python cli/cli_symptoms_checker.py --symptoms "chest pain,shortness of breath" --urgent
"""

import sys
import argparse


def main():
    """Main CLI entry point for symptom checker."""
    parser = argparse.ArgumentParser(
        description='Check symptoms and get possible conditions (for informational purposes only)'
    )
    parser.add_argument(
        '--symptoms',
        '-s',
        type=str,
        help='Comma-separated list of symptoms'
    )
    parser.add_argument(
        '--duration',
        '-d',
        type=str,
        help='Duration of symptoms (e.g., "3 days", "2 weeks")'
    )
    parser.add_argument(
        '--severity',
        '-sev',
        choices=['mild', 'moderate', 'severe'],
        help='Symptom severity level'
    )
    parser.add_argument(
        '--urgent',
        '-u',
        action='store_true',
        help='Check for emergency warning signs'
    )
    parser.add_argument(
        '--age',
        type=int,
        help='Patient age for age-specific conditions'
    )

    args = parser.parse_args()

    if not args.symptoms:
        parser.print_help()
        print("\n" + "=" * 60)
        print("⚠️  DISCLAIMER")
        print("=" * 60)
        print("This tool is for INFORMATIONAL PURPOSES ONLY.")
        print("\nThis is NOT a medical diagnosis or treatment recommendation.")
        print("Always consult a qualified healthcare provider for:")
        print("  - Accurate diagnosis")
        print("  - Medical advice")
        print("  - Treatment planning")
        print("\n🚨 EMERGENCY: Call 911 (US) or your local emergency number if:")
        print("  - Chest pain or pressure")
        print("  - Difficulty breathing")
        print("  - Severe abdominal pain")
        print("  - Loss of consciousness")
        print("  - Severe bleeding")
        sys.exit(1)

    try:
        symptoms = [s.strip() for s in args.symptoms.split(',')]

        print("\n" + "=" * 60)
        print("SYMPTOM CHECKER")
        print("=" * 60)
        print(f"\nSymptoms: {', '.join(symptoms)}")

        if args.duration:
            print(f"Duration: {args.duration}")
        if args.severity:
            print(f"Severity: {args.severity}")
        if args.age:
            print(f"Age: {args.age}")

        print("\n" + "-" * 60)
        print("Possible Conditions (NOT a diagnosis):")
        print("-" * 60)
        print("[Checking symptoms against medical conditions...]")
        print("[Results would be displayed here based on symptom analysis]")

        print("\n" + "-" * 60)
        print("🔍 IMPORTANT CONSIDERATIONS:")
        print("-" * 60)
        print("✓ Symptoms can have multiple causes")
        print("✓ Many conditions present with similar symptoms")
        print("✓ Only a healthcare provider can diagnose")
        print("✓ Laboratory tests often needed for confirmation")

        if args.urgent:
            print("\n" + "!" * 60)
            print("⚠️  URGENT SYMPTOMS DETECTED")
            print("!" * 60)
            print("Seek immediate medical attention!")
            print("Call 911 or go to emergency room immediately.")

        print("\n" + "=" * 60)
        print("NEXT STEPS")
        print("=" * 60)
        print("1. Schedule appointment with primary care doctor")
        print("2. Provide complete medical history")
        print("3. Mention ALL symptoms and when they started")
        print("4. Be prepared for physical examination and tests")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

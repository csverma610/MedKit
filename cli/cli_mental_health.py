#!/usr/bin/env python
"""
CLI for mental health assessments.

Usage:
    python cli/cli_mental_health.py [--assessment] [--chat]

Example:
    python cli/cli_mental_health.py --assessment
    python cli/cli_mental_health.py --chat
"""

import sys
import argparse
from medkit.mental_health.mental_health_assessment import assess_mental_health
from medkit.mental_health.mental_health_chat import chat_mental_health


def main():
    """Main CLI entry point for mental health tools."""
    parser = argparse.ArgumentParser(
        description='Mental health assessment and support tools'
    )
    parser.add_argument(
        '--assessment',
        '-a',
        action='store_true',
        help='Run mental health assessment'
    )
    parser.add_argument(
        '--chat',
        '-c',
        action='store_true',
        help='Start mental health chat'
    )
    parser.add_argument(
        '--interview',
        '-i',
        action='store_true',
        help='Start SANE interview'
    )
    parser.add_argument(
        '--anonymous',
        action='store_true',
        help='Run in anonymous mode'
    )

    args = parser.parse_args()

    if not (args.assessment or args.chat or args.interview):
        parser.print_help()
        print("\nNote: This tool provides mental health support information.")
        print("For immediate mental health crisis support, please contact:")
        print("  - National Suicide Prevention Lifeline: 988 (US)")
        print("  - Crisis Text Line: Text HOME to 741741")
        sys.exit(1)

    try:
        if args.assessment:
            print("\n" + "=" * 60)
            print("MENTAL HEALTH ASSESSMENT")
            print("=" * 60)
            print("\nPlease answer the following questions honestly.")
            print("Your responses will be kept confidential.\n")

            # In a real implementation, this would gather user responses
            print("Assessment tool ready...")
            print("[Implementation would gather user responses here]")

        elif args.chat:
            print("\n" + "=" * 60)
            print("MENTAL HEALTH CHAT")
            print("=" * 60)
            print("\nStarting conversation...")
            print("Type 'quit' or 'exit' to end conversation\n")

            # In a real implementation, this would start interactive chat
            print("Chat interface ready...")
            print("[Implementation would start interactive chat here]")

        elif args.interview:
            print("\n" + "=" * 60)
            print("SANE INTERVIEW")
            print("=" * 60)
            print("\nStructured assessment interview starting...")
            print("[Implementation would start SANE interview here]")

        print("\n" + "=" * 60)
        print("⚠️  IMPORTANT DISCLAIMER")
        print("=" * 60)
        print("This tool is for informational purposes only.")
        print("It does NOT replace professional mental health care.")
        print("If you are in crisis, please seek help immediately.")
        print("\nEmergency Numbers:")
        print("  - US: 988 (Suicide & Crisis Lifeline)")
        print("  - UK: 116 123 (Samaritans)")
        print("  - International: findahelpline.com")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

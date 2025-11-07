#!/usr/bin/env python
"""
CLI for medical physical examination question generation.

Usage:
    python cli/cli_physical_exams.py <exam_type>
    python cli/cli_physical_exams.py <exam_type> --age 45 --gender "Male"
    python cli/cli_physical_exams.py <exam_type> --age 30 --gender "Female" --output output.json
    python cli/cli_physical_exams.py <exam_type> --verbose

Examples:
    python cli/cli_physical_exams.py "Cardiovascular Exam"
    python cli/cli_physical_exams.py "Respiratory Exam" --age 55 --gender "Male"
    python cli/cli_physical_exams.py "Abdominal Exam" --age 45 --gender "Female" --verbose
    python cli/cli_physical_exams.py "Neurological Exam" --age 65 --output exam_questions.json
"""

import sys
import json
import argparse
from pathlib import Path
from medkit.medical.medical_physical_exams_questions import generate_exam_questions


def main():
    """Main CLI entry point for physical exam questions."""
    parser = argparse.ArgumentParser(
        description='Generate structured physical examination questions'
    )
    parser.add_argument(
        'exam_type',
        nargs='?',
        help='Type of physical examination (e.g., Cardiovascular Exam, Respiratory Exam)'
    )
    parser.add_argument(
        '--age',
        '-a',
        type=int,
        help='Patient age in years'
    )
    parser.add_argument(
        '--gender',
        '-g',
        help='Patient gender (Male/Female)'
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

    if not args.exam_type:
        parser.print_help()
        sys.exit(1)

    try:
        # Generate physical exam questions
        result = generate_exam_questions(
            exam_type=args.exam_type,
            age=args.age,
            gender=args.gender,
            verbose=args.verbose
        )
        
        if result:
            print(f"\n{'=' * 70}")
            print(f"Physical Examination Questions")
            print(f"{'=' * 70}")
            
            # Display exam details
            if hasattr(result, 'exam_type'):
                print(f"\nExam Type: {result.exam_type}")
            
            if hasattr(result, 'age') and result.age:
                print(f"Patient Age: {result.age} years")
            
            if hasattr(result, 'gender') and result.gender:
                print(f"Patient Gender: {result.gender}")
            
            # Display examination techniques
            if hasattr(result, 'examination_techniques'):
                print(f"\n--- EXAMINATION TECHNIQUES ---")
                if isinstance(result.examination_techniques, list):
                    for i, technique in enumerate(result.examination_techniques, 1):
                        print(f"\n{i}. {technique}")
                else:
                    print(result.examination_techniques)
            
            # Display inspection questions
            if hasattr(result, 'inspection_questions'):
                print(f"\n--- INSPECTION QUESTIONS ---")
                if isinstance(result.inspection_questions, list):
                    for i, question in enumerate(result.inspection_questions, 1):
                        print(f"{i}. {question}")
                else:
                    print(result.inspection_questions)
            
            # Display palpation questions
            if hasattr(result, 'palpation_questions'):
                print(f"\n--- PALPATION QUESTIONS ---")
                if isinstance(result.palpation_questions, list):
                    for i, question in enumerate(result.palpation_questions, 1):
                        print(f"{i}. {question}")
                else:
                    print(result.palpation_questions)
            
            # Display percussion questions
            if hasattr(result, 'percussion_questions'):
                print(f"\n--- PERCUSSION QUESTIONS ---")
                if isinstance(result.percussion_questions, list):
                    for i, question in enumerate(result.percussion_questions, 1):
                        print(f"{i}. {question}")
                else:
                    print(result.percussion_questions)
            
            # Display auscultation questions
            if hasattr(result, 'auscultation_questions'):
                print(f"\n--- AUSCULTATION QUESTIONS ---")
                if isinstance(result.auscultation_questions, list):
                    for i, question in enumerate(result.auscultation_questions, 1):
                        print(f"{i}. {question}")
                else:
                    print(result.auscultation_questions)
            
            # Display assessment questions
            if hasattr(result, 'assessment_questions'):
                print(f"\n--- ASSESSMENT QUESTIONS ---")
                if isinstance(result.assessment_questions, list):
                    for i, question in enumerate(result.assessment_questions, 1):
                        print(f"{i}. {question}")
                else:
                    print(result.assessment_questions)
            
            # Display clinical notes
            if hasattr(result, 'clinical_notes'):
                print(f"\n--- CLINICAL NOTES ---")
                print(result.clinical_notes)
            
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
                print(f"\n\n✓ Complete exam questions saved to: {output_path}")
            
            print(f"\n{'=' * 70}\n")
        
        else:
            print(f"Error: Could not generate exam questions for: {args.exam_type}")
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

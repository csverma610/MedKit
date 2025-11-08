#!/usr/bin/env python
"""
CLI for surgical procedure information.

Usage:
    python cli/cli_surgery_info.py <surgery_name>
    python cli/cli_surgery_info.py <surgery_name> --output output.json
    python cli/cli_surgery_info.py <surgery_name> --verbose

Examples:
    python cli/cli_surgery_info.py "Knee Replacement"
    python cli/cli_surgery_info.py "Coronary Artery Bypass" --verbose
    python cli/cli_surgery_info.py "Appendectomy" --output surgery_info.json
"""

import sys
import json
import argparse
from pathlib import Path
from medkit.medical.surgery_info import get_surgery_info


def main():
    """Main CLI entry point for surgery information."""
    parser = argparse.ArgumentParser(
        description='Get comprehensive information about surgical procedures'
    )
    parser.add_argument(
        'surgery',
        nargs='?',
        help='Name of the surgical procedure'
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

    if not args.surgery:
        parser.print_help()
        sys.exit(1)

    try:
        # Get surgery information
        result = get_surgery_info(args.surgery)
        
        if result:
            print(f"\n{'=' * 70}")
            print(f"Surgical Procedure Information")
            print(f"{'=' * 70}")
            
            # Display metadata
            if hasattr(result, 'metadata'):
                metadata = result.metadata
                print(f"\nProcedure: {metadata.surgery_name}")
                if hasattr(metadata, 'alternative_names'):
                    print(f"Alternative Names: {metadata.alternative_names}")
                if hasattr(metadata, 'procedure_code'):
                    print(f"Procedure Code: {metadata.procedure_code}")
                if hasattr(metadata, 'surgery_category'):
                    print(f"Category: {metadata.surgery_category}")
                if hasattr(metadata, 'body_systems_involved'):
                    print(f"Body Systems Involved: {metadata.body_systems_involved}")
            
            # Display indications
            if hasattr(result, 'indications'):
                indications = result.indications
                print(f"\n--- INDICATIONS ---")
                if hasattr(indications, 'absolute_indications'):
                    print(f"Absolute Indications: {indications.absolute_indications}")
                if hasattr(indications, 'relative_indications'):
                    print(f"Relative Indications: {indications.relative_indications}")
                if hasattr(indications, 'emergency_indications'):
                    print(f"Emergency Indications: {indications.emergency_indications}")
                if hasattr(indications, 'absolute_contraindications'):
                    print(f"Absolute Contraindications: {indications.absolute_contraindications}")
                if hasattr(indications, 'relative_contraindications'):
                    print(f"Relative Contraindications: {indications.relative_contraindications}")
            
            # Display preoperative information
            if hasattr(result, 'preoperative_phase'):
                preop = result.preoperative_phase
                print(f"\n--- PREOPERATIVE PHASE ---")
                if hasattr(preop, 'patient_evaluation'):
                    print(f"Patient Evaluation: {preop.patient_evaluation}")
                if hasattr(preop, 'preoperative_testing'):
                    print(f"Preoperative Testing: {preop.preoperative_testing}")
                if hasattr(preop, 'risk_stratification'):
                    print(f"Risk Stratification: {preop.risk_stratification}")
                if hasattr(preop, 'patient_counseling'):
                    print(f"Patient Counseling: {preop.patient_counseling}")
            
            # Display operative information
            if hasattr(result, 'operative_phase'):
                op = result.operative_phase
                print(f"\n--- OPERATIVE PHASE ---")
                if hasattr(op, 'surgical_approaches'):
                    print(f"Surgical Approaches: {op.surgical_approaches}")
                if hasattr(op, 'anesthesia'):
                    print(f"Anesthesia: {op.anesthesia}")
                if hasattr(op, 'procedure_steps'):
                    print(f"Procedure Steps: {op.procedure_steps}")
                if hasattr(op, 'estimated_duration'):
                    print(f"Estimated Duration: {op.estimated_duration}")
            
            # Display postoperative information
            if hasattr(result, 'postoperative_phase'):
                postop = result.postoperative_phase
                print(f"\n--- POSTOPERATIVE PHASE ---")
                if hasattr(postop, 'pain_management'):
                    print(f"Pain Management: {postop.pain_management}")
                if hasattr(postop, 'monitoring'):
                    print(f"Monitoring: {postop.monitoring}")
                if hasattr(postop, 'discharge_criteria'):
                    print(f"Discharge Criteria: {postop.discharge_criteria}")
            
            # Display recovery information
            if hasattr(result, 'recovery_timeline'):
                recovery = result.recovery_timeline
                print(f"\n--- RECOVERY TIMELINE ---")
                if hasattr(recovery, 'hospital_stay'):
                    print(f"Hospital Stay: {recovery.hospital_stay}")
                if hasattr(recovery, 'return_to_normal_activities'):
                    print(f"Return to Normal Activities: {recovery.return_to_normal_activities}")
                if hasattr(recovery, 'return_to_work'):
                    print(f"Return to Work: {recovery.return_to_work}")
                if hasattr(recovery, 'success_rates'):
                    print(f"Success Rates: {recovery.success_rates}")
            
            # Display risks
            if hasattr(result, 'operative_risks'):
                print(f"\n--- OPERATIVE RISKS ---")
                print(f"{result.operative_risks}")
            
            # Display alternatives
            if hasattr(result, 'alternative_treatments'):
                print(f"\n--- ALTERNATIVE TREATMENTS ---")
                print(f"{result.alternative_treatments}")
            
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
                print(f"\n\n✓ Complete surgery information saved to: {output_path}")
            
            print(f"\n{'=' * 70}\n")
        
        else:
            print(f"No information found for: {args.surgery}")
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

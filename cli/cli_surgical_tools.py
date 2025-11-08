#!/usr/bin/env python
"""
CLI for surgical tool and instrument information.

Usage:
    python cli/cli_surgical_tools.py <tool_name>
    python cli/cli_surgical_tools.py <tool_name> --output output.json
    python cli/cli_surgical_tools.py <tool_name> --verbose

Examples:
    python cli/cli_surgical_tools.py scalpel
    python cli/cli_surgical_tools.py "surgical retractor" --verbose
    python cli/cli_surgical_tools.py forceps --output forceps_info.json
"""

import sys
import json
import argparse
from pathlib import Path
from medkit.medical.surgical_tool_info import get_surgical_tool_info


def main():
    """Main CLI entry point for surgical tool information."""
    parser = argparse.ArgumentParser(
        description='Get information about surgical tools and instruments'
    )
    parser.add_argument(
        'tool',
        nargs='?',
        help='Name of the surgical tool or instrument'
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

    if not args.tool:
        parser.print_help()
        sys.exit(1)

    try:
        # Get surgical tool information
        result = get_surgical_tool_info(args.tool)
        
        if result:
            print(f"\n{'=' * 70}")
            print(f"Surgical Tool Information")
            print(f"{'=' * 70}")
            
            # Display basic information
            if hasattr(result, 'tool_name'):
                print(f"\nTool: {result.tool_name}")
            
            if hasattr(result, 'tool_type'):
                print(f"Type: {result.tool_type}")
            
            if hasattr(result, 'primary_use'):
                print(f"Primary Use: {result.primary_use}")
            
            # Display description
            if hasattr(result, 'description'):
                print(f"\n--- DESCRIPTION ---")
                print(f"{result.description}")
            
            # Display design and construction
            if hasattr(result, 'design_and_construction'):
                print(f"\n--- DESIGN AND CONSTRUCTION ---")
                print(f"{result.design_and_construction}")
            
            # Display how it works
            if hasattr(result, 'how_it_works'):
                print(f"\n--- HOW IT WORKS ---")
                print(f"{result.how_it_works}")
            
            # Display surgical procedures
            if hasattr(result, 'surgical_procedures'):
                print(f"\n--- USED IN PROCEDURES ---")
                print(f"{result.surgical_procedures}")
            
            # Display handling and technique
            if hasattr(result, 'handling_and_technique'):
                print(f"\n--- HANDLING AND TECHNIQUE ---")
                print(f"{result.handling_and_technique}")
            
            # Display sterilization
            if hasattr(result, 'sterilization_and_maintenance'):
                print(f"\n--- STERILIZATION AND MAINTENANCE ---")
                print(f"{result.sterilization_and_maintenance}")
            
            # Display safety considerations
            if hasattr(result, 'safety_considerations'):
                print(f"\n--- SAFETY CONSIDERATIONS ---")
                print(f"{result.safety_considerations}")
            
            # Display variations
            if hasattr(result, 'tool_variations'):
                print(f"\n--- TOOL VARIATIONS ---")
                print(f"{result.tool_variations}")
            
            # Display cost and availability
            if hasattr(result, 'cost_and_availability'):
                print(f"\n--- COST AND AVAILABILITY ---")
                print(f"{result.cost_and_availability}")
            
            # Display advantages and limitations
            if hasattr(result, 'advantages'):
                print(f"\n--- ADVANTAGES ---")
                print(f"{result.advantages}")
            
            if hasattr(result, 'limitations'):
                print(f"\n--- LIMITATIONS ---")
                print(f"{result.limitations}")
            
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
                print(f"\n\n✓ Complete tool information saved to: {output_path}")
            
            print(f"\n{'=' * 70}\n")
        
        else:
            print(f"No information found for tool: {args.tool}")
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

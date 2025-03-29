"""
Command-line interface for the Atomorph converter.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from atomorph.converter.core.converter import StructureConverter
from typing import Optional, List, Dict, Union

def parse_args() -> argparse.Namespace:
    """
    Parse command line arguments.
    
    Returns:
        Parsed command line arguments
    """
    parser = argparse.ArgumentParser(
        description='Convert atomic structure files between different formats',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic conversion
  conv input.cif output.vasp

  # Sort atoms by atomic number
  conv input.cif output.vasp -s ascending

  # Custom element ordering
  conv input.cif output.vasp -e "Au,Pt,Ag,Cu,Fe"

  # Add atomic constraints
  conv input.cif output.vasp -c fixed
  conv input.cif output.vasp -c elements "Fe,Cu"

  # Multi-frame processing
  conv input.cif output/ -m multi
  conv input.cif output/ -m multi -d -f "1,3,4-10"

  # Parallel processing
  conv input.cif output.vasp -p
        """
    )
    
    # Required arguments
    parser.add_argument('input_path', help='Input file path')
    parser.add_argument('output_path', help='Output file path')
    
    # Optional arguments
    parser.add_argument('-m', '--mode', choices=['single', 'multi'], default='single', help='Conversion mode (default: single)')
    parser.add_argument('-s', '--sort', choices=['ascending', 'descending'], help='Sort atoms by element type')
    parser.add_argument('-e', '--elements', help='Custom element ordering (comma-separated)')
    parser.add_argument('-c', '--constraints', help='Add atomic constraints (fixed, elements, or layers)')
    parser.add_argument('-d', '--separate-dirs', action='store_true', help='Save each frame in separate directories (multi-frame mode)')
    parser.add_argument('-f', '--frames', help='Frame selection (multi-frame mode)')
    parser.add_argument('-p', '--parallel', action='store_true', help='Enable parallel processing')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    
    return parser.parse_args()

def parse_constraints(constraints_str: str) -> Optional[Union[str, List[str], List[Dict[str, float]]]]:
    """
    Parse constraints string into appropriate format.
    
    Args:
        constraints_str: Constraints string
        
    Returns:
        Parsed constraints
    """
    if not constraints_str:
        return None
        
    if constraints_str == 'fixed':
        return 'fixed'
        
    if constraints_str.startswith('elements:'):
        elements = constraints_str[9:].split(',')
        return elements
        
    if constraints_str.startswith('layers:'):
        layers_str = constraints_str[7:]
        layers = []
        for layer in layers_str.split(';'):
            start, end = map(float, layer.split(','))
            layers.append({'start': start, 'end': end})
        return layers
        
    return None

def main() -> None:
    """Main entry point for the command-line interface."""
    args = parse_args()
    
    # Initialize converter
    converter = StructureConverter()
    
    # Parse constraints
    constraints = parse_constraints(args.constraints)
    
    # Parse elements if provided
    elements = args.elements.split(',') if args.elements else None
    
    try:
        # Handle output path for multi-frame mode
        if args.mode == 'multi' and args.separate_dirs:
            if not args.output_path.endswith('/'):
                args.output_path += '/'
            os.makedirs(args.output_path, exist_ok=True)
        
        # Convert structure
        converter.convert(
            input_path=args.input_path,
            output_path=args.output_path,
            mode=args.mode,
            frame=args.frames,
            element_mapping=elements,
            constraints=constraints,
            sort_type=args.sort,
            separate_dirs=args.separate_dirs,
            parallel=args.parallel
        )
        print(f"Conversion completed! Output file: {args.output_path}")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    
    return 0

if __name__ == '__main__':
    exit(main()) 
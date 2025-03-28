import argparse
import json
import os
import sys
from pathlib import Path
from atomorph.converter.core.converter import StructureConverter

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Convert atomic structure files between different formats',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic conversion
  conv input.cif output.vasp

  # Specify input/output formats
  conv input.xyz output.vasp -i xyz -o vasp

  # Convert specific frame from multi-frame file
  conv input.xyz output.vasp -f 0

  # Convert in multi-frame mode
  conv input.xyz output/ -m multi

  # Conversion with ascending element sorting
  conv input.cif output.vasp -s ascending

  # Conversion with descending element sorting
  conv input.cif output.vasp -s descending

  # Conversion with custom element order
  conv input.cif output.vasp -e Au Pt Ag Cu Fe

  # Conversion with atomic constraints
  conv input.cif output.vasp -c constraints.json

  # Multi-frame conversion with parallel processing
  conv input.cif output/ -p

  # Combined usage
  conv input.xyz output.vasp -i xyz -o vasp -f 0 -s ascending -p

Configuration Files:
  constraints.json:
  {
      "fixed_atoms": [0, 2],           // Fix specific atoms (0-based index)
      "fixed_elements": ["Fe", "Cu"],  // Fix all atoms of specified elements
      "fixed_layers": [0],             // Fix atoms in specified layers (counted from bottom)
      "layer_thickness": 1.0           // Layer thickness in Angstroms
  }

  element_order.json:
  {
      "elements": ["Au", "Pt", "Ag", "Cu", "Fe"]
  }
        """
    )
    
    # Required arguments
    parser.add_argument('input_path', help='Input file path')
    parser.add_argument('output_path', help='Output file path')
    
    # Optional arguments
    parser.add_argument('-i', '--input-format', default='cif', help='Input file format (default: cif)')
    parser.add_argument('-o', '--output-format', default='vasp', help='Output file format (default: vasp)')
    parser.add_argument('-m', '--mode', choices=['single', 'multi'], default='single', help='Conversion mode (default: single)')
    parser.add_argument('-f', '--frame', type=int, help='Select specific frame for multi-frame files')
    parser.add_argument('-s', '--sort', choices=['ascending', 'descending'], help='Sort elements by atomic number')
    parser.add_argument('-e', '--elements', nargs='+', help='Specify element order (e.g., -e Au Pt Ag Cu Fe)')
    parser.add_argument('-c', '--constraints', help='Path to constraints configuration file (JSON format)')
    parser.add_argument('-p', '--parallel', action='store_true', help='Enable parallel processing for multi-frame files')
    
    return parser.parse_args()

def main():
    """Main function"""
    args = parse_args()
    
    # Initialize converter
    converter = StructureConverter()
    
    # Set sorting parameters
    if args.sort:
        converter.sort_order = args.sort
    if args.elements:
        converter.element_order = args.elements
    
    # Load constraints if specified
    constraints = None
    if args.constraints:
        with open(args.constraints) as f:
            constraints = json.load(f)
    
    try:
        # 处理输出路径
        if args.mode == 'multi':
            if not args.output_path.endswith('/'):
                args.output_path += '/'
            os.makedirs(args.output_path, exist_ok=True)
        
        # 转换结构
        converter.convert(
            input_path=args.input_path,
            output_path=args.output_path,
            input_format=args.input_format,
            output_format=args.output_format,
            mode=args.mode,
            constraints=constraints,
            multi_frame=args.mode == 'multi',
            parallel=args.parallel
        )
        print(f"转换完成！输出文件：{args.output_path}")
    except Exception as e:
        print(f"Error: 转换失败：{str(e)}")
        sys.exit(1)
    
    return 0

if __name__ == '__main__':
    exit(main()) 
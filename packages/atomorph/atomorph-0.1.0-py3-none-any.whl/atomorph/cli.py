#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Command line interface for Atomorph
"""

import argparse
import json
from pathlib import Path
from typing import Dict, Optional

from atomorph.converter.core.converter import StructureConverter

def load_json_config(config_path: str) -> Dict:
    """Load JSON configuration file"""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        raise ValueError(f"Failed to load configuration file: {str(e)}")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Convert atomic structure files between different formats"
    )
    
    parser.add_argument(
        "input_path",
        help="Input file path"
    )
    
    parser.add_argument(
        "output_path",
        help="Output file path"
    )
    
    parser.add_argument(
        "-i", "--input-format",
        help="Input file format"
    )
    
    parser.add_argument(
        "-o", "--output-format",
        help="Output file format"
    )
    
    parser.add_argument(
        "-m", "--mode",
        choices=["single", "multi"],
        help="Conversion mode (single/multi)"
    )
    
    parser.add_argument(
        "-f", "--frame",
        type=int,
        help="Select specific frame"
    )
    
    parser.add_argument(
        "-e", "--element-mapping",
        help="Element mapping configuration file"
    )
    
    parser.add_argument(
        "-c", "--constraints",
        help="Atomic constraints configuration file"
    )
    
    args = parser.parse_args()
    
    # Load configurations if provided
    element_mapping = None
    if args.element_mapping:
        element_mapping = load_json_config(args.element_mapping)
    
    constraints = None
    if args.constraints:
        constraints = load_json_config(args.constraints)
    
    # Create converter instance
    converter = StructureConverter()
    
    try:
        # Perform conversion
        converter.convert(
            args.input_path,
            args.output_path,
            input_format=args.input_format,
            output_format=args.output_format,
            mode=args.mode,
            frame=args.frame,
            element_mapping=element_mapping,
            constraints=constraints,
        )
        print(f"Conversion successful: {args.input_path} -> {args.output_path}")
    except Exception as e:
        print(f"Conversion failed: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main() 
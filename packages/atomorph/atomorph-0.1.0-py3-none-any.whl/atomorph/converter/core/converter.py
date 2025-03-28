#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Atomorph Core Converter
"""

import os
import warnings
from pathlib import Path
from typing import Dict, List, Optional, Union
import ase.io
from ase import Atoms

# Filter out ASE spacegroup warnings
warnings.filterwarnings("ignore", category=UserWarning, module="ase.spacegroup.spacegroup")

class StructureConverter:
    """Atomic structure converter"""
    
    def __init__(self):
        """Initialize the converter"""
        self.single_frame_only_formats = ["vasp"]
        self.format_mapping = {
            "xyz": "extxyz",  # Map xyz to extxyz
            "extxyz": "extxyz"
        }
    
    def convert(
        self,
        input_path: Union[str, Path],
        output_path: Union[str, Path],
        input_format: Optional[str] = None,
        output_format: Optional[str] = None,
        mode: Optional[str] = None,
        frame: Optional[int] = None,
        element_mapping: Optional[Dict[str, str]] = None,
        constraints: Optional[Dict[str, Union[List[int], bool]]] = None,
    ) -> None:
        """
        Convert atomic structure files
        
        Args:
            input_path: Input file path
            output_path: Output file path
            input_format: Input file format
            output_format: Output file format
            mode: Conversion mode (single/multi)
            frame: Select specific frame
            element_mapping: Element mapping configuration
            constraints: Atomic constraints configuration
        """
        # Convert paths to Path objects
        input_path = Path(input_path)
        output_path = Path(output_path)
        
        # Auto-detect file format
        if input_format is None:
            input_format = input_path.suffix[1:]
        if output_format is None:
            output_format = output_path.suffix[1:]
            
        # Map file formats
        input_format = self.format_mapping.get(input_format, input_format)
        output_format = self.format_mapping.get(output_format, output_format)
        
        # Auto-detect mode
        if mode is None:
            mode = self._detect_mode(input_path, input_format)
        
        # Validate mode
        self._validate_mode(mode, output_format)
        
        # Read structures
        structures = self._read_structures(input_path, input_format, frame)
        
        # Apply element mapping
        if element_mapping:
            structures = self._apply_element_mapping(structures, element_mapping)
        
        # Apply atomic constraints
        if constraints:
            structures = self._apply_constraints(structures, constraints)
        
        # Handle output
        self._handle_output(structures, output_path, output_format, mode)
    
    def _detect_mode(self, input_path: Path, input_format: str) -> str:
        """Detect conversion mode"""
        try:
            structures = ase.io.read(input_path, format=input_format, index=":")
            return "multi" if len(structures) > 1 else "single"
        except Exception:
            return "single"
    
    def _validate_mode(self, mode: str, output_format: str) -> None:
        """Validate conversion mode"""
        if mode == "multi" and output_format in self.single_frame_only_formats:
            if isinstance(output_format, str) and Path(output_format).suffix:
                raise ValueError(f"Output format {output_format} does not support multi-frame structures. Please choose another output format or use single-frame mode.")
    
    def _read_structures(
        self,
        input_path: Path,
        input_format: str,
        frame: Optional[int] = None,
    ) -> List[Atoms]:
        """Read structures"""
        try:
            if frame is not None:
                structures = [ase.io.read(input_path, format=input_format, index=frame-1)]
            else:
                try:
                    # Try to read all frames
                    structures = ase.io.read(input_path, format=input_format, index=":")
                except Exception:
                    # If failed, try to read single frame
                    structures = [ase.io.read(input_path, format=input_format)]
                
                if not isinstance(structures, list):
                    structures = [structures]
            
            # Ensure all structures have lattice
            for structure in structures:
                if structure.cell.rank < 3:
                    # Set default lattice
                    structure.set_cell([10.0, 10.0, 10.0])
                    structure.center()
            
            return structures
        except Exception as e:
            raise ValueError(f"Failed to read file: {str(e)}")
    
    def _apply_element_mapping(
        self,
        structures: List[Atoms],
        element_mapping: Dict[str, str],
    ) -> List[Atoms]:
        """Apply element mapping"""
        for structure in structures:
            symbols = structure.get_chemical_symbols()
            for i, symbol in enumerate(symbols):
                if symbol in element_mapping:
                    symbols[i] = element_mapping[symbol]
            structure.set_chemical_symbols(symbols)
        return structures
    
    def _apply_constraints(
        self,
        structures: List[Atoms],
        constraints: Dict[str, Union[List[int], bool, str, float]],
    ) -> List[Atoms]:
        """Apply atomic constraints"""
        from ase.constraints import FixAtoms
        
        fixed_atoms = []
        selective_dynamics = constraints.get("selective_dynamics", False)
        
        # Handle different types of constraints
        if "fixed_atoms" in constraints:
            # Fix by atom indices
            fixed_atoms.extend(constraints["fixed_atoms"])
        
        if "fixed_elements" in constraints:
            # Fix by element symbols
            for structure in structures:
                symbols = structure.get_chemical_symbols()
                for i, symbol in enumerate(symbols):
                    if symbol in constraints["fixed_elements"]:
                        fixed_atoms.append(i)
        
        if "fixed_layers" in constraints:
            # Fix by z-coordinate layers
            layer_thickness = constraints.get("layer_thickness", 1.0)
            for structure in structures:
                positions = structure.get_positions()
                z_coords = positions[:, 2]
                min_z = min(z_coords)
                max_z = max(z_coords)
                
                # Calculate number of layers
                n_layers = int((max_z - min_z) / layer_thickness) + 1
                
                # Fix atoms in specified layers
                for layer in constraints["fixed_layers"]:
                    if 0 <= layer < n_layers:
                        layer_min = min_z + layer * layer_thickness
                        layer_max = layer_min + layer_thickness
                        for i, z in enumerate(z_coords):
                            if layer_min <= z < layer_max:
                                fixed_atoms.append(i)
        
        # Remove duplicates and sort
        fixed_atoms = sorted(set(fixed_atoms))
        
        # Apply constraints
        for structure in structures:
            if fixed_atoms:
                constraint = FixAtoms(indices=fixed_atoms)
                structure.set_constraint(constraint)
        
        return structures
    
    def _handle_output(
        self,
        structures: List[Atoms],
        output_path: Path,
        output_format: str,
        mode: str = "single",
    ) -> None:
        """Handle output"""
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            if mode == "single":
                # Single frame mode: write directly to file
                if structures:
                    ase.io.write(output_path, structures[0], format=output_format)
            else:
                # Multi-frame mode: choose write method based on format
                if output_format in self.single_frame_only_formats:
                    # Formats not supporting multi-frame: create directory and write separately
                    output_path.mkdir(parents=True, exist_ok=True)
                    for i, structure in enumerate(structures):
                        frame_path = output_path / f"frame_{i:04d}.{output_format}"
                        ase.io.write(frame_path, structure, format=output_format)
                else:
                    # Formats supporting multi-frame: write directly
                    ase.io.write(output_path, structures, format=output_format)
        except Exception as e:
            raise ValueError(f"Failed to write file: {str(e)}") 
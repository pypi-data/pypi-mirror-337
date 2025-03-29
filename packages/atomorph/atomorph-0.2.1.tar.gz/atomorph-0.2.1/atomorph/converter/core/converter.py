#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Core conversion functionality for atomic structure files.
"""

import os
import warnings
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
import ase.io
from ase import Atoms
import sys
from ase.io import read, write
from ase.constraints import FixAtoms
import numpy as np
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial
import multiprocessing

# Filter out ASE spacegroup warnings
warnings.filterwarnings("ignore", category=UserWarning, module="ase.spacegroup.spacegroup")

class StructureConverter:
    """A class for converting atomic structure files between different formats."""
    
    # Default element order (periodic table order)
    DEFAULT_ELEMENT_ORDER = [
        "H", "He",
        "Li", "Be", "B", "C", "N", "O", "F", "Ne",
        "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar",
        "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr",
        "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe",
        "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu",
        "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn",
        "Fr", "Ra", "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr",
        "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og"
    ]

    def __init__(self):
        """Initialize the StructureConverter."""
        self.single_frame_only_formats = ["vasp"]
        self.format_mapping = {
            "xyz": "extxyz",  # Map xyz to extxyz
            "extxyz": "extxyz"
        }
        self._element_order = None
        self._constraints = None
        self._layer_constraints = None
        self.sort_order = "ascending"  # Default ascending sort
        self.MAX_FILE_SIZE = 100 * 1024 * 1024 * 1024  # 100GB
        self.MAX_WORKERS = os.cpu_count() or 4  # Use CPU cores or default to 4 threads
    
    def _get_element_position(self, element: str) -> int:
        """
        Get the position of an element in the periodic table.
        
        Args:
            element: Element symbol
            
        Returns:
            Position in the periodic table
        """
        try:
            return self.DEFAULT_ELEMENT_ORDER.index(element)
        except ValueError:
            return len(self.DEFAULT_ELEMENT_ORDER)  # Put unknown elements at the end
    
    def _check_file_size(self, file_path):
        """Check if file size exceeds limit"""
        file_size = os.path.getsize(file_path)
        if file_size > self.MAX_FILE_SIZE:
            raise ValueError(f"File size ({file_size/1024/1024/1024:.2f}GB) exceeds limit ({self.MAX_FILE_SIZE/1024/1024/1024:.2f}GB)")

    def _show_progress(self, total, desc="Processing"):
        """Show progress bar"""
        return tqdm(total=total, desc=desc, unit="frame")

    def _process_frame(self, frame, output_path, constraints):
        """Process a single structure frame"""
        try:
            self._write_vasp(frame, output_path, constraints)
            return True, output_path
        except Exception as e:
            return False, str(e)

    def convert(
        self,
        input_path: Union[str, Path],
        output_path: Union[str, Path],
        input_format: Optional[str] = None,
        output_format: Optional[str] = None,
        mode: Optional[str] = None,
        frame: Optional[str] = None,
        element_mapping: Optional[Dict[str, str]] = None,
        constraints: Optional[Union[str, List[str]]] = None,
        layer_constraints: Optional[List[Dict[str, float]]] = None,
        sort_type: Optional[str] = None,
        parallel: bool = True,
        multi_frame: bool = False,
        separate_dirs: bool = False
    ) -> None:
        """
        Convert atomic structure file.
        
        Args:
            input_path: Input file path
            output_path: Output file path
            input_format: Input file format
            output_format: Output file format
            mode: Conversion mode ('single' or 'multi')
            frame: Frame selection string
            element_mapping: Element mapping dictionary
            constraints: Atomic constraints
            layer_constraints: Layer-based constraints
            sort_type: Sort type for atoms
            parallel: Whether to use parallel processing
            multi_frame: Whether to process multiple frames
            separate_dirs: Whether to save frames in separate directories
        """
        try:
            # Check file size
            self._check_file_size(input_path)
            
            # Set options
            self._element_order = element_mapping
            self._constraints = constraints
            self._layer_constraints = layer_constraints
            
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
                mode = "multi" if multi_frame else "single"
            
            # Validate mode
            self._validate_mode(mode, output_format)
            
            # Parse frame selection
            frame_indices = self._parse_frame_selection(frame) if frame else None
            
            # Read structures
            structures = self._read_structures(input_path, input_format, frame)
            
            # Apply transformations
            if sort_type:
                structures = self._sort_atoms(structures, sort_type)
            if self._element_order:
                structures = self._apply_element_order(structures)
            if self._constraints:
                structures = self._apply_constraints(structures)
            if self._layer_constraints:
                structures = self._apply_layer_constraints(structures)
            
            # Handle output
            if output_format == "vasp":
                # For VASP format, use custom write function
                if mode == "single":
                    self._write_vasp(structures[0], output_path, constraints)
                else:
                    # Create output directory
                    output_path.mkdir(parents=True, exist_ok=True)
                    if parallel:
                        # Parallel processing for multi-frame
                        print(f"Using {self.MAX_WORKERS} threads for parallel processing...")
                        with ThreadPoolExecutor(max_workers=self.MAX_WORKERS) as executor:
                            # Create task list
                            futures = []
                            for i, structure in enumerate(structures):
                                if separate_dirs:
                                    # Use original frame index for directory name
                                    frame_idx = frame_indices[i] if frame_indices else i
                                    frame_dir = output_path / f"frame_{frame_idx+1}"
                                    frame_dir.mkdir(exist_ok=True)
                                    frame_output = frame_dir / "POSCAR"
                                else:
                                    frame_output = output_path / f"frame_{i+1}.vasp"
                                future = executor.submit(self._process_frame, structure, frame_output, constraints)
                                futures.append(future)
                            
                            # Show progress with progress bar
                            with self._show_progress(len(futures), "Processing frames") as pbar:
                                for future in as_completed(futures):
                                    success, result = future.result()
                                    if not success:
                                        print(f"Warning: Processing failed - {result}")
                                    pbar.update(1)
                    else:
                        # Serial processing for multi-frame
                        with self._show_progress(len(structures), "Processing frames") as pbar:
                            for i, structure in enumerate(structures):
                                if separate_dirs:
                                    # Use original frame index for directory name
                                    frame_idx = frame_indices[i] if frame_indices else i
                                    frame_dir = output_path / f"frame_{frame_idx+1}"
                                    frame_dir.mkdir(exist_ok=True)
                                    frame_output = frame_dir / "POSCAR"
                                else:
                                    frame_output = output_path / f"frame_{i+1}.vasp"
                                self._write_vasp(structure, frame_output, constraints)
                                pbar.update(1)
            else:
                # For other formats, use ASE's write function
                if mode == "single":
                    ase.io.write(output_path, structures[0], format=output_format)
                else:
                    if output_format in self.single_frame_only_formats:
                        # Create output directory
                        output_path.mkdir(parents=True, exist_ok=True)
                        for i, structure in enumerate(structures):
                            if separate_dirs:
                                # Use original frame index for directory name
                                frame_idx = frame_indices[i] if frame_indices else i
                                frame_dir = output_path / f"frame_{frame_idx+1}"
                                frame_dir.mkdir(exist_ok=True)
                                frame_output = frame_dir / f"structure.{output_format}"
                            else:
                                frame_output = output_path / f"frame_{i+1}.{output_format}"
                            ase.io.write(frame_output, structure, format=output_format)
                    else:
                        ase.io.write(output_path, structures, format=output_format)
            
            print(f"Conversion completed! Output file: {output_path}")
            
        except Exception as e:
            raise ValueError(f"Conversion failed: {str(e)}")
    
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
    
    def _parse_frame_selection(self, frame_str: str) -> List[int]:
        """
        Parse frame selection string into a list of frame indices.
        
        Args:
            frame_str: Frame selection string (e.g., "1,3,4-10")
            
        Returns:
            List of frame indices (0-based)
        """
        if not frame_str:
            return []
            
        indices = set()
        parts = frame_str.split(',')
        
        for part in parts:
            if '-' in part:
                start, end = map(int, part.split('-'))
                indices.update(range(start-1, end))
            else:
                indices.add(int(part)-1)
                
        return sorted(list(indices))

    def _read_structures(
        self,
        input_path: Path,
        input_format: str,
        frame: Optional[str] = None,
    ) -> List[Atoms]:
        """Read structures"""
        try:
            # Read all frames first
            all_structures = ase.io.read(input_path, format=input_format, index=":")
            if not isinstance(all_structures, list):
                all_structures = [all_structures]
            
            if frame is not None:
                # Parse frame selection
                frame_indices = self._parse_frame_selection(frame)
                if not frame_indices:
                    raise ValueError("Invalid frame selection format")
                
                # Select specified frames
                structures = []
                for idx in frame_indices:
                    if 0 <= idx < len(all_structures):
                        structures.append(all_structures[idx])
                    else:
                        print(f"Warning: Frame {idx+1} out of range, skipping")
            else:
                structures = all_structures
            
            # Ensure all structures have lattice
            for structure in structures:
                if structure.cell.rank < 3:
                    # Set default lattice
                    structure.set_cell([10.0, 10.0, 10.0])
                    structure.center()
            
            return structures
        except Exception as e:
            raise ValueError(f"Failed to read file: {str(e)}")
    
    def _apply_element_order(self, atoms: Atoms) -> Atoms:
        """
        Apply custom element ordering.
        
        Args:
            atoms: ASE Atoms object
            
        Returns:
            Reordered ASE Atoms object
        """
        if not self._element_order:
            return atoms
            
        # Get current symbols and positions
        symbols = atoms.get_chemical_symbols()
        positions = atoms.get_positions()
        
        # Create new ordering
        new_indices = []
        for element in self._element_order:
            element_indices = [i for i, s in enumerate(symbols) if s == element]
            new_indices.extend(element_indices)
            
        # Create new atoms object with reordered elements
        new_atoms = Atoms(
            symbols=[symbols[i] for i in new_indices],
            positions=positions[new_indices],
            cell=atoms.get_cell(),
            pbc=atoms.get_pbc()
        )
        
        return new_atoms
    
    def _apply_constraints(self, atoms: Atoms) -> Atoms:
        """
        Apply atomic constraints.
        
        Args:
            atoms: ASE Atoms object
            
        Returns:
            Constrained ASE Atoms object
        """
        if not self._constraints:
            return atoms
            
        # Create mask for fixed atoms
        mask = np.zeros(len(atoms), dtype=bool)
        if self._constraints == 'fixed':
            mask[:] = True
        else:
            symbols = atoms.get_chemical_symbols()
            for element in self._constraints:
                mask[symbols == element] = True
                
        # Apply constraints
        constraints = FixAtoms(mask=mask)
        atoms.set_constraint(constraints)
        
        return atoms
    
    def _apply_layer_constraints(self, atoms: Atoms) -> Atoms:
        """
        Apply layer-based constraints.
        
        Args:
            atoms: ASE Atoms object
            
        Returns:
            Constrained ASE Atoms object
        """
        if not self._layer_constraints:
            return atoms
            
        # Get atomic positions and cell
        positions = atoms.get_positions()
        cell = atoms.get_cell()
        
        # Calculate layer positions
        layer_positions = positions[:, 2] / cell[2, 2]
        
        # Create mask for fixed atoms
        mask = np.zeros(len(atoms), dtype=bool)
        for layer in self._layer_constraints:
            layer_mask = (layer_positions >= layer['start']) & (layer_positions <= layer['end'])
            mask[layer_mask] = True
            
        # Apply constraints
        constraints = FixAtoms(mask=mask)
        atoms.set_constraint(constraints)
        
        return atoms
    
    def _sort_atoms(self, atoms: Atoms, sort_type: str = 'ascending') -> Atoms:
        """
        Sort atoms by element type.
        
        Args:
            atoms: ASE Atoms object
            sort_type: 'ascending' or 'descending'
            
        Returns:
            Sorted ASE Atoms object
        """
        if not sort_type:
            return atoms
            
        # Get atomic numbers and indices
        numbers = atoms.get_atomic_numbers()
        indices = np.arange(len(atoms))
        
        # Sort based on atomic numbers
        if sort_type == 'ascending':
            sort_idx = np.argsort(numbers)
        else:  # descending
            sort_idx = np.argsort(numbers)[::-1]
            
        # Create new atoms object with sorted positions
        new_atoms = Atoms(
            symbols=atoms.get_chemical_symbols()[sort_idx],
            positions=atoms.get_positions()[sort_idx],
            cell=atoms.get_cell(),
            pbc=atoms.get_pbc()
        )
        
        return new_atoms
    
    def _write_vasp(self, atoms, output_path, constraints=None):
        """Write structure to VASP format file"""
        # Check if structure is empty
        if len(atoms) == 0:
            raise ValueError("Empty structure, cannot write VASP file")
            
        # Get lattice parameters
        cell = atoms.get_cell()
        if cell is None or len(cell) == 0:
            raise ValueError("Empty lattice parameters, cannot write VASP file")
            
        # Get atomic positions
        positions = atoms.get_positions()
        if positions is None or len(positions) == 0:
            raise ValueError("Empty atomic positions, cannot write VASP file")
            
        # Get element information
        symbols = atoms.get_chemical_symbols()
        if not symbols:
            raise ValueError("Empty element information, cannot write VASP file")
            
        # Get element sorting parameters
        sort_order = getattr(self, 'sort_order', 'ascending')
        element_order = getattr(self, 'element_order', None)
        
        # Create element to periodic table position mapping
        element_positions = {}
        for symbol in symbols:
            if symbol not in element_positions:
                if element_order and symbol in element_order:
                    element_positions[symbol] = element_order.index(symbol)
                else:
                    element_positions[symbol] = self._get_element_position(symbol)
        
        # Sort elements based on sorting type
        reverse = sort_order == "descending"
        sorted_elements = sorted(set(symbols), key=lambda x: element_positions[x], reverse=reverse)
        
        # Reorder atoms
        new_indices = []
        for element in sorted_elements:
            new_indices.extend([i for i, s in enumerate(symbols) if s == element])
        
        # Reorder atoms
        atoms = atoms[new_indices]
        
        # Get constraint information
        fixed_atoms = []
        if constraints:
            if "fixed_atoms" in constraints:
                fixed_atoms.extend(constraints["fixed_atoms"])
            if "fixed_elements" in constraints:
                for element in constraints["fixed_elements"]:
                    fixed_atoms.extend([i for i, s in enumerate(symbols) if s == element])
            if "fixed_layers" in constraints:
                layer_thickness = constraints.get("layer_thickness", 1.0)
                z_coords = positions[:, 2]
                min_z, max_z = z_coords.min(), z_coords.max()
                num_layers = int((max_z - min_z) / layer_thickness) + 1
                
                for layer in constraints["fixed_layers"]:
                    if 0 <= layer < num_layers:
                        layer_min = min_z + layer * layer_thickness
                        layer_max = layer_min + layer_thickness
                        layer_atoms = [i for i, z in enumerate(z_coords) 
                                     if layer_min <= z < layer_max]
                        fixed_atoms.extend(layer_atoms)
        
        # Write VASP format file
        with open(output_path, 'w') as f:
            # Write comment line
            f.write("Converted by Atomorph\n")
            
            # Write scale factor
            f.write("1.0\n")
            
            # Write lattice parameters
            for row in cell:
                f.write(f"{row[0]:.6f} {row[1]:.6f} {row[2]:.6f}\n")
            
            # Write element symbols
            unique_symbols = []
            symbol_counts = []
            for symbol in sorted_elements:
                if symbol not in unique_symbols:
                    unique_symbols.append(symbol)
                    symbol_counts.append(symbols.count(symbol))
            
            f.write(" ".join(unique_symbols) + "\n")
            f.write(" ".join(map(str, symbol_counts)) + "\n")
            
            # Add Selective dynamics marker if there are fixed atoms
            if fixed_atoms:
                f.write("Selective dynamics\n")
            
            # Write coordinate type
            f.write("Cartesian\n")
            
            # Write atomic coordinates
            for i, (symbol, pos) in enumerate(zip(atoms.get_chemical_symbols(), atoms.get_positions())):
                # Determine if atom is fixed
                is_fixed = i in fixed_atoms
                # Write coordinates and fixed marker
                f.write(f"{pos[0]:.6f} {pos[1]:.6f} {pos[2]:.6f} "
                       f"{'F F F' if is_fixed else 'T T T'} {symbol}\n")
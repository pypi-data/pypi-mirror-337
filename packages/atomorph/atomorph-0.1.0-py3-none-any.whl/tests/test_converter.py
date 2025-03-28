"""
Test cases for the StructureConverter class.
"""
import os
import pytest
import numpy as np
from ase.io import read, write
from atomorph.converter import StructureConverter

@pytest.fixture
def converter():
    return StructureConverter()

@pytest.fixture
def test_dir():
    return os.path.join(os.path.dirname(__file__), "test_data")

def test_basic_conversion(converter, test_dir):
    """Test basic file format conversion."""
    input_file = os.path.join(test_dir, "Pd.cif")
    output_file = os.path.join(test_dir, "output.vasp")
    
    # Convert CIF to VASP
    converter.convert(input_file, output_file, input_format="cif", output_format="vasp")
    
    # Verify output file exists
    assert os.path.exists(output_file)
    
    # Read back and verify structure
    atoms = read(output_file)
    assert len(atoms) == 1  # Pd structure has 1 atom
    assert atoms.get_chemical_symbols()[0] == "Pd"

def test_element_mapping(converter, test_dir):
    """Test element mapping functionality."""
    input_file = os.path.join(test_dir, "Pd.cif")
    output_file = os.path.join(test_dir, "output_mapped.vasp")
    element_mapping = {"Pd": "Au"}
    
    converter.convert(
        input_file, 
        output_file, 
        input_format="cif", 
        output_format="vasp",
        element_mapping=element_mapping
    )
    
    atoms = read(output_file)
    assert atoms.get_chemical_symbols()[0] == "Au"

def test_atomic_constraints(converter, test_dir):
    """Test atomic constraints functionality."""
    input_file = os.path.join(test_dir, "Au111.cif")
    output_file = os.path.join(test_dir, "output_constrained.vasp")
    constraints = {
        "fixed_layers": [0],
        "layer_thickness": 2.0,
        "selective_dynamics": True
    }
    
    converter.convert(
        input_file,
        output_file,
        input_format="cif",
        output_format="vasp",
        constraints=constraints
    )
    
    # Read VASP file and verify constraints
    with open(output_file, 'r') as f:
        lines = f.readlines()
        # Skip header lines
        for line in lines[8:]:  # VASP format specific
            if line.strip():
                parts = line.split()
                if len(parts) >= 7:  # Check if line contains constraints
                    constraints = parts[3:6]
                    if float(parts[2]) < 2.0:  # First layer
                        assert all(c == 'F' for c in constraints)
                    else:
                        assert all(c == 'T' for c in constraints)

def test_multi_frame_conversion(converter, test_dir):
    """Test multi-frame structure conversion."""
    input_file = os.path.join(test_dir, "train.xyz")
    output_dir = os.path.join(test_dir, "output_frames")
    
    converter.convert(
        input_file,
        output_dir,
        input_format="xyz",
        output_format="vasp",
        mode="multi"
    )
    
    # Verify output files
    assert os.path.exists(os.path.join(output_dir, "frame_0.vasp"))
    assert os.path.exists(os.path.join(output_dir, "frame_1.vasp"))

def test_error_handling(converter, test_dir):
    """Test error handling for invalid inputs."""
    # Test non-existent file
    with pytest.raises(FileNotFoundError):
        converter.convert(
            "nonexistent.cif",
            "output.vasp",
            input_format="cif",
            output_format="vasp"
        )
    
    # Test invalid format
    input_file = os.path.join(test_dir, "Pd.cif")
    with pytest.raises(ValueError):
        converter.convert(
            input_file,
            "output.unknown",
            input_format="cif",
            output_format="unknown"
        ) 
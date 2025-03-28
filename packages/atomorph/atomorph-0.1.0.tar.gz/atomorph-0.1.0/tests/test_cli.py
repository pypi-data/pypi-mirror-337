"""
Test cases for the command line interface.
"""
import os
import pytest
from atomorph.cli import main

@pytest.fixture
def test_dir():
    return os.path.join(os.path.dirname(__file__), "test_data")

def test_basic_conversion_cli(test_dir):
    """Test basic conversion using CLI."""
    input_file = os.path.join(test_dir, "Pd.cif")
    output_file = os.path.join(test_dir, "output_cli.vasp")
    
    # Test basic conversion
    main([input_file, output_file, "-i", "cif", "-o", "vasp"])
    assert os.path.exists(output_file)

def test_element_mapping_cli(test_dir):
    """Test element mapping using CLI."""
    input_file = os.path.join(test_dir, "Pd.cif")
    output_file = os.path.join(test_dir, "output_mapped_cli.vasp")
    mapping_file = os.path.join(test_dir, "element_mapping.json")
    
    # Test element mapping
    main([
        input_file,
        output_file,
        "-i", "cif",
        "-o", "vasp",
        "-e", mapping_file
    ])
    assert os.path.exists(output_file)

def test_constraints_cli(test_dir):
    """Test atomic constraints using CLI."""
    input_file = os.path.join(test_dir, "Au111.cif")
    output_file = os.path.join(test_dir, "output_constrained_cli.vasp")
    constraints_file = os.path.join(test_dir, "constraints.json")
    
    # Test constraints
    main([
        input_file,
        output_file,
        "-i", "cif",
        "-o", "vasp",
        "-c", constraints_file
    ])
    assert os.path.exists(output_file)

def test_multi_frame_cli(test_dir):
    """Test multi-frame conversion using CLI."""
    input_file = os.path.join(test_dir, "train.xyz")
    output_dir = os.path.join(test_dir, "output_frames_cli")
    
    # Test multi-frame conversion
    main([
        input_file,
        output_dir,
        "-i", "xyz",
        "-o", "vasp",
        "-m", "multi"
    ])
    assert os.path.exists(os.path.join(output_dir, "frame_0.vasp"))

def test_error_handling_cli(test_dir):
    """Test error handling in CLI."""
    # Test non-existent file
    with pytest.raises(SystemExit):
        main(["nonexistent.cif", "output.vasp"])
    
    # Test invalid format
    input_file = os.path.join(test_dir, "Pd.cif")
    with pytest.raises(SystemExit):
        main([input_file, "output.unknown", "-i", "cif", "-o", "unknown"]) 
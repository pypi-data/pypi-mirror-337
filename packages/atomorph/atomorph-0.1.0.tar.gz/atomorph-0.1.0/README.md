# Atomorph

A Python package for atomic structure file format conversion.

## Features

- Support for multiple atomic structure file formats:
  - VASP (POSCAR/CONTCAR)
  - XYZ/EXTXYZ
  - CIF
  - LAMMPS data
- Multi-frame structure support
- Element mapping
- Atomic constraints
- Custom conversion strategies

## Installation

```bash
pip install atomorph
```

## Usage

### Command Line Interface

Basic usage:
```bash
conv input_file output_file [options]
```

Options:
- `-i, --input-format`: Input file format
- `-o, --output-format`: Output file format
- `-m, --mode`: Conversion mode (single/multi)
- `-f, --frame`: Select specific frame
- `-e, --element-mapping`: Element mapping configuration file
- `-c, --constraints`: Atomic constraints configuration file

Examples:
```bash
# Basic conversion
conv input.cif output.vasp -i cif -o vasp

# Multi-frame conversion
conv input.xyz output_dir -i xyz -o vasp -m multi

# Select specific frame
conv input.xyz output.vasp -i xyz -o vasp -f 1

# Use element mapping
conv input.xyz output.vasp -i xyz -o vasp -e mapping.json

# Apply atomic constraints
conv input.xyz output.vasp -i xyz -o vasp -c constraints.json
```

### Python API

```python
from atomorph.converter import StructureConverter

# Create converter instance
converter = StructureConverter()

# Basic conversion
converter.convert(
    "input.cif",
    "output.vasp",
    input_format="cif",
    output_format="vasp"
)

# Multi-frame conversion
converter.convert(
    "input.xyz",
    "output_dir",
    input_format="xyz",
    output_format="vasp",
    mode="multi"
)

# Use element mapping
element_mapping = {"Pd": "Au"}
converter.convert(
    "input.xyz",
    "output.vasp",
    input_format="xyz",
    output_format="vasp",
    element_mapping=element_mapping
)

# Apply atomic constraints
constraints = {
    "fixed_atoms": [0, 1, 2],
    "selective_dynamics": True
}
converter.convert(
    "input.xyz",
    "output.vasp",
    input_format="xyz",
    output_format="vasp",
    constraints=constraints
)
```

## Configuration Files

### Element Mapping

JSON format:
```json
{
    "Pd": "Au",
    "Pt": "Ir"
}
```

### Atomic Constraints

JSON format:
```json
{
    // Fix by atom indices
    "fixed_atoms": [0, 1, 2],
    
    // Fix by element symbols
    "fixed_elements": ["Pd", "Au"],
    
    // Fix by z-coordinate layers
    "fixed_layers": [0, 1],
    "layer_thickness": 1.0,
    
    // Enable selective dynamics in VASP output
    "selective_dynamics": true
}
```

You can use any combination of these constraint types. The constraints will be applied to all atoms that match any of the specified conditions.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
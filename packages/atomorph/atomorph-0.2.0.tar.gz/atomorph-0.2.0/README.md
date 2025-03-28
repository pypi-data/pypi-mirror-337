# Atomorph

Atomorph is a powerful atomic structure file format converter with advanced sorting and constraint capabilities.

## Features

- **Format Conversion**: Convert between various atomic structure file formats (CIF, VASP, XYZ, etc.)
- **Element Sorting**: Sort elements by atomic number (ascending/descending) or custom order
- **Atomic Constraints**: Support for fixed atoms, fixed elements, and fixed layers
- **Multi-frame Support**: Handle both single and multi-frame structure files
- **Parallel Processing**: Efficient processing of large multi-frame files
- **Progress Display**: Real-time progress tracking for large file conversions

## Installation

```bash
pip install atomorph
```

## Quick Start

After installation, you can use the `conv` command-line tool:

```bash
# Basic conversion
conv input.cif output.vasp

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
```

## Configuration Files

### Constraints Configuration (constraints.json)

When using atomic constraints, you need to provide a JSON configuration file with the following format:

```json
{
    "fixed_atoms": [0, 2],           // Fix specific atoms (0-based index)
    "fixed_elements": ["Fe", "Cu"],  // Fix all atoms of specified elements
    "fixed_layers": [0],             // Fix atoms in specified layers (counted from bottom)
    "layer_thickness": 1.0           // Layer thickness in Angstroms
}
```

### Element Order Configuration (element_order.json)

When specifying a custom element order, you can also use a JSON file:

```json
{
    "elements": ["Au", "Pt", "Ag", "Cu", "Fe"]
}
```

## Command Line Options

- `input_path`: Input file path (required)
- `output_path`: Output file path (required)
- `-i, --input-format`: Input file format (default: cif)
- `-o, --output-format`: Output file format (default: vasp)
- `-m, --mode`: Conversion mode (single/multi, default: single)
- `-f, --frame`: Select specific frame for multi-frame files
- `-s, --sort`: Sort elements by atomic number (ascending/descending)
- `-e, --elements`: Specify element order (e.g., -e Au Pt Ag Cu Fe)
- `-c, --constraints`: Path to constraints configuration file (JSON format)
- `-p, --parallel`: Enable parallel processing for multi-frame files

## Python API Usage

```python
from atomorph.converter import StructureConverter

# Initialize converter
converter = StructureConverter()

# Basic conversion
converter.convert(
    input_path="input.cif",
    output_path="output.vasp",
    input_format="cif",
    output_format="vasp"
)

# Conversion with sorting
converter.convert(
    input_path="input.cif",
    output_path="output.vasp",
    sort_order="descending"  # or "ascending"
)

# Conversion with custom element order
converter.convert(
    input_path="input.cif",
    output_path="output.vasp",
    element_order=["Au", "Pt", "Ag", "Cu", "Fe"]
)

# Conversion with constraints
converter.convert(
    input_path="input.cif",
    output_path="output.vasp",
    constraints={
        "fixed_atoms": [0, 2, 4],
        "fixed_elements": ["Fe", "Cu"],
        "fixed_layers": [0, 2],
        "layer_thickness": 1.0
    }
)

# Multi-frame conversion with parallel processing
converter.convert(
    input_path="input.cif",
    output_path="output/",
    parallel=True
)
```

## Supported File Formats

- VASP (POSCAR/CONTCAR)
- CIF
- XYZ/EXTXYZ
- And more formats supported by ASE

## Advanced Features

### Element Sorting

The converter supports three sorting modes:
- `ascending`: Sort elements by atomic number in ascending order
- `descending`: Sort elements by atomic number in descending order
- Custom order: Specify your own element order via command line or JSON file

### Atomic Constraints

Three types of constraints are supported:
1. **Fixed Atoms**: Fix specific atoms by their indices (0-based)
2. **Fixed Elements**: Fix all atoms of specified elements
3. **Fixed Layers**: Fix atoms in specified layers along the z-axis

### Multi-frame Processing

- Automatically detects single/multi-frame files
- Supports parallel processing for multi-frame files
- Shows progress bar for large file conversions

### File Size Handling

- Checks file size before processing
- Default limit: 100MB (configurable)
- Memory-efficient processing

## Error Handling

The converter provides clear error messages for common issues:
- Invalid file formats
- Empty structures
- File size limits
- Invalid constraints
- Parsing errors
- Invalid JSON configuration files

## Performance Optimization

- Parallel processing for multi-frame files
- Progress tracking for large files
- Memory usage optimization
- File size checks

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes in each release.
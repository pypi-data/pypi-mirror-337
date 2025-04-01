# NanoGO Basecaller

<table align="center" style="margin: 0px auto;">
  <tr>
    <td>
      <img src="https://raw.githubusercontent.com/phac-nml/nanogo/main/extra/nanogo_logo.svg" alt="NanoGo Logo" width="400" height="auto"/>
    </td>
    <td>
      <h1>NanoGO Basecaller</h1>
<p align="center" style="margin: 0px auto;">
  <img src="https://img.shields.io/badge/build-passing-brightgreen?style=for-the-badge&logo=gitlab&logoColor=white&logoWidth=40&color=green" alt="Pipeline Status">
  <img src="https://img.shields.io/badge/coverage-58.6%25-brightgreen?style=for-the-badge&logo=codecov&logoColor=white&logoWidth=40&color=green" alt="Coverage">
  <img src="https://img.shields.io/badge/python-_3.8+-blue?style=for-the-badge&logo=python&logoColor=white&logoWidth=40&color=blue" alt="Python Versions">
  <img src="https://img.shields.io/pypi/dm/nanogo-basecaller?style=for-the-badge&logo=pypi&logoColor=white&logoWidth=30&color=orange" alt="PyPI Downloads">
  <img src="https://img.shields.io/badge/license-GNU%20GPL%20v3-blue?style=for-the-badge&logo=gnu&logoColor=white&logoWidth=40&color=blue" alt="License">
</p>
    </td>
  </tr>
</table>

## Table of Contents
- [NanoGO Basecaller](#nanogo-basecaller)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Features](#features)
  - [Installation](#installation)
    - [Requirements](#requirements)
    - [Quick Installation](#quick-installation)
    - [Step-by-Step Installation](#step-by-step-installation)
    - [Installing from Source](#installing-from-source)
    - [Dependencies](#dependencies)
  - [System Requirements](#system-requirements)
  - [Usage](#usage)
    - [Verifying Installation](#verifying-installation)
    - [Interactive Mode](#interactive-mode)
    - [Command-Line Mode](#command-line-mode)
  - [Workflow](#workflow)
  - [Command-Line Options](#command-line-options)
    - [Main Options](#main-options)
    - [Basecalling Options](#basecalling-options)
    - [Device Options](#device-options)
    - [Advanced Options](#advanced-options)
  - [Input Directory Structure](#input-directory-structure)
  - [Output Structure](#output-structure)
    - [temp\_data Directory](#temp_data-directory)
    - [final\_output Directory](#final_output-directory)
  - [File Naming Convention](#file-naming-convention)
  - [Troubleshooting](#troubleshooting)
    - [Common Issues and Solutions](#common-issues-and-solutions)
      - [Installation Issues](#installation-issues)
      - [Runtime Issues](#runtime-issues)
    - [Logging and Debugging](#logging-and-debugging)
  - [License](#license)
  - [Support and Contact](#support-and-contact)

## Overview

NanoGO Basecaller is a specialized component of the NanoGO bioinformatics pipeline, designed for Oxford Nanopore Technologies (ONT) sequencing data processing. The tool provides an intuitive interface to Dorado, Oxford Nanopore's high-performance basecaller, supporting both standard and duplex sequencing modes. NanoGO Basecaller handles the entire process from raw signal data (FAST5/POD5) conversion to demultiplexed nucleotide sequences, with optimized parallel processing and GPU acceleration.

The tool is developed by the National Microbiology Laboratory at the Public Health Agency of Canada to streamline nanopore data processing workflows, making advanced basecalling accessible to researchers without requiring extensive computational expertise.

## Features

- **Dorado Integration**: Seamless integration with the latest Dorado basecaller (automatically uses or downloads the latest version)
- **Multiple Basecalling Modes**:
  - Standard basecalling for routine sequencing data
  - Duplex basecalling for highest accuracy applications
- **Format Conversion**: Automatic FAST5 to POD5 format conversion
- **Model Management**:
  - Interactive model selection with recommendations
  - Automatic model downloading and versioning
  - Support for both DNA and RNA models
- **Demultiplexing**:
  - Built-in support for ONT barcoding kits
  - Automatic sample sheet generation
  - Organized output by barcode
- **Performance Optimization**:
  - Parallel processing with auto-detection of system resources
  - GPU acceleration with CUDA support
  - Multi-GPU processing capability
- **User Interface**:
  - Interactive configuration mode with guided setup
  - Command-line interface for scripting and automation
  - Real-time progress monitoring
- **Robust Error Handling**:
  - Comprehensive version checking
  - Graceful recovery from processing failures

## Installation

### Requirements

- Python 3.8 to 3.10 (3.11+ not currently supported)
- Conda or Miniconda (recommended for dependency management)
- NVIDIA GPU with CUDA support (recommended but not required)
- Linux or Windows Subsystem for Linux (WSL)

### Quick Installation

```bash
conda create -n nanogo-basecaller "python=3.10" -y && conda activate nanogo-basecaller && pip install nanogo-basecaller
```

### Step-by-Step Installation

1. Create a conda environment:
```bash
conda create -n nanogo-basecaller "python=3.10"
```

2. Activate the environment:
```bash
conda activate nanogo-basecaller
```

3. Install the package:
```bash
pip install nanogo-basecaller
```

### Installing from Source

1. Clone the repository:
```bash
git clone https://github.com/phac-nml/nanogo-basecaller.git
```

2. Navigate to the project directory:
```bash
cd nanogo-basecaller
```

3. Install in development mode:
```bash
pip install -e .
```

### Dependencies

The following dependencies will be automatically installed:

- **Core Dependencies**:
  - pip
  - bio
  - GPUtil
  - alive-progress
  - psutil
  - setuptools
  - typing-extensions
  - wheel
  - build
  - poetry-core
  - pyabpoa
  - pod5==0.3.10

- **External Tools**:
  - Dorado (v0.6.0+) - automatically downloaded during installation
  - Pod5 (v0.3.0+) - comes with the package

## System Requirements

- **CPU**: 4+ cores recommended (automatically scales to available resources)
- **RAM**: Minimum 16GB, 32GB+ recommended for larger datasets
- **Storage**: SSD recommended for faster I/O operations
- **GPU**: NVIDIA GPU with CUDA support recommended for optimal performance:
  - RTX series or Tesla series for best performance
  - Multiple GPUs supported for parallel processing
- **Operating System**:
  - Linux (Ubuntu 18.04+, CentOS 7+)
  - Windows 10/11 with WSL2

## Usage

### Verifying Installation

Test that NanoGO Basecaller is properly installed:

```bash
nanogo --help
```

This should display the help information:

```
usage: nanogo [options] <subcommand>

options:
  -h, --help            show this help message and exit
  -v, --version         Display the version number of NanoGO.

Available Tools:
  Valid subcommands

  {basecaller}
                        Description
    basecaller          Run nanogo basecaller using dorado basecaller
```

### Interactive Mode

For guided execution with interactive prompts:

```bash
nanogo basecaller
```

The tool will walk you through selecting:
- Input directory containing FAST5/POD5 files
- Output directory for results
- Basecalling model selection
- Barcoding kit selection
- Processing parameters

### Command-Line Mode

For direct execution or scripting:

```bash
nanogo basecaller -i <raw_ont-data_folder> -o <output_directory_name> [options]
```

## Workflow

NanoGO Basecaller follows this processing workflow:

1. **Version Checking**: Verifies that required tools (Dorado, Pod5) are installed and meet version requirements
2. **Input Processing**: Scans for FAST5/POD5 files in the specified directories
3. **Configuration**:
   - Selects appropriate basecalling model
   - Creates demultiplexing sample sheet
   - Configures parallel processing based on system resources
4. **Preparation**:
   - Converts FAST5 files to POD5 format if needed
   - Downloads required basecalling models
   - Distributes files across processing chunks
5. **Basecalling**:
   - Executes Dorado basecaller (standard or duplex mode)
   - Generates BAM files with basecalled sequences
6. **Demultiplexing**:
   - Separates sequences by barcode
   - Organizes into barcode-specific directories
7. **Output Processing**:
   - Renames files with standardized naming convention
   - Organizes final output structure

## Command-Line Options

### Main Options

```bash
nanogo basecaller [-i <input_dir>] [-o <output_dir>] [-b] [-d] [--device {auto,cpu,gpu}]
```

- `-i <raw_ont-data_folder>`: Path to folder containing ONT raw data
- `-o <output_directory_name>`: Output directory name (default: "dorado_output")

### Basecalling Options

- `-b`, `--basecaller`: Enable to specify and use a particular basecalling software (enabled by default)
- `-d`, `--duplex`: Enable duplex sequencing mode for processing both DNA strands
- `-m`, `--model <model_name>`: Specify a particular Dorado model
- `--ignore <ignore_pattern>`: Ignore files matching the provided pattern (can be specified multiple times)

### Device Options

- `--device {auto,cpu,gpu}`: Specify computing device (default: auto)
- `--gpu-device <device_id>`: Specify GPU device ID to use (default: 0)

### Advanced Options

- `--check-version`: Check for the latest Dorado version before running (default: enabled)
- `--threads <num_threads>`: Number of threads to use (default: auto)
- `--chunk-size <chunk_size>`: Chunk size for processing (default: determined by Dorado)
- `--modified-bases`: Enable modified base detection (requires compatible model)

## Input Directory Structure

NanoGO Basecaller expects an input directory containing one or more subdirectories, each representing a separate sequencing run:

```
Input Directory
├─ Raw_Sample_A
│  ├─ Raw_Sample_A_01.pod5 (POD5 or FAST5)
│  ├─ Raw_Sample_A_02.pod5 (POD5 or FAST5)
├─ Raw_Sample_B
│  ├─ Raw_Sample_B_01.fast5 (POD5 or FAST5)
│  ├─ Raw_Sample_B_02.fast5 (POD5 or FAST5)
│  ├─ Raw_Sample_B_03.fast5 (POD5 or FAST5)
└─ Raw_Sample_N
   └─ Raw_Sample_N_01.pod5 (POD5 or FAST5)
```

**Important Notes**:
- Each subdirectory is treated as a separate sequencing run
- Files can be in FAST5 or POD5 format
  - FAST5 files are automatically converted to POD5 during processing
- File naming is flexible - the tool extracts relevant identifiers automatically
- Input directories can be nested arbitrarily deep

## Output Structure

NanoGO Basecaller generates a structured output directory with the following components:

### temp_data Directory

Contains intermediate files created during processing:

- **basecalling model/**: Downloaded machine learning models
- **sublist_# folders/**: Processing chunks with:
  - Non-demultiplexed BAM files
  - Symbolic links to input POD5/FAST5 files
  - **demux/**: Demultiplexed data organized by barcode
- **sample sheet**: Configuration file for demultiplexing

### final_output Directory

Contains the final processed files:

- **barcode## folders/**: Demultiplexed data organized by barcode
  - Contains FASTQ files for each barcode
- **unclassified/**: Sequences with unidentified barcodes
  - Contains FASTQ files without clear barcode assignment

## File Naming Convention

Output files follow this standardized naming convention:

```
{flow_cell_id}_{run_id}_{dorado_models_hex}_{dorado_kits_hex}_[file_count].fastq
```

Components:
1. **Flow Cell ID**: Identifier from the sequencing data
2. **Run ID**: First 8 characters of the unique run identifier
3. **Dorado Models Hash**: First 8 characters of SHA-256 hash of the models
4. **Dorado Kits Hash**: First 8 characters of SHA-256 hash of the kits
5. **File Count**: Sequential counter for multiple files

This naming convention ensures:
- **Uniqueness**: Files are distinctly identifiable
- **Traceability**: Processing parameters are encoded in the filename
- **Compatibility**: Works across computing environments
- **Sorting**: Files sort logically by group and sequence

## Troubleshooting

### Common Issues and Solutions

#### Installation Issues

**Problem**: Error during installation related to missing compilers  
**Solution**: Install required compilers: `conda install -c conda-forge gcc_linux-64 gxx_linux-64`

**Problem**: Unable to find Dorado during runtime  
**Solution**: NanoGO will attempt to download Dorado automatically. If this fails, ensure internet connectivity or manually install Dorado and provide its path when prompted.

#### Runtime Issues

**Problem**: "No CUDA-capable device is detected"  
**Solution**: Set `--device cpu` to run without GPU or ensure NVIDIA drivers are properly installed.

**Problem**: Memory errors during basecalling  
**Solution**: Reduce chunk size by increasing the number of chunks when prompted during interactive mode.

**Problem**: Tool fails to find input files  
**Solution**: Ensure input files are in the expected format (FAST5 or POD5) and the directory structure follows the expected pattern.

### Logging and Debugging

For troubleshooting, examine the console output for error messages. The tool provides status updates, warnings, and error messages during execution.

## License

NanoGO Basecaller is licensed under the GNU General Public License, Version 3.0. For details, see [GNU General Public License, Version 3.0](https://www.gnu.org/licenses/gpl-3.0).

## Support and Contact

For questions, issues, or assistance:

- **Contact**: [Gurasis Osahan](mailto:gurasis.osahan@phac-aspc.gc.ca) at the National Microbiology Laboratory
- **Issues**: Submit issues through the GitHub repository
- **Documentation**: Refer to the docs directory for additional documentation

**Copyright**: Government of Canada  
**Written by**: National Microbiology Laboratory, Public Health Agency of Canada

---

*Ensuring public health through advanced genomics. Developed with unwavering commitment and expertise by National Microbiology Laboratory, Public Health Agency of Canada.*
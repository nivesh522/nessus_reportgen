# nessus-reportgen

Enterprise-grade Nessus vulnerability scan report generator that converts Nessus CSV and .nessus XML exports into professional Excel and Word reports.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Table of Contents
- [Features](#features)
- [Quick Start](#quick-start)
- [User Guide](#user-guide)
- [Installation](#installation)
- [Usage](#usage)
- [Developer Guide](#developer-guide)
- [Cross-Platform Building](#cross-platform-building--packaging)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Features

- **Unified Parsing Layer**: Supports both Nessus CSV exports and native .nessus XML files
- **Canonical Finding Model**: Uses Pydantic for type-safe data validation
- **Smart Deduplication**: Aggregates findings by (plugin_id, synopsis) to avoid duplicates
- **Professional Excel Reports**:
  - Executive Summary
  - Host Summary
  - Detailed Findings
  - Severity-specific sheets (Critical, High, Medium, Low, Info)
- **Professional Word Reports**:
  - Executive Summary
  - Host Summary
  - Detailed Findings (tables with custom styling, severity-specific colors, blue header, bold labels)
  - Styled with exact hex colors for severity highlighting
  - Exact column widths and text wrapping from template
- **Theming for Excel**: Supports Corporate Minimal and Dark themes
- **CLI Application**: Built with Typer for a clean command-line interface
- **Enterprise-Grade Logging**: Uses loguru for structured logging
- **Robust Error Handling**: Validates inputs and provides meaningful error messages
- **Cross-Platform Support**: Buildable for Windows, macOS, and Linux

## Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd nessus-reportgen

# Install with Poetry
poetry install

# Generate your first report
poetry run nessus-reportgen generate scan.csv report.xlsx
```

## User Guide

### Supported Input Formats

nessus-reportgen supports two input formats:
1. **Nessus CSV Exports**: Standard CSV files exported from Nessus
2. **.nessus XML Files**: Native Nessus XML scan outputs

### Generating Reports

#### Basic Usage

```bash
# Convert a single CSV file to Excel
nessus-reportgen generate scan.csv report.xlsx

# Convert a single CSV file to Word
nessus-reportgen generate scan.csv report.docx

# Convert a single .nessus XML file to Excel
nessus-reportgen generate scan.nessus report.xlsx

# Convert a single .nessus XML file to Word
nessus-reportgen generate scan.nessus report.docx

# Process all files in a directory (merged report)
nessus-reportgen generate scans/ merged-report.xlsx
nessus-reportgen generate scans/ merged-report.docx
```

#### Advanced Options

```bash
# Excel report with dark theme
nessus-reportgen generate scan.csv report.xlsx --theme dark

# Word report with custom template
nessus-reportgen generate scan.csv report.docx --template "Sample Network VAPT Report.docx"

# Filter by minimum severity
nessus-reportgen generate scan.csv report.xlsx --min-severity medium

# Enable verbose logging
nessus-reportgen generate scan.csv report.xlsx --verbose

# Log to a file
nessus-reportgen generate scan.csv report.xlsx --log-file reportgen.log
```

#### CLI Reference

```
nessus-reportgen generate [OPTIONS] INPUT_PATH OUTPUT_PATH

Options:
  -f, --format TEXT        Output format (auto/excel/word) [default: auto]
  -t, --theme TEXT         Report theme for Excel (corporate/dark) [default: corporate]
  --template TEXT          Word template file (.docx)
  --min-severity TEXT      Minimum severity to include (info/low/medium/high/critical) [default: info]
  -v, --verbose            Enable verbose logging
  --log-file TEXT          Log file path
  --version                Show version and exit
  --help                   Show this message and exit
```

### Word Report Styling

The Word report generator uses the following color scheme:

| Element               | Hex Color   |
|-----------------------|-------------|
| Header Fill           | #73A0DD     |
| Critical Severity     | #C0504D     |
| High Severity         | #F79646     |
| Medium Severity       | #F0F04E     |
| Low Severity          | #9BBB59     |
| Informational         | #4BACC6     |

## Installation

### Prerequisites
- Python 3.10 or later
- pip or Poetry

### From PyPI (coming soon)

```bash
pip install nessus-reportgen
```

### From Source (Using pip)

```bash
git clone <repository-url>
cd nessus-reportgen
pip install -e .
```

### From Source (Using Poetry) - Recommended

```bash
git clone <repository-url>
cd nessus-reportgen
poetry install
```

## Developer Guide

### Development Setup

```bash
# Clone repository
git clone <repository-url>
cd nessus-reportgen

# Install development dependencies
poetry install --with dev

# Verify installation
poetry run nessus-reportgen --version
```

### Project Layout

```
nessus-reportgen/
├── pyproject.toml          # Project metadata and dependencies
├── README.md               # This file
├── LICENSE
├── Makefile                # Development and build commands
├── poetry.lock             # Poetry lock file (committed for reproducibility)
├── nessus-reportgen.spec   # PyInstaller spec file
│
├── src/reportgen/
│   ├── cli.py                 # CLI application
│   ├── __init__.py
│   │
│   ├── parsers/
│   │   ├── base.py            # Base parser interface
│   │   ├── csv_parser.py      # CSV parser implementation
│   │   └── nessus_parser.py   # Nessus XML parser
│   │
│   ├── models/
│   │   └── finding.py         # Pydantic Finding model
│   │
│   ├── processors/
│   │   └── aggregator.py      # Deduplication and aggregation
│   │
│   ├── report/
│   │   ├── excel_writer.py    # Excel report generation
│   │   ├── doc_writer.py      # Word report generation
│   │   └── themes.py          # Theme definitions
│   │
│   └── utils/
│       ├── logging.py          # Logging setup
│       └── validators.py       # Input validators
│
└── tests/
    └── test_aggregator.py
```

### Linting and Formatting

```bash
# Check linting
make lint

# Auto-format code
make format
```

### Testing

```bash
# Run all tests
make test

# Run tests with coverage
make test-cov
```

### Cleanup

```bash
make clean
```

## Cross-Platform Building & Packaging

### Prerequisites
All platforms require Python 3.10 or later.

### Build Python Package (All Platforms)
This builds a source distribution and a wheel:
```bash
make build
# or manually:
poetry run python -m build
```

### Build Standalone Executable

#### Linux / macOS
```bash
make build-exe
# or with the spec file:
make build-exe-spec
```
This creates a single-file executable in `dist/`.

#### Windows (PowerShell or Command Prompt)
```powershell
# Using PowerShell
poetry run pyinstaller --clean --onefile --name nessus-reportgen src\reportgen\cli.py

# Or with the spec file:
poetry run pyinstaller --clean nessus-reportgen.spec
```
This creates `nessus-reportgen.exe` in `dist\`.

### Cross-Compiling Executables
To build Windows executables on Linux/macOS, use **Wine** + **PyInstaller** (advanced).

## Troubleshooting

### Poetry Installation Issues
If you encounter dependency resolution errors, try:
```bash
poetry lock --no-update
poetry install
```

### PyInstaller Build Errors
Ensure you're using Python <3.15 and have all dependencies installed:
```bash
poetry install --with dev
```

## License

MIT

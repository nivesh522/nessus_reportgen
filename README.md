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

### From Pre-Built Binaries (Recommended for End Users)

Download the appropriate binary for your platform and architecture from the [GitHub Releases](https://github.com/[your-username]/nessus-reportgen/releases) page:

#### Check Your System Architecture
First, determine your system architecture:
- **Linux/macOS**: Run `uname -m` in terminal
  - `x86_64` or `amd64` → Use `x64` binary
  - `aarch64` or `arm64` → Use `arm64` binary
- **Windows**: Open System Information → Look for "System Type"

#### Windows
1. Download `nessus-reportgen-windows-x64.exe`
2. You can rename it to `nessus-reportgen.exe` for convenience
3. Open Command Prompt or PowerShell and navigate to the download directory
4. Run the executable directly:
   ```powershell
   # Show help
   .\nessus-reportgen.exe --help
   
   # Generate a report
   .\nessus-reportgen.exe generate scan.csv report.xlsx
   ```

#### Linux
1. Download the appropriate binary:
   - For x86-64 (most PCs): `nessus-reportgen-linux-x64`
   - For ARM64 (Raspberry Pi, AWS Graviton, etc.): `nessus-reportgen-linux-arm64`
2. Make it executable:
   ```bash
   chmod +x nessus-reportgen-linux-*
   ```
3. Optionally, move it to a directory in your PATH (like `/usr/local/bin`):
   ```bash
   sudo mv nessus-reportgen-linux-x64 /usr/local/bin/nessus-reportgen
   # or for ARM64
   sudo mv nessus-reportgen-linux-arm64 /usr/local/bin/nessus-reportgen
   ```
4. Run it:
   ```bash
   # Show help
   ./nessus-reportgen-linux-x64 --help
   # or for ARM64
   ./nessus-reportgen-linux-arm64 --help
   
   # Generate a report
   ./nessus-reportgen-linux-x64 generate scan.csv report.xlsx
   ```

#### macOS
1. Download the appropriate binary:
   - For Intel Macs: `nessus-reportgen-macos-x64`
   - For Apple Silicon (M1/M2/M3): `nessus-reportgen-macos-arm64`
2. Make it executable:
   ```bash
   chmod +x nessus-reportgen-macos-*
   ```
3. If you get a security warning, right-click and select "Open" (or go to System Settings > Privacy & Security)
4. Optionally, move it to a directory in your PATH:
   ```bash
   sudo mv nessus-reportgen-macos-x64 /usr/local/bin/nessus-reportgen
   # or for ARM64
   sudo mv nessus-reportgen-macos-arm64 /usr/local/bin/nessus-reportgen
   ```
5. Run it:
   ```bash
   # Show help
   ./nessus-reportgen-macos-x64 --help
   # or for ARM64
   ./nessus-reportgen-macos-arm64 --help
   
   # Generate a report
   ./nessus-reportgen-macos-x64 generate scan.csv report.xlsx
   ```

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

### Binary Issues

#### Linux: "GLIBC_2.XX not found"
This happens when the binary was built on a system with a newer GLIBC version than your system. The GitHub Release binaries are built on Ubuntu 22.04 (GLIBC 2.35), which should be compatible with most modern Linux distributions. If you still encounter issues, you can build the binary from source on your system.

#### macOS: Security Warning
macOS may block the binary because it's from an unidentified developer. To fix:
1. Right-click the binary and select "Open"
2. Or go to **System Settings > Privacy & Security** and click "Open Anyway"

#### Windows: SmartScreen Warning
Windows SmartScreen may block the executable. Click "More info" and then "Run anyway".

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

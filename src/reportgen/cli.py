import sys
from pathlib import Path
from enum import Enum

import typer
from loguru import logger

try:
    from . import __version__
    from .parsers import CSVParser, NessusXMLParser
    from .processors import aggregate_findings
    from .report import ExcelReportWriter, WordReportWriter, get_theme
    from .utils import setup_logger, validate_file_path
except ImportError:
    from reportgen import __version__
    from reportgen.parsers import CSVParser, NessusXMLParser
    from reportgen.processors import aggregate_findings
    from reportgen.report import ExcelReportWriter, WordReportWriter, get_theme
    from reportgen.utils import setup_logger, validate_file_path


class OutputFormat(str, Enum):
    AUTO = "auto"
    EXCEL = "excel"
    WORD = "word"


class ExcelTheme(str, Enum):
    CORPORATE = "corporate"
    DARK = "dark"


class Severity(str, Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


app = typer.Typer(
    name="nessus-reportgen",
    help="""Enterprise-grade Nessus vulnerability scan report generator.

Converts Nessus CSV exports (.csv) and native Nessus XML files (.nessus) into professional,
formatted Excel (.xlsx) and Word (.docx) reports.

Supports:
- Single file or batch directory processing
- Severity-based filtering
- Custom Word templates
- Multiple Excel themes

Example usage:
  nessus-reportgen generate scan.nessus report.xlsx
  nessus-reportgen generate scans/ report.docx --template custom-template.docx
  nessus-reportgen generate scan.csv report.xlsx --min-severity high
""",
    add_completion=True,
    rich_markup_mode="rich",
)


def version_callback(value: bool) -> None:
    if value:
        typer.echo(f"nessus-reportgen v{__version__}")
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool | None = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version information and exit",
    ),
) -> None:
    """Enterprise-grade Nessus vulnerability scan report generator."""
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())


@app.command(
    help="""Generate a professional report from Nessus scan results.

INPUT_PATH: Path to a single Nessus CSV/XML file or a directory containing multiple files.
OUTPUT_PATH: Path where the generated report will be saved (.xlsx or .docx).
"""
)
def generate(
    input_path: str = typer.Argument(
        ...,
        help="Input file or directory (supports .csv and .nessus files)",
        show_default=False,
    ),
    output_path: str = typer.Argument(
        ...,
        help="Output report file (.xlsx for Excel, .docx for Word)",
        show_default=False,
    ),
    format: OutputFormat = typer.Option(
        OutputFormat.AUTO,
        "--format",
        "-f",
        help="Force output format (auto-detects from file extension by default)",
        case_sensitive=False,
    ),
    theme: ExcelTheme = typer.Option(
        ExcelTheme.CORPORATE,
        "--theme",
        "-t",
        help="Visual theme for Excel reports (corporate or dark)",
        case_sensitive=False,
    ),
    template: str | None = typer.Option(
        None,
        "--template",
        help="Custom Word template file (.docx) to use for styling",
        show_default=False,
    ),
    min_severity: Severity = typer.Option(
        Severity.INFO,
        "--min-severity",
        help="Minimum severity level to include in the report",
        case_sensitive=False,
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-V",
        help="Enable verbose logging output",
    ),
    log_file: str | None = typer.Option(
        None,
        "--log-file",
        help="Write logs to the specified file",
        show_default=False,
    ),
) -> None:
    setup_logger(verbose=verbose, log_file=log_file)
    logger.info("Starting report generation")

    input_p = Path(input_path)
    output_p = Path(output_path)

    findings: list[any] = []
    if input_p.is_file():
        findings = _parse_single_file(input_p)
    elif input_p.is_dir():
        findings = _parse_directory(input_p)
    else:
        logger.error(f"Invalid input path: {input_path}")
        raise typer.Exit(code=1)

    severity_order = {
        Severity.INFO: 0,
        Severity.LOW: 1,
        Severity.MEDIUM: 2,
        Severity.HIGH: 3,
        Severity.CRITICAL: 4,
    }
    min_level = severity_order.get(min_severity, 0)
    filtered_findings = []
    for f in findings:
        sev = f.severity.lower()
        level = severity_order.get(sev, 0)
        if level >= min_level:
            filtered_findings.append(f)
    findings = filtered_findings
    logger.info(f"Filtered to {len(findings)} findings with minimum severity {min_severity}")

    findings = aggregate_findings(findings)

    output_ext = output_p.suffix.lower()
    if format == OutputFormat.AUTO:
        if output_ext == ".xlsx":
            fmt = OutputFormat.EXCEL
        elif output_ext == ".docx":
            fmt = OutputFormat.WORD
        else:
            fmt = OutputFormat.EXCEL
    else:
        fmt = format

    if fmt == OutputFormat.EXCEL:
        theme_obj = get_theme(theme.value)
        writer = ExcelReportWriter(theme_obj)
    elif fmt == OutputFormat.WORD:
        template_p = Path(template) if template else None
        writer = WordReportWriter(template_p)
    else:
        logger.error(f"Invalid output format: {fmt}")
        raise typer.Exit(code=1)

    writer.write(output_p, findings)

    logger.success(f"Report generated successfully: {output_path}")


def _parse_single_file(file_path: Path) -> list[any]:
    validate_file_path(str(file_path), must_exist=True)
    ext = file_path.suffix.lower()
    if ext == ".csv":
        parser = CSVParser()
    elif ext == ".nessus":
        parser = NessusXMLParser()
    else:
        logger.error(f"Unsupported file format: {ext}")
        raise typer.Exit(code=1)
    return parser.parse(file_path)


def _parse_directory(dir_path: Path) -> list[any]:
    findings = []
    csv_files = list(dir_path.glob("*.csv"))
    nessus_files = list(dir_path.glob("*.nessus"))
    all_files = csv_files + nessus_files
    logger.info(f"Found {len(all_files)} files in directory")
    for file in all_files:
        try:
            findings.extend(_parse_single_file(file))
        except Exception as e:
            logger.warning(f"Skipping file {file}: {e}")
    return findings


if __name__ == "__main__":
    app()

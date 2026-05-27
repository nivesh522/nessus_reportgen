from pathlib import Path

import typer
from loguru import logger

from . import __version__
from .parsers import CSVParser, NessusXMLParser
from .processors import aggregate_findings
from .report import ExcelReportWriter, WordReportWriter, get_theme
from .utils import setup_logger, validate_file_path

app = typer.Typer(
    name="nessus-reportgen",
    help="Enterprise-grade Nessus vulnerability scan report generator",
    add_completion=False,
)


def version_callback(value: bool) -> None:
    if value:
        typer.echo(f"nessus-reportgen v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool | None = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit",
    ),
) -> None:
    pass


@app.command()
def generate(
    input_path: str = typer.Argument(..., help="Input file or directory (CSV or Nessus XML)"),
    output_path: str = typer.Argument(..., help="Output file (.xlsx or .docx)"),
    format: str = typer.Option("auto", "--format", "-f", help="Output format (auto/excel/word)"),
    theme: str = typer.Option(
        "corporate", "--theme", "-t", help="Report theme for Excel (corporate/dark)"
    ),
    template: str | None = typer.Option(None, "--template", help="Word template file (.docx)"),
    min_severity: str = typer.Option(
        "info", "--min-severity", help="Minimum severity to include (info/low/medium/high/critical)"
    ),
    verbose: bool = typer.Option(False, "--verbose", help="Enable verbose logging"),
    log_file: str | None = typer.Option(None, "--log-file", help="Log file path"),
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

    severity_order = {"info": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}
    min_sev = min_severity.lower()
    min_level = severity_order.get(min_sev, 0)
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
    if format == "auto":
        if output_ext == ".xlsx":
            fmt = "excel"
        elif output_ext == ".docx":
            fmt = "word"
        else:
            fmt = "excel"
    else:
        fmt = format

    if fmt == "excel":
        theme_obj = get_theme(theme)
        writer = ExcelReportWriter(theme_obj)
    elif fmt == "word":
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

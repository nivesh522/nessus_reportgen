from pathlib import Path

from docx import Document
from docx.oxml import parse_xml
from docx.shared import Pt, RGBColor
from loguru import logger

from ..models import Finding


def set_cell_shading(cell, fill_color: str) -> None:
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(
        r'<w:shd xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:fill="%s"/>'
        % fill_color
    )
    tcPr.append(shd)


def set_cell_width(cell, width: int, width_type: str = "dxa") -> None:
    tcPr = cell._element.get_or_add_tcPr()
    tcW = parse_xml(
        r'<w:tcW xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:w="%d" w:type="%s"/>'
        % (width, width_type)
    )
    tcPr.append(tcW)


def enable_text_wrap(cell) -> None:
    tcPr = cell._element.get_or_add_tcPr()
    text_wrap = parse_xml(
        r'<w:noWrap xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:val="0"/>'
    )
    tcPr.append(text_wrap)


SEVERITY_COLORS = {
    "Critical": "C0504D",
    "High": "F79646",
    "Medium": "F0F04E",
    "Low": "9BBB59",
    "Info": "4BACC6",
    "Informational": "4BACC6",
}
HEADER_FILL_COLOR = "73A0DD"
COLUMN_WIDTHS = [2093, 11083]  # left, right in dxa


class WordReportWriter:
    def __init__(self, template_path: Path | None = None):
        self.template_path = template_path

    def write(self, output_path: Path, findings: list[Finding]) -> None:
        if self.template_path and self.template_path.exists():
            doc = Document(str(self.template_path))
        else:
            doc = Document()

        self._add_executive_summary(doc, findings)
        self._add_host_summary(doc, findings)
        self._add_findings(doc, findings)

        doc.save(str(output_path))
        logger.info(f"Word report written to {output_path}")

    def _add_executive_summary(self, doc: Document, findings: list[Finding]) -> None:
        severity_counts: dict[str, int] = {
            "Critical": 0,
            "High": 0,
            "Medium": 0,
            "Low": 0,
            "Info": 0,
        }
        for f in findings:
            sev = f.severity.capitalize()
            if sev in severity_counts:
                severity_counts[sev] += 1
            else:
                severity_counts["Info"] += 1

        doc.add_heading("Executive Summary", level=1)
        doc.add_paragraph("The following vulnerabilities were identified during the assessment:")

        table = doc.add_table(rows=2, cols=4)
        header_cells = table.rows[0].cells
        header_cells[0].text = "Critical"
        header_cells[1].text = "High"
        header_cells[2].text = "Medium"
        header_cells[3].text = "Low"

        data_cells = table.rows[1].cells
        data_cells[0].text = str(severity_counts["Critical"])
        data_cells[1].text = str(severity_counts["High"])
        data_cells[2].text = str(severity_counts["Medium"])
        data_cells[3].text = str(severity_counts["Low"])

        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        run.font.size = Pt(11)
        doc.add_paragraph()

    def _add_host_summary(self, doc: Document, findings: list[Finding]) -> None:
        host_data: dict[str, dict[str, int]] = {}
        all_ips: list[str] = []
        for f in findings:
            for ip in f.affected_ips:
                if ip not in host_data:
                    host_data[ip] = {
                        "Total": 0,
                        "Critical": 0,
                        "High": 0,
                        "Medium": 0,
                        "Low": 0,
                        "Info": 0,
                    }
                    all_ips.append(ip)
                host_data[ip]["Total"] += 1
                sev = f.severity.capitalize()
                if sev in host_data[ip]:
                    host_data[ip][sev] += 1
                else:
                    host_data[ip]["Info"] += 1

        doc.add_heading("Identified Hosts", level=2)
        doc.add_paragraph(
            f"In total {len(all_ips)} hosts were identified during the scan that had vulnerabilities in them."
        )
        table = doc.add_table(rows=1, cols=1)
        table.rows[0].cells[0].text = "IP"
        for ip in sorted(all_ips):
            row_cells = table.add_row().cells
            row_cells[0].text = ip
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        run.font.size = Pt(11)
        doc.add_paragraph()

        doc.add_heading("Open Ports", level=2)
        doc.add_paragraph("")
        doc.add_heading("Vulnerabilities", level=2)
        doc.add_heading("Vulnerabilities and Affected Hosts", level=3)

    def _add_findings(self, doc: Document, findings: list[Finding]) -> None:
        for finding in findings:
            if finding.severity.lower() == "info":
                continue
            table = doc.add_table(rows=8, cols=2)
            fields = [
                ("Synopsis", finding.synopsis or "N/A"),
                ("Ports", ", ".join(finding.ports) if finding.ports else "N/A"),
                ("Severity", finding.severity),
                ("Risk", finding.risk or "N/A"),
                ("Description", finding.description or "N/A"),
                ("Solution", finding.solution or "N/A"),
                ("CVE numbers", "\n".join(finding.cves) if finding.cves else ""),
                (
                    "Affected IP addresses",
                    ", ".join(finding.affected_ips) if finding.affected_ips else "N/A",
                ),
            ]
            for i, (label, value) in enumerate(fields):
                cell_left = table.rows[i].cells[0]
                cell_right = table.rows[i].cells[1]
                cell_left.text = label
                cell_right.text = value

                # Set column widths
                set_cell_width(cell_left, COLUMN_WIDTHS[0])
                set_cell_width(cell_right, COLUMN_WIDTHS[1])

                # Enable text wrapping
                enable_text_wrap(cell_left)
                enable_text_wrap(cell_right)

                for paragraph in cell_left.paragraphs:
                    for run in paragraph.runs:
                        run.font.size = Pt(11)
                        run.font.bold = True
                        if i == 0:
                            run.font.color.rgb = RGBColor(255, 255, 255)

                for paragraph in cell_right.paragraphs:
                    for run in paragraph.runs:
                        run.font.size = Pt(11)

                if i == 0:
                    set_cell_shading(cell_left, HEADER_FILL_COLOR)
                    set_cell_shading(cell_right, HEADER_FILL_COLOR)

                if i in [2, 3]:
                    sev_key = finding.severity.capitalize()
                    if sev_key in SEVERITY_COLORS:
                        set_cell_shading(cell_right, SEVERITY_COLORS[sev_key])

            doc.add_paragraph()

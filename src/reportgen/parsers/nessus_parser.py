from pathlib import Path

from loguru import logger
from lxml import etree

from ..models import Finding
from .base import BaseParser


class NessusXMLParser(BaseParser):
    def parse(self, file_path: Path) -> list[Finding]:
        findings: list[Finding] = []
        try:
            tree = etree.parse(str(file_path))
            root = tree.getroot()
            for report_host in root.findall(".//ReportHost"):
                host_ip = report_host.get("name", "")
                for report_item in report_host.findall(".//ReportItem"):
                    try:
                        finding = self._report_item_to_finding(report_item, host_ip)
                        findings.append(finding)
                    except Exception as e:
                        logger.warning(f"Skipping ReportItem: {e}")
            logger.info(f"Successfully parsed {len(findings)} findings from Nessus XML")
            return findings
        except Exception as e:
            logger.error(f"Error parsing Nessus XML file {file_path}: {e}")
            raise

    def _report_item_to_finding(self, item: etree._Element, host_ip: str) -> Finding:
        def safe_str(path: str) -> str | None:
            elem = item.find(path)
            return elem.text.strip() if elem is not None and elem.text else None

        def safe_int_attr(attr: str) -> int | None:
            val = item.get(attr, "")
            try:
                return int(val) if val else None
            except ValueError:
                return None

        def safe_float_attr(attr: str) -> float | None:
            val = item.get(attr, "")
            try:
                return float(val) if val else None
            except ValueError:
                return None

        port = item.get("port", "")
        protocol = item.get("protocol", "")
        severity_code = item.get("severity", "0")
        severity_map = {"0": "Info", "1": "Low", "2": "Medium", "3": "High", "4": "Critical"}
        severity = severity_map.get(severity_code, "Info")

        cves = []
        for cve in item.findall(".//cve"):
            if cve.text:
                cves.append(cve.text.strip())

        return Finding(
            plugin_id=safe_int_attr("pluginID"),
            title=item.get("pluginName", "Unknown Vulnerability"),
            synopsis=safe_str("synopsis"),
            description=safe_str("description"),
            solution=safe_str("solution"),
            see_also=safe_str("see_also"),
            severity=severity,
            risk=severity,
            ports=[port] if port else [],
            affected_ips=[host_ip] if host_ip else [],
            protocol=protocol if protocol else None,
            cves=cves,
            cvss_v2=safe_float_attr("cvss_base_score"),
            cvss_v3=safe_float_attr("cvss3_base_score"),
            plugin_output=safe_str("plugin_output"),
            plugin_publication_date=safe_str("plugin_publication_date"),
            plugin_modification_date=safe_str("plugin_modification_date"),
            metasploit=bool(item.find(".//metasploit_name") is not None),
            stig_severity=safe_str("stig_severity"),
        )

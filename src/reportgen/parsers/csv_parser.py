import csv
from pathlib import Path
from typing import List, Dict, Any, Optional
from loguru import logger
from ..models import Finding
from .base import BaseParser


class CSVParser(BaseParser):
    def parse(self, file_path: Path) -> List[Finding]:
        findings: List[Finding] = []
        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row_num, row in enumerate(reader, start=2):
                    try:
                        finding = self._row_to_finding(row)
                        findings.append(finding)
                    except Exception as e:
                        logger.warning(f"Skipping row {row_num}: {e}")
            logger.info(f"Successfully parsed {len(findings)} findings from CSV")
            return findings
        except Exception as e:
            logger.error(f"Error parsing CSV file {file_path}: {e}")
            raise

    def _row_to_finding(self, row: Dict[str, Any]) -> Finding:
        def safe_str(key: str) -> Optional[str]:
            val = row.get(key, "")
            return val.strip() if val else None

        def safe_int(key: str) -> Optional[int]:
            val = row.get(key, "")
            try:
                return int(val) if val.strip() else None
            except ValueError:
                return None

        def safe_float(key: str) -> Optional[float]:
            val = row.get(key, "")
            try:
                return float(val) if val.strip() else None
            except ValueError:
                return None

        def safe_bool(key: str) -> Optional[bool]:
            val = row.get(key, "")
            val_lower = val.lower().strip()
            if val_lower in ("yes", "true", "1"):
                return True
            elif val_lower in ("no", "false", "0"):
                return False
            return None

        def split_list(key: str, sep: str = ",") -> List[str]:
            val = row.get(key, "")
            if not val:
                return []
            return [x.strip() for x in val.split(sep) if x.strip()]

        cves = split_list("CVE")
        bid = split_list("BID")
        xref = split_list("XREF")
        mskb = split_list("MSKB")
        port = safe_str("Port")
        host = safe_str("Host")

        return Finding(
            plugin_id=safe_int("Plugin ID"),
            title=safe_str("Name") or "Unknown Vulnerability",
            synopsis=safe_str("Synopsis"),
            description=safe_str("Description"),
            solution=safe_str("Solution"),
            see_also=safe_str("See Also"),
            severity=safe_str("Risk") or safe_str("STIG Severity") or "Info",
            risk=safe_str("Risk"),
            ports=[port] if port else [],
            affected_ips=[host] if host else [],
            protocol=safe_str("Protocol"),
            cves=cves,
            cvss_v2=safe_float("CVSS v2.0"),
            cvss_v3=safe_float("CVSS v3.0"),
            cvss_v4=safe_float("CVSS v4.0"),
            vpr_score=safe_float("VPR Score"),
            epss_score=safe_float("EPSS Score"),
            plugin_output=safe_str("Plugin Output"),
            plugin_publication_date=safe_str("Plugin Publication Date"),
            plugin_modification_date=safe_str("Plugin Modification Date"),
            metasploit=safe_bool("Metasploit"),
            canvas=safe_bool("CANVAS"),
            core_impact=safe_bool("Core Impact"),
            risk_factor=safe_str("Risk Factor"),
            bid=bid,
            xref=xref,
            mskb=mskb,
            stig_severity=safe_str("STIG Severity"),
        )

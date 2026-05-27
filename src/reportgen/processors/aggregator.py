from loguru import logger
from typing import Optional

from ..models import Finding


def aggregate_findings(findings: list[Finding]) -> list[Finding]:
    grouped: dict[tuple[Optional[int], Optional[str]], Finding] = {}

    for finding in findings:
        key = (finding.plugin_id, finding.synopsis)
        if key not in grouped:
            grouped[key] = Finding(
                plugin_id=finding.plugin_id,
                title=finding.title,
                synopsis=finding.synopsis,
                description=finding.description,
                solution=finding.solution,
                see_also=finding.see_also,
                severity=finding.severity,
                risk=finding.risk,
                ports=[],
                affected_ips=[],
                protocol=finding.protocol,
                cves=[],
                cvss_v2=finding.cvss_v2,
                cvss_v3=finding.cvss_v3,
                cvss_v4=finding.cvss_v4,
                vpr_score=finding.vpr_score,
                epss_score=finding.epss_score,
                plugin_output=finding.plugin_output,
                plugin_publication_date=finding.plugin_publication_date,
                plugin_modification_date=finding.plugin_modification_date,
                metasploit=finding.metasploit,
                canvas=finding.canvas,
                core_impact=finding.core_impact,
                risk_factor=finding.risk_factor,
                bid=[],
                xref=[],
                mskb=[],
                stig_severity=finding.stig_severity,
            )
        existing = grouped[key]

        existing.ports = list(dict.fromkeys(existing.ports + finding.ports))
        existing.affected_ips = list(dict.fromkeys(existing.affected_ips + finding.affected_ips))
        existing.cves = list(dict.fromkeys(existing.cves + finding.cves))
        existing.bid = list(dict.fromkeys(existing.bid + finding.bid))
        existing.xref = list(dict.fromkeys(existing.xref + finding.xref))
        existing.mskb = list(dict.fromkeys(existing.mskb + finding.mskb))

    result = list(grouped.values())
    logger.info(f"Aggregated {len(findings)} findings into {len(result)} unique findings")
    return result

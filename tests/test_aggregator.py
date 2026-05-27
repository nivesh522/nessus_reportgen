from reportgen.models import Finding
from reportgen.processors import aggregate_findings


def test_aggregate_findings():
    f1 = Finding(
        plugin_id=35291,
        title="Weak Hash Algorithm",
        synopsis="The remote service uses a weak hash algorithm.",
        severity="High",
        ports=["443"],
        affected_ips=["192.168.10.35"],
        cves=["CVE-2004-2761"],
    )
    f2 = Finding(
        plugin_id=35291,
        title="Weak Hash Algorithm",
        synopsis="The remote service uses a weak hash algorithm.",
        severity="High",
        ports=["8443"],
        affected_ips=["192.168.10.119"],
        cves=["CVE-2004-2761"],
    )
    findings = [f1, f2]
    aggregated = aggregate_findings(findings)

    assert len(aggregated) == 1
    result = aggregated[0]
    assert result.plugin_id == 35291
    assert result.ports == ["443", "8443"]
    assert result.affected_ips == ["192.168.10.35", "192.168.10.119"]

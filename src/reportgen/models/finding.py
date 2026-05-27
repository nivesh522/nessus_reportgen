
from pydantic import BaseModel, ConfigDict, Field


class Finding(BaseModel):
    model_config = ConfigDict(frozen=False)

    plugin_id: int | None = None
    title: str
    synopsis: str | None = None
    description: str | None = None
    solution: str | None = None
    see_also: str | None = None
    severity: str
    risk: str | None = None
    ports: list[str] = Field(default_factory=list)
    affected_ips: list[str] = Field(default_factory=list)
    protocol: str | None = None
    cves: list[str] = Field(default_factory=list)
    cvss_v2: float | None = None
    cvss_v3: float | None = None
    cvss_v4: float | None = None
    vpr_score: float | None = None
    epss_score: float | None = None
    plugin_output: str | None = None
    plugin_publication_date: str | None = None
    plugin_modification_date: str | None = None
    metasploit: bool | None = None
    canvas: bool | None = None
    core_impact: bool | None = None
    risk_factor: str | None = None
    bid: list[str] = Field(default_factory=list)
    xref: list[str] = Field(default_factory=list)
    mskb: list[str] = Field(default_factory=list)
    stig_severity: str | None = None

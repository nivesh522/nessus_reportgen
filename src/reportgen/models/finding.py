from pydantic import BaseModel, Field
from typing import List, Optional


class Finding(BaseModel):
    plugin_id: Optional[int] = None
    title: str
    synopsis: Optional[str] = None
    description: Optional[str] = None
    solution: Optional[str] = None
    see_also: Optional[str] = None
    severity: str
    risk: Optional[str] = None
    ports: List[str] = Field(default_factory=list)
    affected_ips: List[str] = Field(default_factory=list)
    protocol: Optional[str] = None
    cves: List[str] = Field(default_factory=list)
    cvss_v2: Optional[float] = None
    cvss_v3: Optional[float] = None
    cvss_v4: Optional[float] = None
    vpr_score: Optional[float] = None
    epss_score: Optional[float] = None
    plugin_output: Optional[str] = None
    plugin_publication_date: Optional[str] = None
    plugin_modification_date: Optional[str] = None
    metasploit: Optional[bool] = None
    canvas: Optional[bool] = None
    core_impact: Optional[bool] = None
    risk_factor: Optional[str] = None
    bid: List[str] = Field(default_factory=list)
    xref: List[str] = Field(default_factory=list)
    mskb: List[str] = Field(default_factory=list)
    stig_severity: Optional[str] = None

    class Config:
        frozen = False

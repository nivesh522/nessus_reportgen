from dataclasses import dataclass
from typing import Dict


@dataclass
class Theme:
    name: str
    header_bg: str
    header_font: str
    cell_bg: str
    cell_font: str
    critical_bg: str
    high_bg: str
    medium_bg: str
    low_bg: str
    info_bg: str


THEMES: Dict[str, Theme] = {
    "corporate": Theme(
        name="Corporate Minimal",
        header_bg="4472C4",
        header_font="FFFFFF",
        cell_bg="FFFFFF",
        cell_font="000000",
        critical_bg="C00000",
        high_bg="FF0000",
        medium_bg="FFC000",
        low_bg="92D050",
        info_bg="00B0F0",
    ),
    "dark": Theme(
        name="Dark Theme",
        header_bg="212121",
        header_font="FFFFFF",
        cell_bg="333333",
        cell_font="E0E0E0",
        critical_bg="8B0000",
        high_bg="CD5C5C",
        medium_bg="DAA520",
        low_bg="6B8E23",
        info_bg="4682B4",
    ),
}


def get_theme(theme_name: str) -> Theme:
    return THEMES.get(theme_name.lower(), THEMES["corporate"])

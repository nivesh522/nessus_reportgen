from abc import ABC, abstractmethod
from pathlib import Path

from ..models import Finding


class BaseParser(ABC):
    @abstractmethod
    def parse(self, file_path: Path) -> list[Finding]:
        pass

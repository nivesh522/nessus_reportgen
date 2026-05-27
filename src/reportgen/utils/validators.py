from pathlib import Path
from typing import Optional
from loguru import logger


def validate_file_path(file_path: str, must_exist: bool = True) -> Path:
    path = Path(file_path)
    if must_exist and not path.exists():
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")
    return path

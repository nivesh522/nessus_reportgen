import sys

from loguru import logger


def setup_logger(verbose: bool = False, log_file: str | None = None) -> None:
    logger.remove()
    level = "DEBUG" if verbose else "INFO"
    logger.add(
        sys.stderr,
        level=level,
        format="<level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    )
    if log_file:
        logger.add(log_file, rotation="500 MB", retention="10 days", level="DEBUG")

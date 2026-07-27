import logging
from pathlib import Path

from rich.console import Console


console = Console()

logger = logging.getLogger("CryptoIntelOS")


def initialize_logger():
    """
    Initialize console and file logging.
    """

    logger.setLevel(logging.INFO)

    log_directory = Path("logs")
    log_directory.mkdir(
        exist_ok=True,
    )

    log_file = log_directory / "cryptointel.log"

    if logger.hasHandlers():
        logger.handlers.clear()

    file_handler = logging.FileHandler(
        log_file,
        encoding="utf-8",
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler.setFormatter(
        formatter,
    )

    logger.addHandler(
        file_handler,
    )

    console.print(
        "[green][OK] Logger initialized[/green]"
    )

    logger.info(
        "Logger initialized successfully"
    )
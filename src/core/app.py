from src.core.banner import show_banner
from src.core.config import config
from src.core.logger import initialize_logger, logger


def run():
    """Start the CryptoIntel OS application."""

    show_banner()

    initialize_logger()

    config.verify_directories()

    logger.info("Project directories verified")

    print(f"Version: {config.version}")
    print(f"Environment: {config.environment}")

    logger.info("Application startup completed")

    print("\n✓ CryptoIntel OS is ready!")
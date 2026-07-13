from src.core.banner import show_banner
from src.core.config import config
from src.core.logger import initialize_logger, logger
from src.database.manager import database


def run():
    """Start the CryptoIntel OS application."""

    show_banner()

    initialize_logger()

    config.verify_directories()

    database.connect()
    database.create_tables()

    logger.info("Project directories verified")
    logger.info("Database connected")
    logger.info("Database tables verified")

    print(f"Version: {config.version}")
    print(f"Environment: {config.environment}")

    logger.info("Application startup completed")

    print("\n✓ CryptoIntel OS is ready!")

    database.close()
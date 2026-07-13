from src.core.banner import show_banner
from src.core.config import load_configuration
from src.core.logger import initialize_logger


def run():
    """Start the CryptoIntel OS application."""

    show_banner()
    load_configuration()
    initialize_logger()

    print("\n✓ CryptoIntel OS is ready!")
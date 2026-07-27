from src.web_engine.manager import (
    browser_manager,
)

from src.core.banner import show_banner

from src.core.config import config

from src.core.logger import (
    initialize_logger,
    logger,
)

from src.database.manager import database

from src.scheduler.scheduler import scheduler

from src.services.project_service import (
    project_service,
)

from src.services.event_service import (
    event_service,
)


def run():
    """
    Starts CryptoIntel OS.
    """

    show_banner()

    initialize_logger()

    config.verify_directories()

    database.connect()

    database.create_tables()

    # ---------------------------------------
    # Start Chromium Browser
    # ---------------------------------------

    browser_manager.start()

    try:

        scheduler.run()

        print("\nStored Projects\n")

        for project in project_service.list_projects():

            print(project)

        print("\nStored Events\n")

        for event in event_service.list_events():

            print(event)

        logger.info(
            "Application startup completed"
        )

        print(f"\nVersion: {config.version}")

        print(
            f"Environment: {config.environment}"
        )

        print("\n✓ CryptoIntel OS is ready!")

    finally:

        # ---------------------------------------
        # Always close browser and database
        # ---------------------------------------

        browser_manager.stop()

        database.close()
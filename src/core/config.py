import os
from pathlib import Path

from dotenv import load_dotenv


class Config:
    """
    Application configuration manager.
    """

    def __init__(self):
        load_dotenv()

        self.project_root = Path(__file__).resolve().parents[2]

        self.data_dir = self.project_root / "data"
        self.logs_dir = self.project_root / "logs"
        self.assets_dir = self.project_root / "assets"
        self.docs_dir = self.project_root / "docs"

        self.environment = os.getenv(
            "ENVIRONMENT",
            "development",
        )

        self.version = "0.2.0"

        # -----------------------------
        # API Tokens
        # -----------------------------

        self.github_token = os.getenv("GITHUB_TOKEN", "")

    def verify_directories(self):
        """
        Ensure required project folders exist.
        """

        directories = [
            self.data_dir,
            self.logs_dir,
            self.assets_dir,
            self.docs_dir,
        ]

        for directory in directories:
            directory.mkdir(exist_ok=True)

        print("✓ Project directories verified")


config = Config()
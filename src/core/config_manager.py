import json
from pathlib import Path


class ConfigManager:
    """
    Loads configuration files for CryptoIntel OS.
    """

    def __init__(self):
        self.config_path = Path("config")

        self.collectors = self._load_json(
            "collectors.json"
        )

    def _load_json(self, filename):
        """
        Load a JSON configuration file.
        """

        path = self.config_path / filename

        if not path.exists():
            raise FileNotFoundError(
                f"Missing configuration file: {path}"
            )

        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    def collector_enabled(self, name):
        """
        Check whether a collector is enabled.
        """

        return self.collectors.get(name, False)


config_manager = ConfigManager()
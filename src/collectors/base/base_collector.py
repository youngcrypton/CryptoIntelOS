from abc import ABC, abstractmethod
from datetime import datetime


class BaseCollector(ABC):
    """
    Base class for every collector in CryptoIntel OS.
    """

    def __init__(self, name: str):
        self.name = name
        self.running = False
        self.last_run = None

    def start(self):
        self.running = True
        print(f"[{self.name}] Collector started.")

    def stop(self):
        self.running = False
        print(f"[{self.name}] Collector stopped.")

    def execute(self):
        """
        Executes one collection cycle.
        """

        if not self.running:
            self.start()

        raw_data = self.collect()

        normalized_data = self.normalize(raw_data)

        self.last_run = datetime.utcnow()

        return normalized_data

    @abstractmethod
    def collect(self):
        """
        Collect raw intelligence.
        """
        pass

    @abstractmethod
    def normalize(self, data):
        """
        Normalize raw intelligence into CryptoIntel format.
        """
        pass
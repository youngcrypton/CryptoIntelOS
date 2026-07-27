from abc import ABC, abstractmethod


class BaseCollector(ABC):
    """
    Base class for every CryptoIntel collector.
    """

    name = "Base Collector"

    @abstractmethod
    def collect(self, project):
        """
        Collect intelligence for one project.

        Must return either:
            None

        or

            CollectorResult
        """
        pass
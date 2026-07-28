from abc import ABC, abstractmethod


class BaseNotification(ABC):
    """
    Base notification provider.
    """

    @abstractmethod
    def send(self, event):
        pass
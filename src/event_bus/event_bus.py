from collections import defaultdict


class EventBus:
    """
    Central event dispatcher for CryptoIntel OS.
    """

    def __init__(self):
        self.subscribers = defaultdict(list)

    def subscribe(self, event_type, callback):
        """
        Register a listener.
        """

        self.subscribers[event_type].append(callback)

    def publish(self, event_type, event):
        """
        Publish an event to all listeners.
        """

        for callback in self.subscribers[event_type]:
            callback(event)


event_bus = EventBus()
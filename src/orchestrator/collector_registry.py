class CollectorRegistry:
    """
    Stores every collector registered with CryptoIntel OS.
    """

    def __init__(self):
        self.collectors = []

    def register(self, collector):

        self.collectors.append(collector)

        print(
            f"[Registry] Registered: {collector.name}"
        )

    def unregister(self, collector):

        if collector in self.collectors:
            self.collectors.remove(collector)

    def all(self):

        return self.collectors


collector_registry = CollectorRegistry()
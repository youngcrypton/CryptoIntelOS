class IntelligenceRegistry:
    """
    Stores every intelligence engine available
    inside CryptoIntel OS.
    """

    def __init__(self):

        self._engines = {}

    def register(
        self,
        collector_name,
        engine,
    ):

        self._engines[collector_name] = engine

    def get_engine(
        self,
        collector_name,
    ):

        return self._engines.get(collector_name)

    def list_engines(self):

        return self._engines


intelligence_registry = IntelligenceRegistry()
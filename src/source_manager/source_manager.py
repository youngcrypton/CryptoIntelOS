from src.source_manager.source import IntelligenceSource


class SourceManager:
    """
    Central registry for every intelligence source.
    """

    def __init__(self):

        self.sources = {}

    def register(self, source: IntelligenceSource):

        self.sources[source.name] = source

        print(f"[Source Manager] Registered {source.name}")

    def get(self, name):

        return self.sources.get(name)

    def all(self):

        return list(self.sources.values())

    def enabled_sources(self):

        return [
            source
            for source in self.sources.values()
            if source.enabled
        ]


source_manager = SourceManager()
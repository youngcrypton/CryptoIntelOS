"""Backward-compatible query loader facade."""

from .ecosystem_loader import ecosystem_loader


class QueryLoader:
    def load_ecosystems(self):
        return ecosystem_loader.load()


query_loader = QueryLoader()

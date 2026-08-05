import json
from pathlib import Path

from src.catalog.source_definition import SourceDefinition


class CatalogLoader:

    def __init__(self):

        self.catalog_path = Path("catalog/sources")

    def load(self):

        sources = []

        for file in self.catalog_path.glob("*.json"):

            with open(file, "r", encoding="utf-8") as f:

                data = json.load(f)

            sources.append(SourceDefinition(**data))

        return sources


catalog_loader = CatalogLoader()
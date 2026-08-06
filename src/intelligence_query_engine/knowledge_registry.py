from src.intelligence_query_engine.ecosystem_loader import ecosystem_loader
from src.intelligence_query_engine.domain_loader import domain_loader


class KnowledgeRegistry:

    def get_ecosystems(self):
        return ecosystem_loader.load()

    def get_domains(self):
        return domain_loader.load()

    def get_all(self):

        return {
            "ecosystems": self.get_ecosystems(),
            "domains": self.get_domains(),
        }


knowledge_registry = KnowledgeRegistry()
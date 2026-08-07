from src.core_intelligence.models import Evidence, Observation
from .analysis_engine import WebsiteAnalysisEngine

class AuditAnalyzer:
    def analyze(self, observation: Observation) -> tuple[Evidence, ...]:
        return tuple(item for item in WebsiteAnalysisEngine().analyze(observation).evidence if item.metric == "website.security")

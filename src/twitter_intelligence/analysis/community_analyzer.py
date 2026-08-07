from src.core_intelligence.models import Evidence, Observation
from .analysis_engine import TwitterAnalysisEngine

class CommunityAnalyzer:
    def analyze(self, observation: Observation) -> tuple[Evidence, ...]:
        return tuple(item for item in TwitterAnalysisEngine().analyze(observation).evidence if item.metric == "twitter.community")

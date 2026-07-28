from src.models.project_intelligence_profile import (
    ProjectIntelligenceProfile,
)


class IntelligenceAnalyzer:
    """
    AI Intelligence Analyzer.

    Reads a Project Intelligence Profile and produces
    a confidence score and executive summary.
    """

    def analyze(self, profile: ProjectIntelligenceProfile):

        score = profile.signal_count * 15

        if score > 100:
            score = 100

        profile.confidence_score = score

        profile.ai_summary = (
            f"{profile.project_name} currently has "
            f"{profile.signal_count} intelligence signals. "
            f"Current confidence is {score}%."
        )

        return profile


analyzer = IntelligenceAnalyzer()
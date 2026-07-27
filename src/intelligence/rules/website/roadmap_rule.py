from src.intelligence.rules.base_rule import BaseRule


class RoadmapRule(BaseRule):
    """
    Detects roadmap pages.
    """

    name = "Roadmap Rule"

    priority = "Medium"

    def evaluate(self, website):

        text = website.page_text.lower()

        keywords = [
            "roadmap",
            "coming soon",
            "next phase",
            "future plans",
            "milestone",
        ]

        for keyword in keywords:

            if keyword in text:

                return {
                    "title": "Roadmap Detected",
                    "summary": keyword,
                    "confidence": 90,
                    "priority": self.priority,
                }

        return None


roadmap_rule = RoadmapRule()
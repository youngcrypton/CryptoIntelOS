from src.intelligence.rules.base_rule import BaseRule


class TeamRule(BaseRule):
    """
    Detects team information.
    """

    name = "Team Rule"

    priority = "Low"

    def evaluate(self, website):

        text = website.page_text.lower()

        keywords = [
            "team",
            "founder",
            "founders",
            "our team",
            "leadership",
            "advisor",
            "advisors",
        ]

        for keyword in keywords:

            if keyword in text:

                return {
                    "title": "Team Information Found",
                    "summary": f"Detected '{keyword}' on website.",
                    "confidence": 90,
                    "priority": self.priority,
                }

        return None


team_rule = TeamRule()
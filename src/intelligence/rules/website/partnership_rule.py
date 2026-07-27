from src.intelligence.rules.base_rule import BaseRule


class PartnershipRule(BaseRule):
    """
    Detects partnership announcements.
    """

    name = "Partnership Rule"

    priority = "Medium"

    def evaluate(self, website):

        text = website.page_text.lower()

        keywords = [
            "partner",
            "partnership",
            "partners",
            "ecosystem",
            "integrated with",
            "powered by",
        ]

        for keyword in keywords:

            if keyword in text:

                return {
                    "title": "Possible Partnership",
                    "summary": f"Detected '{keyword}'.",
                    "confidence": 80,
                    "priority": self.priority,
                }

        return None


partnership_rule = PartnershipRule()
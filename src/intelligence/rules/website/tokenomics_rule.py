from src.intelligence.rules.base_rule import BaseRule


class TokenomicsRule(BaseRule):
    """
    Detects tokenomics pages.
    """

    name = "Tokenomics Rule"

    priority = "High"

    def evaluate(self, website):

        text = website.page_text.lower()

        keywords = [
            "tokenomics",
            "token supply",
            "circulating supply",
            "vesting",
            "allocation",
            "airdrop",
            "staking",
            "hype",
        ]

        for keyword in keywords:

            if keyword in text:

                return {
                    "title": "Tokenomics Information Found",
                    "summary": keyword,
                    "confidence": 95,
                    "priority": self.priority,
                }

        return None


tokenomics_rule = TokenomicsRule()
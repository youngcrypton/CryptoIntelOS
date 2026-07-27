from src.intelligence.finding import Finding
from src.intelligence.rules.base_rule import BaseRule


class WhitepaperRule(BaseRule):

    name = "Whitepaper"

    def evaluate(self, website):

        findings = []

        links = getattr(
            website,
            "external_links",
            [],
        )

        for link in links:

            lower = link.lower()

            if (
                "whitepaper" in lower
                or lower.endswith(".pdf")
            ):

                findings.append(
                    Finding(
                        title="Whitepaper Found",
                        summary=link,
                        severity="Low",
                        confidence=100,
                        evidence=link,
                        source="Whitepaper Rule",
                    )
                )

        return findings


whitepaper_rule = WhitepaperRule()
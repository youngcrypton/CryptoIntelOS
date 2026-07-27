from src.intelligence.finding import Finding
from src.intelligence.rules.base_rule import BaseRule


class DocumentationRule(BaseRule):

    name = "Documentation"

    def evaluate(self, website):

        findings = []

        links = getattr(
            website,
            "external_links",
            [],
        )

        documentation_sites = (
            "docs",
            "gitbook",
            "documentation",
        )

        for link in links:

            url = link.lower()

            if any(site in url for site in documentation_sites):

                findings.append(
                    Finding(
                        title="Documentation Found",
                        summary=link,
                        severity="Low",
                        confidence=100,
                        evidence=link,
                        source="Documentation Rule",
                    )
                )

        return findings


documentation_rule = DocumentationRule()
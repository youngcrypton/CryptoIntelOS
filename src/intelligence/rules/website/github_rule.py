from src.intelligence.finding import Finding
from src.intelligence.rules.base_rule import BaseRule


class GitHubRule(BaseRule):

    name = "GitHub"

    def evaluate(self, website):

        findings = []

        links = getattr(
            website,
            "external_links",
            [],
        )

        for link in links:

            if "github.com" in link.lower():

                findings.append(
                    Finding(
                        title="GitHub Repository Found",
                        summary=link,
                        severity="Low",
                        confidence=100,
                        evidence=link,
                        source="GitHub Rule",
                    )
                )

        return findings


github_rule = GitHubRule()
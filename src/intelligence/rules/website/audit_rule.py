from src.intelligence.finding import Finding
from src.intelligence.rules.base_rule import BaseRule


class AuditRule(BaseRule):

    name = "Audit"

    AUDIT_SITES = (
        "certik",
        "halborn",
        "trailofbits",
        "quantstamp",
        "openzeppelin",
        "hacken",
        "code4rena",
        "sherlock",
    )

    def evaluate(self, website):

        findings = []

        links = getattr(
            website,
            "external_links",
            [],
        )

        for link in links:

            lower = link.lower()

            if any(site in lower for site in self.AUDIT_SITES):

                findings.append(
                    Finding(
                        title="Audit Found",
                        summary=link,
                        severity="Low",
                        confidence=100,
                        evidence=link,
                        source="Audit Rule",
                    )
                )

        return findings


audit_rule = AuditRule()
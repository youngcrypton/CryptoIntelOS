from src.intelligence.rules.registry import (
    rule_registry,
)


class RuleEngine:
    """
    Executes every registered rule and returns
    one flat list of findings.
    """

    def run(
        self,
        normalized_data,
    ):

        findings = []

        for rule in rule_registry.get_rules():

            result = rule.evaluate(
                normalized_data,
            )

            if not result:
                continue

            # Rule returned multiple findings
            if isinstance(result, list):

                findings.extend(result)

            # Rule returned one finding
            else:

                findings.append(result)

        return findings


rule_engine = RuleEngine()
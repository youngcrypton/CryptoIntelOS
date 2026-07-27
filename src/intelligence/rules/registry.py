from src.intelligence.rules.website.documentation_rule import (
    documentation_rule,
)

from src.intelligence.rules.website.github_rule import (
    github_rule,
)

from src.intelligence.rules.website.audit_rule import (
    audit_rule,
)

from src.intelligence.rules.website.whitepaper_rule import (
    whitepaper_rule,
)


class RuleRegistry:
    """
    Stores all intelligence rules.
    """

    def __init__(self):

        self._rules = []

    def register(
        self,
        rule,
    ):

        self._rules.append(rule)

    def get_rules(self):

        return self._rules


rule_registry = RuleRegistry()


# ---------------------------------------------------
# Register Website Rules
# ---------------------------------------------------

rule_registry.register(
    documentation_rule,
)

rule_registry.register(
    github_rule,
)

rule_registry.register(
    audit_rule,
)

rule_registry.register(
    whitepaper_rule,
)
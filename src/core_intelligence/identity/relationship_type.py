"""Canonical relationship categories."""
from enum import StrEnum

class RelationshipType(StrEnum):
    FOUNDED = "founded"
    OWNS = "owns"
    MAINTAINS = "maintains"
    DEPLOYS = "deploys"
    INVESTED_IN = "invested_in"
    IMPLEMENTS = "implements"
    USES = "uses"
    ASSOCIATED_WITH = "associated_with"

from enum import StrEnum
class ReasoningStatus(StrEnum):
    PENDING="pending"; COMPLETED="completed"; FAILED="failed"; INCONCLUSIVE="inconclusive"; NEEDS_REVIEW="needs_review"

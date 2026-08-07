from enum import StrEnum
class CorrelationStatus(StrEnum):
    CANDIDATE="candidate"; CONFIRMED="confirmed"; REJECTED="rejected"; NEEDS_REVIEW="needs_review"

from enum import Enum


class DistributionStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    DELIVERED = "delivered"
    RETRY_PENDING = "retry_pending"
    FAILED = "failed"
    CANCELLED = "cancelled"

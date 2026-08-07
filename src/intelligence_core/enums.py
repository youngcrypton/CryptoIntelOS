"""Shared enums for source-agnostic intelligence objects."""

from enum import Enum


class MonitoringPriority(str, Enum):
    """Operational priority assigned to an intelligence item."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IntelligenceSource(str, Enum):
    """Supported intelligence-source families."""

    TWITTER = "twitter"
    WEBSITE = "website"
    DISCORD = "discord"
    TELEGRAM = "telegram"
    GITHUB = "github"
    NEWS = "news"
    DOCUMENTATION = "documentation"
    ON_CHAIN = "on_chain"
    WALLET = "wallet"
    LAUNCHPAD = "launchpad"
    UNKNOWN = "unknown"


class SignalSeverity(str, Enum):
    """Severity of an intelligence signal."""

    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

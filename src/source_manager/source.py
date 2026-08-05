from dataclasses import dataclass
from datetime import datetime


@dataclass
class IntelligenceSource:
    """
    Represents one intelligence source monitored by CryptoIntel OS.
    """

    name: str

    category: str

    enabled: bool = True

    priority: int = 1

    scan_interval: int = 300

    last_scan: datetime | None = None

    healthy: bool = True

    rate_limit: int = 0
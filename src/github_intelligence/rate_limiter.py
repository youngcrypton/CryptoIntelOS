"""GitHub API rate-limit state tracking."""

from dataclasses import dataclass
from datetime import datetime, timezone

from .exceptions import RateLimitExceeded


@dataclass
class RateLimiter:
    """Track request usage and reset timing from GitHub response headers."""

    remaining_requests: int | None = None
    used_requests: int = 0
    reset_timestamp: int | None = None

    def update(
        self,
        remaining_requests: int,
        used_requests: int,
        reset_timestamp: int,
    ) -> None:
        """Update rate-limit state from response metadata."""

        self.remaining_requests = remaining_requests
        self.used_requests = used_requests
        self.reset_timestamp = reset_timestamp

    def ensure_available(self) -> None:
        """Raise when the known request budget is exhausted."""

        if self.remaining_requests == 0:
            raise RateLimitExceeded(self.message())

    def reset_at(self) -> datetime | None:
        """Return the reset timestamp as UTC, when known."""

        if self.reset_timestamp is None:
            return None
        return datetime.fromtimestamp(self.reset_timestamp, tz=timezone.utc)

    def message(self) -> str:
        """Return a concise rate-limit status message."""

        if self.reset_timestamp is None:
            return "GitHub API rate limit exceeded"
        return f"GitHub API rate limit exceeded; resets at {self.reset_at().isoformat()}"

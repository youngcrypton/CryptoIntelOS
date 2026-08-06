"""Thread-safe in-memory cache for intelligence query plans."""

from copy import deepcopy
from dataclasses import dataclass
from threading import RLock
from typing import Any


@dataclass(frozen=True)
class CacheStatistics:
    """Snapshot of query-cache usage and effectiveness."""

    total_entries: int
    cache_hits: int
    cache_misses: int
    hit_rate: float


class QueryCache:
    """Store generated query plans in a thread-safe in-memory cache."""

    def __init__(self) -> None:
        """Initialize an empty cache and its usage counters."""

        self._entries: dict[str, Any] = {}
        self._cache_hits = 0
        self._cache_misses = 0
        self._lock = RLock()

    def get(self, key: str) -> Any | None:
        """Return a defensive copy of a cached value, if present."""

        with self._lock:
            if key not in self._entries:
                self._cache_misses += 1
                return None

            self._cache_hits += 1
            return deepcopy(self._entries[key])

    def set(self, key: str, value: Any) -> None:
        """Store a defensive copy of a generated query plan."""

        with self._lock:
            self._entries[key] = deepcopy(value)

    def contains(self, key: str) -> bool:
        """Return whether the cache contains the supplied key."""

        with self._lock:
            return key in self._entries

    def clear(self) -> None:
        """Remove all cached entries and reset cache statistics."""

        with self._lock:
            self._entries.clear()
            self._cache_hits = 0
            self._cache_misses = 0

    def statistics(self) -> CacheStatistics:
        """Return a thread-safe snapshot of cache statistics."""

        with self._lock:
            total_requests = self._cache_hits + self._cache_misses
            hit_rate = (
                self._cache_hits / total_requests
                if total_requests
                else 0.0
            )
            return CacheStatistics(
                total_entries=len(self._entries),
                cache_hits=self._cache_hits,
                cache_misses=self._cache_misses,
                hit_rate=round(hit_rate, 4),
            )

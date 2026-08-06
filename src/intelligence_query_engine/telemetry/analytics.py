"""Thread-safe runtime analytics for Intelligence Query Engine operations."""

from dataclasses import dataclass
from threading import RLock


@dataclass(frozen=True)
class AnalyticsSnapshot:
    """Immutable snapshot of IQE runtime metrics."""

    total_query_plans_generated: int
    total_queries_generated: int
    builder_usage: dict[str, int]
    cache_hits: int
    cache_misses: int
    validation_runs: int
    validation_failures: int
    duplicates_removed: int
    average_generation_time: float
    quality_score_statistics: dict[str, float | int]


class IQEAnalytics:
    """Collect thread-safe, in-memory metrics without affecting IQE behavior."""

    def __init__(self) -> None:
        """Initialize an empty analytics collector."""

        self._lock = RLock()
        self.reset()

    def record_generation(
        self,
        builder_type: str,
        query_count: int,
        generation_time: float,
        quality_score: float | None = None,
    ) -> None:
        """Record a generated query plan and its optional quality score."""

        with self._lock:
            self._total_query_plans_generated += 1
            self._total_queries_generated += query_count
            self._builder_usage[builder_type] = (
                self._builder_usage.get(builder_type, 0) + 1
            )
            self._total_generation_time += generation_time
            if quality_score is not None:
                self._quality_scores.append(quality_score)

    def record_validation(self, valid: bool) -> None:
        """Record one validation run and whether it failed."""

        with self._lock:
            self._validation_runs += 1
            if not valid:
                self._validation_failures += 1

    def record_cache_hit(self) -> None:
        """Record a cache hit."""

        with self._lock:
            self._cache_hits += 1

    def record_cache_miss(self) -> None:
        """Record a cache miss."""

        with self._lock:
            self._cache_misses += 1

    def record_duplicate_removal(self, count: int) -> None:
        """Record the number of removed duplicate queries."""

        with self._lock:
            self._duplicates_removed += count

    def snapshot(self) -> AnalyticsSnapshot:
        """Return an immutable snapshot of all collected runtime metrics."""

        with self._lock:
            return AnalyticsSnapshot(
                total_query_plans_generated=self._total_query_plans_generated,
                total_queries_generated=self._total_queries_generated,
                builder_usage=dict(self._builder_usage),
                cache_hits=self._cache_hits,
                cache_misses=self._cache_misses,
                validation_runs=self._validation_runs,
                validation_failures=self._validation_failures,
                duplicates_removed=self._duplicates_removed,
                average_generation_time=self._average_generation_time(),
                quality_score_statistics=self._quality_score_statistics(),
            )

    def reset(self) -> None:
        """Clear all tracked metrics."""

        with self._lock:
            self._total_query_plans_generated = 0
            self._total_queries_generated = 0
            self._builder_usage: dict[str, int] = {}
            self._cache_hits = 0
            self._cache_misses = 0
            self._validation_runs = 0
            self._validation_failures = 0
            self._duplicates_removed = 0
            self._total_generation_time = 0.0
            self._quality_scores: list[float] = []

    def _average_generation_time(self) -> float:
        """Return the average plan-generation duration in seconds."""

        if not self._total_query_plans_generated:
            return 0.0

        return round(
            self._total_generation_time / self._total_query_plans_generated,
            6,
        )

    def _quality_score_statistics(self) -> dict[str, float | int]:
        """Return count, minimum, maximum, and average quality scores."""

        if not self._quality_scores:
            return {"count": 0, "minimum": 0.0, "maximum": 0.0, "average": 0.0}

        return {
            "count": len(self._quality_scores),
            "minimum": min(self._quality_scores),
            "maximum": max(self._quality_scores),
            "average": round(
                sum(self._quality_scores) / len(self._quality_scores),
                2,
            ),
        }

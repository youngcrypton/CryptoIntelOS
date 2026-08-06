"""Combined repository activity profile model."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ActivityProfile:
    """Commit and release metrics without intelligence scoring."""

    commit_metrics: dict[str, object]
    release_metrics: dict[str, object]
    development_health: str
    maintenance_status: str
    activity_summary: dict[str, object]

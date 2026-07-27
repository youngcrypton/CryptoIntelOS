from dataclasses import dataclass


@dataclass
class WebsiteSnapshotRecord:
    """Represents a website snapshot stored in the database."""

    id: int
    project: str
    url: str
    title: str
    description: str
    html_hash: str
    collected_at: str
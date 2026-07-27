from dataclasses import dataclass, field


@dataclass
class WebsiteProfile:
    """
    Structured information extracted from a website.
    """

    url: str = ""
    title: str = ""
    description: str = ""
    language: str = ""

    users: int | None = None
    daily_volume: str = ""
    max_tps: int | None = None
    block_time: str = ""
    token: str = ""

    github: list[str] = field(default_factory=list)
    docs: list[str] = field(default_factory=list)
    audits: list[str] = field(default_factory=list)
    whitepapers: list[str] = field(default_factory=list)
    partners: list[str] = field(default_factory=list)
    investors: list[str] = field(default_factory=list)
    exchanges: list[str] = field(default_factory=list)
    socials: list[str] = field(default_factory=list)
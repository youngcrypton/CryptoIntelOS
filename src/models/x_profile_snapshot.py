from dataclasses import dataclass


@dataclass
class XProfileSnapshot:
    """
    Represents a stored X profile snapshot.
    """

    id: int | None

    project: str

    username: str

    display_name: str

    bio: str

    followers: int

    following: int

    verified: bool

    website: str

    joined: str

    profile_image: str

    banner_image: str

    collected_at: str
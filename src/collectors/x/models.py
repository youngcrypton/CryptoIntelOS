from dataclasses import dataclass


@dataclass
class XProfile:
    """
    Represents a project's X profile.
    """

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
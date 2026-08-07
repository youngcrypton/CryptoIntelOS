from .exceptions import DuplicateWhaleError, WhaleNotFoundError
from .whale_profile import WhaleProfile


class WhaleRegistry:
    def __init__(self) -> None:
        self._profiles: dict[str, WhaleProfile] = {}

    def register(self, profile: WhaleProfile) -> None:
        if profile.canonical_identifier in self._profiles:
            raise DuplicateWhaleError(profile.canonical_identifier)
        self._profiles[profile.canonical_identifier] = profile

    def get(self, identifier: str) -> WhaleProfile:
        try:
            return self._profiles[identifier]
        except KeyError as error:
            raise WhaleNotFoundError(identifier) from error

    def all(self) -> tuple[WhaleProfile, ...]:
        return tuple(self._profiles.values())

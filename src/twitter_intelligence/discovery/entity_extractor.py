import re
from urllib.parse import urlparse

from .discovery_result import DiscoveredEntity, DiscoveredEntityType


class TwitterEntityExtractor:
    """Deterministically parse explicit entities without inference."""

    URL_PATTERN = re.compile(r"https?://[^\s<>()]+", re.IGNORECASE)
    EMAIL_PATTERN = re.compile(r"(?<![\w.+-])[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}(?![\w.-])")
    MENTION_PATTERN = re.compile(r"(?<!\w)@([A-Za-z0-9_]{1,15})")
    HASHTAG_PATTERN = re.compile(r"(?<!\w)#([\w]+)", re.UNICODE)
    CASHTAG_PATTERN = re.compile(r"(?<!\w)\$([A-Za-z][A-Za-z0-9]{0,9})")

    def extract(self, text: str, *, username: str | None = None) -> tuple[DiscoveredEntity, ...]:
        entities: list[DiscoveredEntity] = []
        if username:
            entities.append(self._entity(DiscoveredEntityType.USERNAME, username, username.lower().lstrip("@")))
        for match in self.MENTION_PATTERN.finditer(text):
            entities.append(self._entity(DiscoveredEntityType.MENTION, match.group(0), match.group(1).lower()))
        for match in self.HASHTAG_PATTERN.finditer(text):
            entities.append(self._entity(DiscoveredEntityType.HASHTAG, match.group(0), match.group(1).casefold()))
        for match in self.CASHTAG_PATTERN.finditer(text):
            entities.append(self._entity(DiscoveredEntityType.CASHTAG, match.group(0), match.group(1).upper()))
        for match in self.EMAIL_PATTERN.finditer(text):
            entities.append(self._entity(DiscoveredEntityType.EMAIL, match.group(0), match.group(0).lower()))
        for match in self.URL_PATTERN.finditer(text):
            url = match.group(0).rstrip(".,;:!?]\")'")
            entities.extend(self._url_entities(url))
        return self._unique(entities)

    def _url_entities(self, url: str) -> tuple[DiscoveredEntity, ...]:
        parsed = urlparse(url)
        domain = (parsed.hostname or "").lower()
        normalized = parsed._replace(netloc=domain).geturl()
        values = [self._entity(DiscoveredEntityType.URL, url, normalized)]
        if domain:
            values.append(self._entity(DiscoveredEntityType.DOMAIN, domain, domain))
        path = parsed.path.strip("/")
        if domain in {"github.com", "www.github.com"} and path:
            segments = path.split("/")
            values.append(self._entity(DiscoveredEntityType.GITHUB_ORGANIZATION, segments[0], segments[0].lower()))
            if len(segments) >= 2:
                repository = f"{segments[0]}/{segments[1]}"
                values.append(self._entity(DiscoveredEntityType.GITHUB_REPOSITORY, repository, repository.lower()))
        elif domain in {"discord.gg", "discord.com"}:
            values.append(self._entity(DiscoveredEntityType.DISCORD_INVITE, url, normalized))
        elif domain in {"t.me", "telegram.me"}:
            values.append(self._entity(DiscoveredEntityType.TELEGRAM_LINK, url, normalized))
        elif domain.endswith("gitbook.io") or domain == "gitbook.com":
            values.append(self._entity(DiscoveredEntityType.GITBOOK_LINK, url, normalized))
            values.append(self._entity(DiscoveredEntityType.DOCUMENTATION_LINK, url, normalized))
        else:
            values.append(self._entity(DiscoveredEntityType.WEBSITE, url, normalized))
        return tuple(values)

    @staticmethod
    def _entity(entity_type: DiscoveredEntityType, value: str, normalized: str) -> DiscoveredEntity:
        return DiscoveredEntity(entity_type, value, normalized)

    @staticmethod
    def _unique(values: list[DiscoveredEntity]) -> tuple[DiscoveredEntity, ...]:
        seen: set[tuple[DiscoveredEntityType, str]] = set()
        result = []
        for value in values:
            key = (value.entity_type, value.normalized_value)
            if key not in seen:
                seen.add(key)
                result.append(value)
        return tuple(result)

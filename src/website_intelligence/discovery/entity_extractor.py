import re
from urllib.parse import urljoin, urlparse, urlunparse

from .discovery_result import DiscoveredEntity, DiscoveredEntityType


class WebsiteEntityExtractor:
    """Extract explicit website entities using deterministic patterns."""

    URL_PATTERN = re.compile(r"https?://[^\s<>()]+", re.IGNORECASE)
    EMAIL_PATTERN = re.compile(r"(?<![\w.+-])[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}(?![\w.-])")

    def extract(
        self,
        text: str = "",
        *,
        urls: tuple[str, ...] = (),
        base_url: str | None = None,
    ) -> tuple[DiscoveredEntity, ...]:
        values: list[DiscoveredEntity] = []
        for match in self.EMAIL_PATTERN.finditer(text):
            values.append(self._entity(DiscoveredEntityType.EMAIL, match.group(0), match.group(0).casefold()))
        supplied_urls = [match.group(0).rstrip(".,;:!?]\")'") for match in self.URL_PATTERN.finditer(text)]
        supplied_urls.extend(urls)
        for supplied in supplied_urls:
            absolute = urljoin(base_url, supplied) if base_url else supplied
            values.extend(self._url_entities(absolute, base_url))
        return self._unique(values)

    def _url_entities(self, value: str, base_url: str | None) -> tuple[DiscoveredEntity, ...]:
        parsed = urlparse(value)
        domain = (parsed.hostname or "").casefold()
        normalized = urlunparse(parsed._replace(scheme=parsed.scheme.casefold(), netloc=domain))
        values = [self._entity(DiscoveredEntityType.URL, value, normalized)]
        if domain:
            values.append(self._entity(DiscoveredEntityType.DOMAIN, domain, domain))
        base_domain = (urlparse(base_url).hostname or "").casefold() if base_url else ""
        link_type = DiscoveredEntityType.INTERNAL_LINK if base_domain and domain == base_domain else DiscoveredEntityType.EXTERNAL_LINK
        values.append(self._entity(link_type, value, normalized))
        values.extend(self._classify(normalized, domain, parsed.path.casefold()))
        return tuple(values)

    def _classify(self, url: str, domain: str, path: str) -> tuple[DiscoveredEntity, ...]:
        result: list[DiscoveredEntity] = []
        exact_paths = {
            "docs": DiscoveredEntityType.DOCUMENTATION, "documentation": DiscoveredEntityType.DOCUMENTATION,
            "whitepaper": DiscoveredEntityType.WHITEPAPER, "blog": DiscoveredEntityType.BLOG,
            "roadmap": DiscoveredEntityType.ROADMAP, "careers": DiscoveredEntityType.CAREERS,
            "jobs": DiscoveredEntityType.CAREERS, "team": DiscoveredEntityType.TEAM,
            "audit": DiscoveredEntityType.AUDIT, "audits": DiscoveredEntityType.AUDIT,
            "faq": DiscoveredEntityType.FAQ, "contact": DiscoveredEntityType.CONTACT,
        }
        segments = set(filter(None, path.split("/")))
        for segment, entity_type in exact_paths.items():
            if segment in segments:
                result.append(self._entity(entity_type, url, url))
        if domain.endswith("gitbook.io") or domain == "gitbook.com":
            result.extend((self._entity(DiscoveredEntityType.GITBOOK, url, url), self._entity(DiscoveredEntityType.DOCUMENTATION, url, url)))
        if domain in {"github.com", "www.github.com"}:
            result.append(self._entity(DiscoveredEntityType.GITHUB_LINK, url, url))
            parts = list(filter(None, path.split("/")))
            if len(parts) >= 2:
                repository = f"{parts[0]}/{parts[1]}"
                result.append(self._entity(DiscoveredEntityType.GITHUB_REPOSITORY, repository, repository.casefold()))
        if domain in {"twitter.com", "x.com"}:
            account = next(iter(filter(None, path.split("/"))), "")
            if account:
                result.append(self._entity(DiscoveredEntityType.TWITTER_ACCOUNT, url, account.casefold()))
        social = {"twitter.com": DiscoveredEntityType.TWITTER_ACCOUNT, "x.com": DiscoveredEntityType.TWITTER_ACCOUNT, "discord.gg": DiscoveredEntityType.DISCORD_INVITE, "t.me": DiscoveredEntityType.TELEGRAM_LINK, "telegram.me": DiscoveredEntityType.TELEGRAM_LINK, "linkedin.com": DiscoveredEntityType.LINKEDIN_LINK, "youtube.com": DiscoveredEntityType.YOUTUBE_LINK, "youtu.be": DiscoveredEntityType.YOUTUBE_LINK, "medium.com": DiscoveredEntityType.MEDIUM_LINK}
        for social_domain, entity_type in social.items():
            if domain == social_domain or domain.endswith(f".{social_domain}"):
                if entity_type is DiscoveredEntityType.TWITTER_ACCOUNT:
                    continue
                result.append(self._entity(entity_type, url, url))
        return tuple(result)

    @staticmethod
    def _entity(entity_type: DiscoveredEntityType, value: str, normalized: str) -> DiscoveredEntity:
        return DiscoveredEntity(entity_type, value, normalized)

    @staticmethod
    def _unique(values: list[DiscoveredEntity]) -> tuple[DiscoveredEntity, ...]:
        return tuple(dict.fromkeys(values))

from .discovery_result import DiscoveredEntity, DiscoveredEntityType


class MediaDiscovery:
    """Normalize supplied Twitter media metadata without fetching media."""

    def discover(self, media: tuple[tuple[str, str], ...]) -> tuple[DiscoveredEntity, ...]:
        results = []
        for media_type, url in media:
            entity_type = {
                "image": DiscoveredEntityType.IMAGE,
                "video": DiscoveredEntityType.VIDEO,
                "space": DiscoveredEntityType.SPACE,
            }.get(media_type.casefold(), DiscoveredEntityType.MEDIA)
            results.append(DiscoveredEntity(entity_type, url, url))
        return tuple(results)

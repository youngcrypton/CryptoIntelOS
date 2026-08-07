from .discovery_result import DiscoveredEntity, DiscoveredEntityType


class MetadataDiscovery:
    def discover(self, metadata: tuple[tuple[str, str], ...]) -> tuple[DiscoveredEntity, ...]:
        types = {
            "logo": DiscoveredEntityType.LOGO,
            "og:logo": DiscoveredEntityType.LOGO,
            "favicon": DiscoveredEntityType.FAVICON,
            "icon": DiscoveredEntityType.FAVICON,
        }
        return tuple(
            DiscoveredEntity(types.get(key.casefold(), DiscoveredEntityType.METADATA), key, value)
            for key, value in metadata
        )

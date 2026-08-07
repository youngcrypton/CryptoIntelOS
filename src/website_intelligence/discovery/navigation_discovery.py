from .discovery_result import DiscoveredEntity, DiscoveredEntityType


class NavigationDiscovery:
    """Normalize explicit navigation labels and URLs."""

    def discover(self, items: tuple[tuple[str, str], ...]) -> tuple[DiscoveredEntity, ...]:
        return tuple(DiscoveredEntity(DiscoveredEntityType.NAVIGATION, label, url) for label, url in items)

from src.discovery.sources.static import static_source


class DiscoveryEngine:
    """Coordinates all project discovery sources."""

    def discover(self):
        print("\n========== Discovery Engine ==========\n")

        projects = []

        projects.extend(
            static_source.discover()
        )

        print(f"Discovered {len(projects)} project(s).")

        print("\n========== Discovery Finished ==========\n")

        return projects


discovery_engine = DiscoveryEngine()
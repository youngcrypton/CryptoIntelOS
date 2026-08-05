from src.collectors.github_collector import GitHubCollector


class CollectorFactory:
    """
    Creates collector instances from source definitions.
    """

    def __init__(self):

        self.collectors = {
            "GitHubCollector": GitHubCollector,
        }

    def create(self, collector_name):

        collector = self.collectors.get(collector_name)

        if collector is None:

            raise ValueError(
                f"Unknown collector: {collector_name}"
            )

        return collector()


collector_factory = CollectorFactory()
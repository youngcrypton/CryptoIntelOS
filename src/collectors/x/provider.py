from src.collectors.x.models import XProfile


class XProvider:
    """
    Provides X (Twitter) data.

    Currently returns mock data.
    Later this class will connect to a real data source.
    """

    def get_profile(self, project):

        return XProfile(
            username="HyperliquidX",
            display_name="Hyperliquid",
            bio="The blockchain to house all finance.",
            followers=452317,
            following=118,
            verified=True,
            website=project.website,
            joined="2023-01-14",
            profile_image="https://example.com/profile.jpg",
            banner_image="https://example.com/banner.jpg",
        )


x_provider = XProvider()
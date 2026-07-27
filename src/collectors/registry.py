from src.core.config_manager import config_manager

from src.collectors.websites.collector import website_collector
from src.collectors.x.collector import x_collector


class CollectorRegistry:
    """
    Registers all enabled collectors.
    """

    def __init__(self):

        self._collectors = []

        self.load_collectors()

    def load_collectors(self):

        self._collectors.clear()

        print("\n========== Collector Registry ==========\n")

        self._register(
            "website",
            website_collector,
            "Website Collector",
        )

        self._register(
            "x",
            x_collector,
            "X Collector",
        )

        # Future collectors
        #
        # self._register(
        #     "telegram",
        #     telegram_collector,
        #     "Telegram Collector",
        # )
        #
        # self._register(
        #     "discord",
        #     discord_collector,
        #     "Discord Collector",
        # )
        #
        # self._register(
        #     "github",
        #     github_collector,
        #     "GitHub Collector",
        # )

        print(f"\nLoaded {len(self._collectors)} collector(s).\n")

    def _register(
        self,
        config_name,
        collector,
        display_name,
    ):

        if config_manager.collector_enabled(config_name):

            self._collectors.append(
                collector
            )

            print(f"[OK] {display_name}")

        else:

            print(f"[DISABLED] {display_name}")

    def get_collectors(self):

        return self._collectors


collector_registry = CollectorRegistry()
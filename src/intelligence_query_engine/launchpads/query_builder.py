"""Launchpad discovery-query builder for crypto project intelligence."""

from typing import Final


class LaunchpadQueryBuilder:
    """Build categorized launchpad discovery queries for a crypto project."""

    _CATEGORY_TEMPLATES: Final[dict[str, tuple[str, ...]]] = {
        "coinlist": ("CoinList {project}", "{project} CoinList", "{project} CoinList token sale"),
        "daomaker": ("DAO Maker {project}", "{project} DAO Maker", "{project} DAO Maker IDO"),
        "seedify": ("Seedify {project}", "{project} Seedify", "{project} Seedify IDO"),
        "fjord": ("Fjord Foundry {project}", "{project} Fjord", "{project} Fjord sale"),
        "legion": ("Legion {project}", "{project} Legion launchpad", "{project} Legion token sale"),
        "echo": ("Echo {project}", "{project} Echo investment", "{project} Echo sale"),
        "impossible_finance": ("Impossible Finance {project}", "{project} Impossible Finance", "{project} Impossible IDO"),
        "pumpfun": ("Pump.fun {project}", "{project} Pump.fun", "{project} Pump.fun launch"),
        "virtuals": ("Virtuals Protocol {project}", "{project} Virtuals", "{project} Virtuals launch"),
        "believe": ("Believe {project}", "{project} Believe launchpad", "{project} Believe launch"),
        "polkastarter": ("Polkastarter {project}", "{project} Polkastarter", "{project} Polkastarter IDO"),
        "binance_wallet": ("Binance Wallet {project}", "{project} Binance Wallet sale", "{project} Binance Web3 Wallet"),
        "bybit_launchpad": ("Bybit Launchpad {project}", "{project} Bybit Launchpad", "{project} Bybit token sale"),
        "kucoin_spotlight": ("KuCoin Spotlight {project}", "{project} KuCoin Spotlight", "{project} KuCoin token sale"),
        "gate_startup": ("Gate Startup {project}", "{project} Gate Startup", "{project} Gate.io token sale"),
        "okx_jumpstart": ("OKX Jumpstart {project}", "{project} OKX Jumpstart", "{project} OKX token sale"),
        "bitget_launchpad": ("Bitget Launchpad {project}", "{project} Bitget Launchpad", "{project} Bitget token sale"),
        "airdrop_platforms": ("{project} airdrop", "{project} airdrop platform", "{project} token claim"),
        "builder_programs": ("{project} builder program", "{project} developer grant", "{project} accelerator program"),
        "ecosystem_launches": ("{project} launchpad", "{project} public sale", "{project} IDO IEO ecosystem fund"),
    }

    def __init__(self, project_name: str) -> None:
        """Initialize the builder with a non-empty project name."""

        normalized_name = project_name.strip()
        if not normalized_name:
            raise ValueError("project_name must not be empty")

        self.project_name = normalized_name

    def build(self) -> dict[str, list[str]]:
        """Return launchpad discovery queries grouped by platform or program."""

        return {
            category: [
                query.format(project=self.project_name)
                for query in templates
            ]
            for category, templates in self._CATEGORY_TEMPLATES.items()
        }

"""Wallet discovery-query builder for project intelligence collection."""

from typing import Final


class WalletQueryBuilder:
    """Build categorized wallet discovery queries for a crypto project."""

    _CATEGORY_TEMPLATES: Final[dict[str, tuple[str, ...]]] = {
        "smart_money": (
            "{project} smart money",
            "{project} smart money wallet",
            "{project} profitable wallet",
        ),
        "vc_wallets": (
            "{project} VC wallet",
            "{project} venture capital wallet",
            "{project} investor wallet address",
        ),
        "foundation_wallets": (
            "{project} foundation wallet",
            "{project} foundation address",
            "{project} foundation multisig",
        ),
        "team_wallets": (
            "{project} team wallet",
            "{project} team address",
            "{project} team token allocation wallet",
        ),
        "treasury_wallets": (
            "{project} treasury wallet",
            "{project} DAO treasury address",
            "{project} treasury multisig",
        ),
        "exchange_wallets": (
            "{project} exchange wallet",
            "{project} CEX deposit wallet",
            "{project} exchange address",
        ),
        "whale_wallets": (
            "{project} whale wallet",
            "{project} whale accumulation",
            "{project} large holder wallet",
        ),
        "multisigs": (
            "{project} multisig",
            "{project} Safe multisig",
            "{project} multisig wallet address",
        ),
        "bridge_wallets": (
            "{project} bridge wallet",
            "{project} bridge contract address",
            "{project} cross-chain bridge wallet",
        ),
        "vesting_wallets": (
            "{project} vesting wallet",
            "{project} vesting contract address",
            "{project} token unlock wallet",
        ),
        "deployer_wallets": (
            "{project} deployer",
            "{project} deployer wallet",
            "{project} contract deployer address",
        ),
        "ecosystem_wallets": (
            "{project} ecosystem wallet",
            "{project} ecosystem fund wallet",
            "{project} grant wallet address",
        ),
    }

    def __init__(self, project_name: str) -> None:
        """Initialize the builder with a non-empty project name."""

        normalized_name = project_name.strip()
        if not normalized_name:
            raise ValueError("project_name must not be empty")

        self.project_name = normalized_name

    def build(self) -> dict[str, list[str]]:
        """Return wallet discovery queries grouped by wallet classification."""

        return {
            category: [
                query.format(project=self.project_name)
                for query in templates
            ]
            for category, templates in self._CATEGORY_TEMPLATES.items()
        }

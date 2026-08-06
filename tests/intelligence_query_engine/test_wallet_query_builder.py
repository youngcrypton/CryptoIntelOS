"""Tests for wallet discovery queries."""

from intelligence_query_engine.wallets.query_builder import WalletQueryBuilder


def test_wallet_builder_returns_expected_categories(project_name: str) -> None:
    queries = WalletQueryBuilder(project_name).build()

    assert set(queries) >= {"foundation_wallets", "treasury_wallets", "multisigs"}
    assert queries["foundation_wallets"][0] == "Monad foundation wallet"
    assert queries["treasury_wallets"][0] == "Monad treasury wallet"
    assert all(len(values) == len(set(values)) for values in queries.values())

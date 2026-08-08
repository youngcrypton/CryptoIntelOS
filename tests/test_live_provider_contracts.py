from datetime import UTC, datetime
from src.providers.github import GitHubConfig, GitHubConnector, GitHubProvider, GitHubAdapter
from src.providers.website import HttpConnector, WebsiteFetcher, WebsiteAdapter
from src.providers.ethereum import EthereumConfig, EthereumRpcConnector, EthereumProvider, EthereumAdapter
from src.providers.solana import SolanaConfig, SolanaRpcConnector, SolanaProvider, SolanaAdapter
from src.providers.connectors import ConnectorContext
from src.providers.providers import ProviderContext
from src.providers.adapters import AdapterContext

NOW = datetime(2026, 8, 8, tzinfo=UTC)
class Transport:
    def request(self, operation, **kwargs): return {"id": "repo-1", "url": operation}
    def call(self, operation, **kwargs): return {"hash": "0xabc", "result": operation}

def test_github_fixture_transport_provider_adapter():
    connector = GitHubConnector(GitHubConfig(token="fixture"), Transport())
    result = GitHubProvider(connector).normalize(connector.request("repos/acme/os", ConnectorContext("c", "e"), __import__('src.providers.connectors', fromlist=['ConnectorPolicy']).ConnectorPolicy()), ProviderContext("e", "c"), __import__('src.providers.providers', fromlist=['ProviderPolicy']).ProviderPolicy())
    adapted = GitHubAdapter().adapt(result, AdapterContext("e", "github"))
    assert adapted.objects[0].source == "github"

def test_website_ethereum_solana_fixture_paths():
    website = WebsiteFetcher(HttpConnector(transport=Transport())).fetch("https://example.test", ProviderContext("e", "c"))
    assert WebsiteAdapter().adapt(website, AdapterContext("e", "website")).objects[0].source == "website"
    eth = EthereumProvider(EthereumRpcConnector(EthereumConfig("fixture:"), Transport())).query("eth_getBlockByNumber", (), ProviderContext("e", "c"))
    assert EthereumAdapter().adapt(eth, AdapterContext("e", "ethereum")).objects[0].source == "ethereum"
    sol = SolanaProvider(SolanaRpcConnector(SolanaConfig("fixture:", chain_id="mainnet"), Transport())).query("getSlot", (), ProviderContext("e", "c"))
    assert SolanaAdapter().adapt(sol, AdapterContext("e", "solana")).objects[0].source == "solana"

from src.intelligence_query_engine.twitter.ecosystems.ethereum import ETHEREUM_QUERY_PACK
from src.intelligence_query_engine.twitter.ecosystems.solana import SOLANA_QUERY_PACK
from src.intelligence_query_engine.twitter.ecosystems.base import BASE_QUERY_PACK
from src.intelligence_query_engine.twitter.ecosystems.monad import MONAD_QUERY_PACK
from src.intelligence_query_engine.twitter.ecosystems.sui import SUI_QUERY_PACK
from src.intelligence_query_engine.twitter.ecosystems.bnb import BNB_QUERY_PACK
from src.intelligence_query_engine.twitter.ecosystems.ton import TON_QUERY_PACK
from src.intelligence_query_engine.twitter.ecosystems.polkadot import POLKADOT_QUERY_PACK
from src.intelligence_query_engine.twitter.ecosystems.arbitrum import ARBITRUM_QUERY_PACK
from src.intelligence_query_engine.twitter.ecosystems.optimism import OPTIMISM_QUERY_PACK
from src.intelligence_query_engine.twitter.ecosystems.avalanche import AVALANCHE_QUERY_PACK
from src.intelligence_query_engine.twitter.ecosystems.polygon import POLYGON_QUERY_PACK
from src.intelligence_query_engine.twitter.ecosystems.cosmos import COSMOS_QUERY_PACK
from src.intelligence_query_engine.twitter.ecosystems.near import NEAR_QUERY_PACK
from src.intelligence_query_engine.twitter.ecosystems.aptos import APTOS_QUERY_PACK
from src.intelligence_query_engine.twitter.ecosystems.berachain import BERACHAIN_QUERY_PACK
from src.intelligence_query_engine.twitter.ecosystems.hyperliquid import HYPERLIQUID_QUERY_PACK
from src.intelligence_query_engine.twitter.ecosystems.sei import SEI_QUERY_PACK
from src.intelligence_query_engine.twitter.ecosystems.celestia import CELESTIA_QUERY_PACK
from src.intelligence_query_engine.twitter.ecosystems.nft import NFT_QUERY_PACK
from src.intelligence_query_engine.twitter.ecosystems.funding import FUNDING_QUERY_PACK
from src.intelligence_query_engine.twitter.ecosystems.ai import AI_QUERY_PACK


class QueryLoader:

    def load_ecosystems(self):

        return {

            "ethereum": ETHEREUM_QUERY_PACK,
            "solana": SOLANA_QUERY_PACK,
            "base": BASE_QUERY_PACK,
            "monad": MONAD_QUERY_PACK,
            "sui": SUI_QUERY_PACK,
            "bnb": BNB_QUERY_PACK,
            "ton": TON_QUERY_PACK,
            "polkadot": POLKADOT_QUERY_PACK,
            "arbitrum": ARBITRUM_QUERY_PACK,
            "optimism": OPTIMISM_QUERY_PACK,
            "avalanche": AVALANCHE_QUERY_PACK,
            "polygon": POLYGON_QUERY_PACK,
            "cosmos": COSMOS_QUERY_PACK,
            "near": NEAR_QUERY_PACK,
            "aptos": APTOS_QUERY_PACK,
            "berachain": BERACHAIN_QUERY_PACK,
            "hyperliquid": HYPERLIQUID_QUERY_PACK,
            "sei": SEI_QUERY_PACK,
            "celestia": CELESTIA_QUERY_PACK,
            "nft": NFT_QUERY_PACK,
            "funding": FUNDING_QUERY_PACK,
            "ai": AI_QUERY_PACK,

        }


query_loader = QueryLoader()
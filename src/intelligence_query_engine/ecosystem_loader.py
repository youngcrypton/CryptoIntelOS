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
from src.intelligence_query_engine.twitter.ecosystems.starknet import STARKNET_QUERY_PACK
from src.intelligence_query_engine.twitter.ecosystems.zksync import ZKSYNC_QUERY_PACK
from src.intelligence_query_engine.twitter.ecosystems.linea import LINEA_QUERY_PACK
from src.intelligence_query_engine.twitter.ecosystems.scroll import SCROLL_QUERY_PACK
from src.intelligence_query_engine.twitter.ecosystems.mantle import MANTLE_QUERY_PACK
from src.intelligence_query_engine.twitter.ecosystems.injective import INJECTIVE_QUERY_PACK
from src.intelligence_query_engine.twitter.ecosystems.sonic import SONIC_QUERY_PACK


class EcosystemLoader:

    def load(self):

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
            "starknet": STARKNET_QUERY_PACK,
            "zksync": ZKSYNC_QUERY_PACK,
            "linea": LINEA_QUERY_PACK,
            "scroll": SCROLL_QUERY_PACK,
            "mantle": MANTLE_QUERY_PACK,
            "injective": INJECTIVE_QUERY_PACK,
            "sonic": SONIC_QUERY_PACK,

        }


ecosystem_loader = EcosystemLoader()
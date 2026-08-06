from src.intelligence_query_engine.twitter.domains.defi import DEFI_QUERY_PACK
from src.intelligence_query_engine.twitter.domains.depin import DEPIN_QUERY_PACK
from src.intelligence_query_engine.twitter.domains.rwa import RWA_QUERY_PACK


class DomainLoader:

    def load(self):

        return {

            "finance": {

                "defi": DEFI_QUERY_PACK,
                "rwa": RWA_QUERY_PACK,

            },

            "infrastructure": {

                "depin": DEPIN_QUERY_PACK,

            }

        }


domain_loader = DomainLoader()
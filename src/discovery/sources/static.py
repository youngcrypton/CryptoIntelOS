class StaticDiscoverySource:
    """Temporary discovery source used during development."""

    def discover(self):
        return [
            {
                "name": "Hyperliquid",
                "website": "https://hyperliquid.xyz",
                "blockchain": "HyperEVM",
                "category": "DeFi",
            }
        ]


static_source = StaticDiscoverySource()
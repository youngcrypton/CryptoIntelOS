from ._configured import ConfiguredSignalGenerator
from .signal_builder import SignalRule

class WatchlistSignal(ConfiguredSignalGenerator):
    def __init__(self) -> None:
        super().__init__(SignalRule("Watchlist Candidate", ("Active Founder", "Ecosystem Expansion", "Emerging Narrative", "Product Shipping", "Partnership Activity", "Funding Activity"), ("Founder Credibility", "Ecosystem Presence", "Narrative Strength", "Product Maturity", "Partnership Confidence", "Funding Confidence"), "low", "Add the project to the intelligence watchlist.", False))

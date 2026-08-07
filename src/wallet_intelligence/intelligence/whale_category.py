from enum import StrEnum


class WhaleCategory(StrEnum):
    VC = "vc"
    SMART_MONEY = "smart_money"
    FOUNDATION = "foundation"
    TREASURY = "treasury"
    EXCHANGE = "exchange"
    MARKET_MAKER = "market_maker"
    HIGH_CONVICTION = "high_conviction"
    EMERGING_WHALE = "emerging_whale"

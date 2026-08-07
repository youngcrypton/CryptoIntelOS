from enum import StrEnum


class LabelType(StrEnum):
    FOUNDER = "founder"
    TEAM = "team"
    FOUNDATION = "foundation"
    TREASURY = "treasury"
    VC = "vc"
    SMART_MONEY = "smart_money"
    EXCHANGE = "exchange"
    BRIDGE = "bridge"
    MARKET_MAKER = "market_maker"
    MEV = "mev"
    DAO = "dao"
    UNKNOWN = "unknown"

from src.intelligence_query_engine.shared.query_category import QueryCategory

BOOLEAN_QUERIES = {

    QueryCategory.PRE_LAUNCH: [

        '("stealth launch" OR "launching soon") (crypto OR blockchain OR web3)',

        '("testnet" AND "mainnet") (blockchain)',

        '("whitelist" OR "presale") (web3)',

    ],

    QueryCategory.HIRING: [

        '("we are hiring") (solidity OR rust OR move)',

        '("open roles") (crypto OR blockchain)',

    ],

    QueryCategory.GEM_DISCOVERY: [

        '("hidden gem") (crypto)',

        '("next 100x") (web3)',

    ]

}
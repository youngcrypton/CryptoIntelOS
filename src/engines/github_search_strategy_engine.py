from src.intelligence_query_engine.query_loader import query_loader


class GitHubSearchStrategyEngine:
    """
    Builds structured GitHub search strategies from the Intelligence Query Engine.
    """

    def build_strategies(self) -> list[dict]:

        ecosystems = query_loader.load_ecosystems()

        strategies = []
        seen = set()

        for ecosystem_name, query_pack in ecosystems.items():

            # Keywords
            for keyword in query_pack.get("keywords", []):

                key = ("keyword", keyword)

                if key in seen:
                    continue

                seen.add(key)

                strategies.append({
                    "ecosystem": ecosystem_name,
                    "category": "keyword",
                    "query": keyword,
                })

            # Boolean Queries
            for boolean_query in query_pack.get("boolean_queries", []):

                key = ("boolean", boolean_query)

                if key in seen:
                    continue

                seen.add(key)

                strategies.append({
                    "ecosystem": ecosystem_name,
                    "category": "boolean",
                    "query": boolean_query,
                })

        return strategies


github_search_strategy_engine = GitHubSearchStrategyEngine()
from src.engines.github_search_strategy_engine import (
    github_search_strategy_engine,
)

from src.services.github_search_service import (
    github_search_service,
)


print()
print("=" * 70)
print("CryptoIntel OS")
print("GitHub Multi-Query Discovery")
print("=" * 70)

strategies = github_search_strategy_engine.build_strategies()

print(f"\nStrategies Loaded : {len(strategies)}")

# Keep this small while developing.
selected_strategies = strategies[:5]

results = github_search_service.search_multiple(
    selected_strategies,
    limit_per_query=3,
)

summary = results["summary"]

print("\nDiscovery Summary")
print("-" * 70)

print(f"Queries Executed     : {summary['queries_executed']}")
print(f"Repositories Found   : {summary['repositories_found']}")
print(f"Unique Repositories  : {summary['unique_repositories']}")
print(f"Duplicates Removed   : {summary['duplicates_removed']}")

print("\nRepositories")
print("=" * 70)

for repository in results["repositories"]:

    print(repository["full_name"])

    print(f"Stars      : {repository['stars']}")

    print(f"Language   : {repository['language']}")

    print(f"Owner      : {repository['owner']}")

    print(f"Homepage   : {repository['homepage']}")

    print()

    print("Discovery Evidence")

    for evidence in repository["discovery_evidence"]:

        print(
            f"  • "
            f"{evidence['ecosystem']} | "
            f"{evidence['category']} | "
            f"{evidence['query']}"
        )

    print("-" * 70)

print("\nQuery Statistics")
print("=" * 70)

for statistic in results["statistics"]:

    print(

        f"{statistic['ecosystem']:<12}"

        f"{statistic['category']:<10}"

        f"{statistic['results']:>3} result(s)   "

        f"{statistic['query']}"

    )
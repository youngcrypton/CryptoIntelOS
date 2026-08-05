from src.engines.github_search_strategy_engine import (
    github_search_strategy_engine,
)

print()
print("=" * 60)
print("GitHub Search Strategy Engine")
print("=" * 60)

strategies = github_search_strategy_engine.build_strategies()

print(f"\nStrategies Generated: {len(strategies)}\n")

for index, strategy in enumerate(strategies[:20], start=1):

    print(f"[{index}]")

    print(f"Ecosystem : {strategy['ecosystem']}")
    print(f"Category  : {strategy['category']}")
    print(f"Query     : {strategy['query']}")

    print("-" * 60)
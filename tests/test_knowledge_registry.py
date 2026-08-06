import os
import sys

# Add the project root to Python's import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.intelligence_query_engine.knowledge_registry import knowledge_registry


def print_separator():
    print("=" * 60)


def main():

    registry = knowledge_registry.get_all()

    ecosystems = registry["ecosystems"]
    domains = registry["domains"]

    print_separator()
    print("CryptoIntel OS - Knowledge Registry Test")
    print_separator()

    print("\nECOSYSTEMS\n")

    ecosystem_count = 0

    for name, pack in ecosystems.items():

        ecosystem_count += 1

        print(f"✓ {name}")
        print(f"   Hashtags        : {len(pack['hashtags'])}")
        print(f"   Keywords        : {len(pack['keywords'])}")
        print(f"   Boolean Queries : {len(pack['boolean_queries'])}")
        print()

    print_separator()
    print(f"Total Ecosystems: {ecosystem_count}")
    print_separator()

    print("\nDOMAINS\n")

    domain_count = 0

    for category, packs in domains.items():

        print(category.upper())

        for name, pack in packs.items():

            domain_count += 1

            print(f"  ✓ {name}")
            print(f"     Hashtags        : {len(pack['hashtags'])}")
            print(f"     Keywords        : {len(pack['keywords'])}")
            print(f"     Boolean Queries : {len(pack['boolean_queries'])}")

        print()

    print_separator()
    print(f"Total Domains: {domain_count}")
    print_separator()

    print()
    print(f"Knowledge Packs Total: {ecosystem_count + domain_count}")
    print_separator()


if __name__ == "__main__":
    main()
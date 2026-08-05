import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.intelligence_query_engine.query_loader import query_loader


def main():
    ecosystems = query_loader.load_ecosystems()

    print("=" * 50)
    print("CryptoIntel OS - Query Loader Test")
    print("=" * 50)

    print("\nLoaded Query Packs:\n")

    for name, pack in ecosystems.items():
        print(f"✓ {name}")

        print(f"   Hashtags        : {len(pack['hashtags'])}")
        print(f"   Keywords        : {len(pack['keywords'])}")
        print(f"   Boolean Queries : {len(pack['boolean_queries'])}")

        print()

    print("=" * 50)
    print(f"Total Packs Loaded: {len(ecosystems)}")
    print("=" * 50)


if __name__ == "__main__":
    main()
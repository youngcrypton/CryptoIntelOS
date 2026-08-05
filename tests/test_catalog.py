from src.catalog.catalog_loader import catalog_loader


sources = catalog_loader.load()

print()

print("Loaded Intelligence Sources")

print("---------------------------")

for source in sources:

    print(
        f"{source.name} | "
        f"{source.category} | "
        f"Priority {source.priority}"
    )
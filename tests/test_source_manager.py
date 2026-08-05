from src.source_manager.source import IntelligenceSource
from src.source_manager.source_manager import source_manager


source_manager.register(
    IntelligenceSource(
        name="GitHub",
        category="Development",
        priority=10,
    )
)

source_manager.register(
    IntelligenceSource(
        name="Twitter",
        category="Social",
        priority=8,
    )
)

source_manager.register(
    IntelligenceSource(
        name="Website",
        category="Web",
        priority=9,
    )
)

print()

print("Registered Sources")

print("------------------")

for source in source_manager.all():

    print(
        source.name,
        "|",
        source.category,
        "| Priority:",
        source.priority,
    )
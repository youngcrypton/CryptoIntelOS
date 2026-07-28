from src.collectors.github_collector import (
    github_collector,
)

from src.orchestrator.orchestrator import (
    orchestrator,
)


orchestrator.register(
    github_collector
)

orchestrator.run()
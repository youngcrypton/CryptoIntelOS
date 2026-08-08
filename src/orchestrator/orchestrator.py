from datetime import datetime

from src.platform_sdk import LegacyExecutionAdapter

from src.catalog.catalog_loader import catalog_loader
from src.factory.collector_factory import collector_factory

from src.orchestrator.collector_registry import (
    collector_registry,
)

from src.orchestrator.execution_context import (
    ExecutionContext,
)

from src.orchestrator.health_monitor import (
    health_monitor,
)


class IntelligenceOrchestrator:

    def __init__(self, runtime_adapter=None):
        self.runtime_adapter = runtime_adapter or LegacyExecutionAdapter()

    def load_collectors(self):

        sources = catalog_loader.load()

        for source in sources:

            if not source.enabled:
                continue

            collector = collector_factory.create(
                source.collector
            )

            collector_registry.register(
                collector
            )

    def run(self):

        print("\n========== ORCHESTRATOR ==========\n")

        for collector in collector_registry.all():

            context = ExecutionContext(
                collector_name=collector.name,
                started_at=datetime.utcnow(),
            )

            try:

                self.runtime_adapter.execute_collector(
                    collector,
                    execution_id=f"legacy:collector:{collector.name}",
                )

                context.success = True

                health_monitor.healthy(
                    collector.name
                )

            except Exception as e:

                context.error = str(e)

                health_monitor.failed(
                    collector.name
                )

                print(e)

            context.finished_at = datetime.utcnow()

        print("\n===============================\n")


orchestrator = IntelligenceOrchestrator()

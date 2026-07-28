from datetime import datetime

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
    """
    Runs every registered collector.
    """

    def register(self, collector):

        collector_registry.register(collector)

    def run(self):

        print("\n========== ORCHESTRATOR ==========\n")

        for collector in collector_registry.all():

            context = ExecutionContext(
                collector_name=collector.name,
                started_at=datetime.utcnow(),
            )

            try:

                collector.execute()

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
from src.event_bus.event_bus import event_bus
from src.platform_sdk import LegacyExecutionAdapter

from src.intelligence.analyzer import analyzer


class IntelligencePipeline:
    """
    Central intelligence processing pipeline.
    """

    def __init__(self, runtime_adapter=None):
        self.runtime_adapter = runtime_adapter or LegacyExecutionAdapter()

    def process(self, profile):

        analyzed = analyzer.analyze(profile)

        print("\n==============================")
        print("AI INTELLIGENCE REPORT")
        print("==============================")

        print(f"Project      : {analyzed.project_name}")
        print(f"Confidence   : {analyzed.confidence_score}%")
        print(f"Signals      : {analyzed.signal_count}")

        print("\nSummary")

        print(analyzed.ai_summary)

        event_bus.publish(
            "intelligence_event",
            analyzed
        )

        self.runtime_adapter.execute_value(
            analyzed,
            source="legacy-intelligence-pipeline",
            execution_id=f"legacy:intelligence:{getattr(analyzed, 'project_name', 'project')}",
        )
        return analyzed


pipeline = IntelligencePipeline()

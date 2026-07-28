from src.event_bus.event_bus import event_bus

from src.intelligence.analyzer import analyzer


class IntelligencePipeline:
    """
    Central intelligence processing pipeline.
    """

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


pipeline = IntelligencePipeline()
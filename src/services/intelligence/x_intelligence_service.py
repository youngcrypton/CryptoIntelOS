from src.intelligence.detectors.change_detector import (
    change_detector,
)

from src.intelligence.normalizers.x_normalizer import (
    x_normalizer,
)

from src.intelligence.engine.registry import (
    intelligence_registry,
)

from src.services.event_service import (
    event_service,
)


class XIntelligenceService:
    """
    Handles all X (Twitter) intelligence.
    """

    def process(
        self,
        project,
        result,
    ):

        payload = result.payload

        print(f"Username    : {payload.username}")
        print(f"Followers   : {payload.followers:,}")
        print(f"Following   : {payload.following:,}")
        print(f"Verified    : {payload.verified}")

        current_data = x_normalizer.normalize(
            payload
        )

        # Placeholder until we build the X snapshot database
        previous_data = None

        changes = change_detector.compare(
            previous_data,
            current_data,
        )

        if changes:

            print("\n========== X Changes ==========\n")

            for change in changes:

                print(f"{change['field']}")
                print(f"Old : {change['old']}")
                print(f"New : {change['new']}\n")

        event_service.record_event(
            project=result.project,
            source=result.collector,
            signal_type=result.signal_type,
            title=result.title,
            summary=result.summary,
            priority="Medium",
            confidence=result.confidence,
            evidence=result.evidence,
        )


x_intelligence_service = XIntelligenceService()

intelligence_registry.register(
    "X Collector",
    x_intelligence_service,
)
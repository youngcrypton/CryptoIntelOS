from src.database.repositories.event_repository import event_repository


class EventService:
    """Business logic for intelligence events."""

    def record_event(
        self,
        project,
        source,
        signal_type,
        title,
        summary,
        priority="Medium",
        confidence=100,
        evidence="",
    ):
        event_repository.add_event(
            project=project,
            source=source,
            signal_type=signal_type,
            title=title,
            summary=summary,
            priority=priority,
            confidence=confidence,
            evidence=evidence,
        )

    def list_events(self):
        return event_repository.get_all_events()


event_service = EventService()
from datetime import datetime

from src.database.manager import database
from src.models.event import Event


class EventRepository:
    """Handles intelligence event database operations."""

    def add_event(
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
        cursor = database.connection.cursor()

        # Prevent duplicate events
        cursor.execute(
            """
            SELECT id
            FROM events
            WHERE project = ?
            AND title = ?
            AND summary = ?
            """,
            (
                project,
                title,
                summary,
            ),
        )

        if cursor.fetchone():
            print(f"✓ Duplicate event skipped: {title}")
            return

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            """
            INSERT INTO events
            (
                project,
                source,
                signal_type,
                title,
                summary,
                priority,
                confidence,
                evidence,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                project,
                source,
                signal_type,
                title,
                summary,
                priority,
                confidence,
                evidence,
                created_at,
            ),
        )

        database.connection.commit()

        print(f"✓ Event recorded: {title}")

    def get_all_events(self):
        cursor = database.connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                project,
                source,
                signal_type,
                title,
                summary,
                priority,
                confidence,
                evidence,
                created_at
            FROM events
            ORDER BY id DESC
            """
        )

        rows = cursor.fetchall()

        return [
            Event(
                id=row[0],
                project=row[1],
                source=row[2],
                signal_type=row[3],
                title=row[4],
                summary=row[5],
                priority=row[6],
                confidence=row[7],
                evidence=row[8],
                created_at=row[9],
            )
            for row in rows
        ]


event_repository = EventRepository()
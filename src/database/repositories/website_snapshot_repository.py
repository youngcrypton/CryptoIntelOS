from datetime import datetime

from src.database.manager import database
from src.models.website_snapshot import WebsiteSnapshotRecord


class WebsiteSnapshotRepository:
    """Handles website snapshot database operations."""

    def add_snapshot(
        self,
        project,
        url,
        title,
        description,
        html_hash,
    ):
        cursor = database.connection.cursor()

        collected_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            """
            INSERT INTO website_snapshots
            (
                project,
                url,
                title,
                description,
                html_hash,
                collected_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                project,
                url,
                title,
                description,
                html_hash,
                collected_at,
            ),
        )

        database.connection.commit()

        print("✓ Website snapshot saved")

    def get_latest_snapshot(self, project):
        cursor = database.connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                project,
                url,
                title,
                description,
                html_hash,
                collected_at
            FROM website_snapshots
            WHERE project = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (project,),
        )

        row = cursor.fetchone()

        if not row:
            return None

        return WebsiteSnapshotRecord(
            id=row[0],
            project=row[1],
            url=row[2],
            title=row[3],
            description=row[4],
            html_hash=row[5],
            collected_at=row[6],
        )


website_snapshot_repository = WebsiteSnapshotRepository()
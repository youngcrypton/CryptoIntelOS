from datetime import datetime

from src.database.manager import database
from src.models.x_profile_snapshot import XProfileSnapshot


class XProfileRepository:
    """
    Handles X profile snapshot database operations.
    """

    def add_snapshot(
        self,
        project,
        username,
        display_name,
        bio,
        followers,
        following,
        verified,
        website,
        joined,
        profile_image,
        banner_image,
    ):
        cursor = database.connection.cursor()

        collected_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            """
            INSERT INTO x_profile_snapshots
            (
                project,
                username,
                display_name,
                bio,
                followers,
                following,
                verified,
                website,
                joined,
                profile_image,
                banner_image,
                collected_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                project,
                username,
                display_name,
                bio,
                followers,
                following,
                int(verified),
                website,
                joined,
                profile_image,
                banner_image,
                collected_at,
            ),
        )

        database.connection.commit()

        print("✓ X profile snapshot saved")

    def get_latest_snapshot(self, project):
        cursor = database.connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                project,
                username,
                display_name,
                bio,
                followers,
                following,
                verified,
                website,
                joined,
                profile_image,
                banner_image,
                collected_at
            FROM x_profile_snapshots
            WHERE project = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (project,),
        )

        row = cursor.fetchone()

        if not row:
            return None

        return XProfileSnapshot(
            id=row[0],
            project=row[1],
            username=row[2],
            display_name=row[3],
            bio=row[4],
            followers=row[5],
            following=row[6],
            verified=bool(row[7]),
            website=row[8],
            joined=row[9],
            profile_image=row[10],
            banner_image=row[11],
            collected_at=row[12],
        )


x_profile_repository = XProfileRepository()
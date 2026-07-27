from src.database.manager import database
from src.models.project import Project


class ProjectRepository:
    """Handles project database operations."""

    def add_project(
        self,
        name,
        website,
        blockchain,
        category,
    ):
        cursor = database.connection.cursor()

        cursor.execute(
            """
            SELECT id
            FROM projects
            WHERE name = ?
            """,
            (name,),
        )

        if cursor.fetchone():
            print(f"✓ Project '{name}' already exists")
            return

        cursor.execute(
            """
            INSERT INTO projects
            (
                name,
                website,
                blockchain,
                category
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                name,
                website,
                blockchain,
                category,
            ),
        )

        database.connection.commit()

        print(f"✓ Project '{name}' added")

    def get_all_projects(self):
        """Return every project being monitored."""

        cursor = database.connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                name,
                website,
                blockchain,
                category,
                status
            FROM projects
            ORDER BY name
            """
        )

        rows = cursor.fetchall()

        return [
            Project(
                id=row[0],
                name=row[1],
                website=row[2],
                blockchain=row[3],
                category=row[4],
                status=row[5],
            )
            for row in rows
        ]


project_repository = ProjectRepository()
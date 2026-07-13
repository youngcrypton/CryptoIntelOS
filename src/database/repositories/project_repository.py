from src.database.manager import database


class ProjectRepository:
    """Handles all project-related database operations."""

    def add_project(
        self,
        name,
        website=None,
        discord=None,
        x=None,
        blockchain=None,
        category=None,
        status="Watching",
    ):
        """Add a new project to the database."""

        cursor = database.connection.cursor()

        cursor.execute(
            """
            INSERT INTO projects
            (name, website, discord, x, blockchain, category, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                name,
                website,
                discord,
                x,
                blockchain,
                category,
                status,
            ),
        )

        database.connection.commit()

        print(f"✓ Project '{name}' added")


project_repository = ProjectRepository()
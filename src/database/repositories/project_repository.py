from src.database.manager import database


class ProjectRepository:
    """Handles all project-related database operations."""

    def project_exists(self, name):
        """Return True if the project already exists."""

        cursor = database.connection.cursor()

        cursor.execute(
            "SELECT id FROM projects WHERE LOWER(name)=LOWER(?)",
            (name,),
        )

        return cursor.fetchone() is not None

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
        """Add a new project."""

        if self.project_exists(name):
            print(f"✓ Project '{name}' already exists")
            return

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

    def get_all_projects(self):
        """Return all stored projects."""

        cursor = database.connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                name,
                blockchain,
                category,
                status
            FROM projects
            ORDER BY id
            """
        )

        return cursor.fetchall()


project_repository = ProjectRepository()
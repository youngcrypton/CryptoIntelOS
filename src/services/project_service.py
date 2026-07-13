from src.database.repositories.project_repository import project_repository


class ProjectService:
    """Business logic for managing projects."""

    def add_project(
        self,
        name,
        website=None,
        discord=None,
        x=None,
        blockchain=None,
        category=None,
    ):
        """Add a project."""

        project_repository.add_project(
            name=name,
            website=website,
            discord=discord,
            x=x,
            blockchain=blockchain,
            category=category,
        )

    def list_projects(self):
        """Return all projects."""

        return project_repository.get_all_projects()


project_service = ProjectService()
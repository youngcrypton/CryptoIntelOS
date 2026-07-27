from src.database.repositories.project_repository import project_repository


class ProjectService:
    """Business logic for projects."""

    def add_project(
        self,
        name,
        website,
        blockchain,
        category,
    ):
        project_repository.add_project(
            name=name,
            website=website,
            blockchain=blockchain,
            category=category,
        )

    def list_projects(self):
        """Return all monitored projects."""
        return project_repository.get_all_projects()


project_service = ProjectService()
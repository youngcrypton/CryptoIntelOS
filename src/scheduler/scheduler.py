from src.collectors.registry import collector_registry
from src.discovery.engine import discovery_engine
from src.pipeline.pipeline import pipeline

from src.services.project_service import project_service


class Scheduler:
    """Coordinates all monitoring jobs."""

    def run(self):

        print("\n========== Scheduler Started ==========\n")

        # ----------------------------------
        # Discover new projects
        # ----------------------------------

        discovered_projects = discovery_engine.discover()

        for project in discovered_projects:

            project_service.add_project(
                name=project["name"],
                website=project["website"],
                blockchain=project["blockchain"],
                category=project["category"],
            )

        # ----------------------------------
        # Load monitored projects
        # ----------------------------------

        projects = project_service.list_projects()

        print(f"Monitoring {len(projects)} project(s).\n")

        # ----------------------------------
        # Run collectors
        # ----------------------------------

        for project in projects:

            print(f"Project: {project.name}")

            for collector in collector_registry.get_collectors():

                result = collector.collect(project)

                if result is None:
                    continue

                print(f"Collector   : {result.collector}")
                print(f"Signal      : {result.signal_type}")
                print(f"Summary     : {result.summary}")

                pipeline.process(project, result)

                print()

        print("========== Scheduler Finished ==========\n")


scheduler = Scheduler()
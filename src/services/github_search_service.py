from github import Github
from github.GithubException import GithubException

from src.core.config import config


class GitHubSearchService:
    """
    Service responsible for searching GitHub repositories.

    Responsibilities
    ----------------
    - Execute GitHub repository searches
    - Normalize repository data
    - Execute multiple search strategies
    - Merge duplicate repositories
    - Preserve discovery evidence
    """

    def __init__(self):

        self.client = Github(config.github_token) if config.github_token else Github()

    def search_repositories(self, query: str, limit: int = 10):

        try:

            repositories = self.client.search_repositories(
                query=query,
                sort="updated",
                order="desc",
            )

            results = []

            for repository in repositories[:limit]:

                results.append({

                    "id": repository.id,

                    "name": repository.name,

                    "full_name": repository.full_name,

                    "description": repository.description,

                    "url": repository.html_url,

                    "stars": repository.stargazers_count,

                    "forks": repository.forks_count,

                    "language": repository.language,

                    "topics": repository.get_topics(),

                    "created_at": repository.created_at,

                    "updated_at": repository.updated_at,

                    "owner": repository.owner.login,

                    "default_branch": repository.default_branch,

                    "watchers": repository.watchers_count,

                    "open_issues": repository.open_issues_count,

                    "license": (
                        repository.license.name
                        if repository.license
                        else None
                    ),

                    "homepage": repository.homepage,

                })

            return results

        except GithubException as error:

            print(f"GitHub Search Error: {error}")

            return []

    def search_multiple(
        self,
        strategies: list[dict],
        limit_per_query: int = 5,
    ):

        discovered = {}

        statistics = []

        total_matches = 0

        duplicate_matches = 0

        for strategy in strategies:

            repositories = self.search_repositories(
                query=strategy["query"],
                limit=limit_per_query,
            )

            statistics.append({

                "ecosystem": strategy["ecosystem"],

                "category": strategy["category"],

                "query": strategy["query"],

                "results": len(repositories),

            })

            total_matches += len(repositories)

            for repository in repositories:

                repository_id = repository["id"]

                if repository_id not in discovered:

                    repository["discovery_evidence"] = [strategy]

                    discovered[repository_id] = repository

                else:

                    duplicate_matches += 1

                    discovered[repository_id][
                        "discovery_evidence"
                    ].append(strategy)

        return {

            "repositories": list(discovered.values()),

            "statistics": statistics,

            "summary": {

                "queries_executed": len(strategies),

                "repositories_found": total_matches,

                "unique_repositories": len(discovered),

                "duplicates_removed": duplicate_matches,

            }

        }


github_search_service = GitHubSearchService()

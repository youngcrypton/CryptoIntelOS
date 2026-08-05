from src.services.github_search_service import github_search_service

print()
print("=" * 60)
print("GitHub Repository Discovery")
print("=" * 60)

repositories = github_search_service.search_repositories(
    "blockchain",
    limit=5,
)

print(f"\nRepositories Found: {len(repositories)}\n")

for index, repository in enumerate(repositories, start=1):

    print(f"[{index}] {repository['full_name']}")

    print(f"Stars: {repository['stars']}")

    print(f"Language: {repository['language']}")

    print(f"Description: {repository['description']}")

    print(f"URL: {repository['url']}")

    print("-" * 60)
"""Reusable builder for project-specific website discovery queries."""

from typing import Final


class WebsiteQueryBuilder:
    """Build categorized website intelligence queries for one project."""

    _CATEGORY_SUFFIXES: Final[dict[str, tuple[str, ...]]] = {
        "official_websites": (
            "official website",
            "official site",
            "project website",
        ),
        "documentation": (
            "docs",
            "documentation",
            "developer docs",
            "GitBook",
            "technical docs",
        ),
        "gitbook": (
            "GitBook",
            "documentation GitBook",
            "developer GitBook",
        ),
        "whitepapers": (
            "whitepaper",
            "litepaper",
            "technical paper",
        ),
        "roadmaps": (
            "roadmap",
            "product roadmap",
            "development roadmap",
        ),
        "blogs": (
            "blog",
            "announcements blog",
            "news updates",
        ),
        "careers": (
            "careers",
            "jobs",
            "hiring",
        ),
        "team_pages": (
            "team",
            "founders",
            "leadership team",
        ),
        "investor_pages": (
            "investors",
            "funding backers",
            "venture capital investors",
        ),
        "partner_pages": (
            "partners",
            "ecosystem partners",
            "integrations",
        ),
        "audit_reports": (
            "audit report",
            "smart contract audit",
            "security audit",
        ),
        "tokenomics": (
            "tokenomics",
            "token allocation",
            "token emissions",
        ),
        "governance": (
            "governance",
            "governance forum",
            "DAO proposals",
        ),
        "developer_docs": (
            "developer documentation",
            "developer guide",
            "developer SDK",
        ),
        "api_docs": (
            "API docs",
            "API documentation",
            "API reference",
        ),
        "status_pages": (
            "status page",
            "system status",
            "uptime status",
        ),
        "support_pages": (
            "support",
            "help center",
            "knowledge base",
        ),
        "contact_pages": (
            "contact",
            "contact us",
            "business development contact",
        ),
        "media_kits": (
            "media kit",
            "press kit",
            "brand assets",
        ),
    }

    def __init__(self, project_name: str) -> None:
        """Initialize the builder with a non-empty project name."""

        normalized_name = project_name.strip()
        if not normalized_name:
            raise ValueError("project_name must not be empty")

        self.project_name = normalized_name

    def build(self) -> dict[str, list[str]]:
        """Return website discovery queries grouped by resource category."""

        return {
            category: [
                f"{self.project_name} {suffix}"
                for suffix in suffixes
            ]
            for category, suffixes in self._CATEGORY_SUFFIXES.items()
        }

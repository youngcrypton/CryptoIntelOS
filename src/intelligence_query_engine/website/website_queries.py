"""Structured website-discovery queries for crypto intelligence collectors."""

from typing import Final


WebsiteQueries = dict[str, list[str]]


WEBSITE_QUERY_CATEGORIES: Final[WebsiteQueries] = {
    "official_websites": [
        "{project} official website",
        "{project} official site",
        "{project} official crypto project",
    ],
    "documentation": [
        "{project} documentation",
        "{project} docs",
        "{project} technical documentation",
    ],
    "gitbook": [
        "{project} GitBook",
        "site:gitbook.io {project}",
        "site:{project}.gitbook.io",
    ],
    "whitepapers": [
        "{project} whitepaper",
        "{project} litepaper",
        "{project} technical paper",
    ],
    "roadmaps": [
        "{project} roadmap",
        "{project} product roadmap",
        "{project} development roadmap",
    ],
    "blogs": [
        "{project} blog",
        "{project} announcements blog",
        "{project} news updates",
    ],
    "careers": [
        "{project} careers",
        "{project} jobs",
        "{project} hiring",
    ],
    "team_pages": [
        "{project} team",
        "{project} founders",
        "{project} leadership team",
    ],
    "investor_pages": [
        "{project} investors",
        "{project} funding backers",
        "{project} venture capital investors",
    ],
    "partner_pages": [
        "{project} partners",
        "{project} ecosystem partners",
        "{project} integrations",
    ],
    "audit_reports": [
        "{project} audit report",
        "{project} smart contract audit",
        "{project} security audit PDF",
    ],
    "tokenomics": [
        "{project} tokenomics",
        "{project} token allocation",
        "{project} token emissions",
    ],
    "governance": [
        "{project} governance",
        "{project} governance forum",
        "{project} DAO proposals",
    ],
    "media_kits": [
        "{project} media kit",
        "{project} press kit",
        "{project} brand assets",
    ],
    "developer_docs": [
        "{project} developer documentation",
        "{project} developer guide",
        "{project} developer SDK",
    ],
    "api_docs": [
        "{project} API documentation",
        "{project} API reference",
        "{project} API docs",
    ],
    "changelogs": [
        "{project} changelog",
        "{project} release notes",
        "{project} version history",
    ],
    "status_pages": [
        "{project} status page",
        "{project} system status",
        "{project} uptime status",
    ],
    "support_pages": [
        "{project} support",
        "{project} help center",
        "{project} knowledge base",
    ],
    "contact_pages": [
        "{project} contact",
        "{project} contact us",
        "{project} business development contact",
    ],
}


def get_website_queries() -> WebsiteQueries:
    """Return independent website-discovery query lists grouped by category."""

    return {
        category: list(queries)
        for category, queries in WEBSITE_QUERY_CATEGORIES.items()
    }

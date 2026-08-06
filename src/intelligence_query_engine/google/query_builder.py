"""Google search-operator query builder for project intelligence discovery."""

from typing import Final


class GoogleDorkBuilder:
    """Build categorized Google dork queries for a crypto project."""

    _CATEGORY_TEMPLATES: Final[dict[str, tuple[str, ...]]] = {
        "official": (
            'intitle:"{project}"',
            '"{project}" official website',
            'inurl:{slug} "{project}"',
        ),
        "documentation": (
            'site:docs.{slug}.xyz',
            'site:docs.{slug}.org',
            '"{project}" documentation',
        ),
        "github": (
            'site:github.com "{project}"',
            'site:github.com/{slug}',
            'site:github.com "{project}" language:Python',
        ),
        "gitbook": (
            'site:gitbook.io "{project}"',
            'site:{slug}.gitbook.io',
            '"{project}" GitBook',
        ),
        "whitepaper": (
            'filetype:pdf "{project}" whitepaper',
            'filetype:pdf "{project}" litepaper',
            '"{project}" technical paper',
        ),
        "roadmap": (
            '"{project}" roadmap',
            '"{project}" product roadmap',
            '"{project}" development roadmap',
        ),
        "blog": (
            'site:medium.com "{project}"',
            'site:mirror.xyz "{project}"',
            '"{project}" blog',
        ),
        "audits": (
            '"{project}" audit report filetype:pdf',
            '"{project}" smart contract audit',
            'site:github.com "{project}" audit',
        ),
        "governance": (
            '"{project}" governance forum',
            '"{project}" DAO proposal',
            'site:forum.{slug}.xyz "{project}"',
        ),
        "tokenomics": (
            '"{project}" tokenomics',
            '"{project}" token allocation',
            'filetype:pdf "{project}" tokenomics',
        ),
        "careers": (
            '"{project}" careers',
            '"{project}" jobs',
            'site:linkedin.com/jobs "{project}"',
        ),
        "api": (
            '"{project}" API docs',
            '"{project}" API reference',
            'inurl:api "{project}"',
        ),
        "developer": (
            '"{project}" developer docs',
            '"{project}" SDK',
            'site:github.com "{project}" developer',
        ),
        "forum": (
            'site:notion.so "{project}"',
            'site:commonwealth.im "{project}"',
            'site:discourse.org "{project}"',
        ),
        "support": (
            '"{project}" support',
            '"{project}" help center',
            'inurl:support "{project}"',
        ),
        "media": (
            '"{project}" media kit',
            '"{project}" press kit',
            '"{project}" brand assets',
        ),
        "investors": (
            '"{project}" investors',
            '"{project}" funding backers',
            '"{project}" venture capital',
        ),
        "partners": (
            '"{project}" partners',
            '"{project}" integrations',
            '"{project}" strategic partnership',
        ),
        "social": (
            'site:x.com "{project}"',
            'site:twitter.com "{project}"',
            'site:discord.com "{project}"',
        ),
        "news": (
            '"{project}" news',
            '"{project}" announcement',
            'intitle:"{project}" crypto',
        ),
    }

    def __init__(self, project_name: str) -> None:
        """Initialize the builder with a non-empty project name."""

        normalized_name = project_name.strip()
        if not normalized_name:
            raise ValueError("project_name must not be empty")

        self.project_name = normalized_name
        self._project_slug = normalized_name.lower().replace(" ", "-")

    def build(self) -> dict[str, list[str]]:
        """Return categorized Google dorks formatted for the project name."""

        return {
            category: [
                query.format(
                    project=self.project_name,
                    slug=self._project_slug,
                )
                for query in templates
            ]
            for category, templates in self._CATEGORY_TEMPLATES.items()
        }

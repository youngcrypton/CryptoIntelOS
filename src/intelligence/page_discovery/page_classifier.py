from src.intelligence.page_discovery.page_types import (
    PageType,
)


class PageClassifier:
    """
    Classifies pages into intelligence categories.
    """

    def classify(
        self,
        page,
    ):

        url = page.url.lower()

        title = page.title.lower()

        text = page.text.lower()

        content = f"{url} {title} {text}"

        checks = {

            PageType.DOCUMENTATION: [
                "docs",
                "documentation",
                "developer",
                "gitbook",
            ],

            PageType.TOKENOMICS: [
                "tokenomics",
                "allocation",
                "vesting",
                "supply",
            ],

            PageType.ROADMAP: [
                "roadmap",
                "milestone",
            ],

            PageType.TEAM: [
                "team",
                "founder",
                "about",
            ],

            PageType.GITHUB: [
                "github",
            ],

            PageType.BLOG: [
                "blog",
                "news",
                "article",
            ],

            PageType.API: [
                "api",
                "swagger",
            ],

            PageType.ECOSYSTEM: [
                "ecosystem",
                "partners",
            ],

            PageType.GOVERNANCE: [
                "governance",
                "dao",
            ],

            PageType.WHITEPAPER: [
                "whitepaper",
            ],

            PageType.AUDIT: [
                "audit",
            ],

            PageType.SECURITY: [
                "security",
                "bug bounty",
            ],

            PageType.CAREERS: [
                "career",
                "jobs",
            ],

            PageType.STAKING: [
                "staking",
            ],

            PageType.BRIDGE: [
                "bridge",
            ],

            PageType.FAQ: [
                "faq",
            ],

            PageType.LEGAL: [
                "privacy",
                "terms",
                "license",
            ],

        }

        for page_type, keywords in checks.items():

            for keyword in keywords:

                if keyword in content:

                    return page_type

        if page.url.endswith("/"):

            return PageType.HOME

        return PageType.UNKNOWN


page_classifier = PageClassifier()
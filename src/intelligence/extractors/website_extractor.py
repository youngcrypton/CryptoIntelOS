import re

from src.intelligence.extractors.base_extractor import BaseExtractor
from src.intelligence.extractors.website_profile import WebsiteProfile


class WebsiteExtractor(BaseExtractor):
    """
    Extracts structured intelligence from a website page.
    """

    def extract(self, page):

        profile = WebsiteProfile()

        # -----------------------------
        # Basic Information
        # -----------------------------

        profile.url = getattr(page, "url", "")
        profile.title = getattr(page, "title", "")
        profile.description = getattr(page, "description", "")
        profile.language = getattr(page, "language", "")

        # -----------------------------
        # External Links
        # -----------------------------

        links = getattr(page, "external_links", [])

        for link in links:

            lower = link.lower()

            if "github.com" in lower:

                profile.github.append(link)

            elif (
                "gitbook" in lower
                or "docs" in lower
                or "documentation" in lower
            ):

                profile.docs.append(link)

            elif any(
                audit in lower
                for audit in (
                    "certik",
                    "halborn",
                    "trailofbits",
                    "quantstamp",
                    "openzeppelin",
                    "hacken",
                    "code4rena",
                    "sherlock",
                )
            ):

                profile.audits.append(link)

            elif (
                "whitepaper" in lower
                or lower.endswith(".pdf")
            ):

                profile.whitepapers.append(link)

            elif any(
                social in lower
                for social in (
                    "twitter",
                    "x.com",
                    "discord",
                    "telegram",
                    "medium",
                    "youtube",
                )
            ):

                profile.socials.append(link)

        # -----------------------------
        # Website Text
        # -----------------------------

        text = getattr(page, "page_text", "")

        if not text:
            text = getattr(page, "text", "")

        # -----------------------------
        # Users
        # -----------------------------

        match = re.search(
            r"Users\s+([\d,]+)",
            text,
        )

        if match:

            profile.users = int(
                match.group(1).replace(",", "")
            )

        # -----------------------------
        # Daily Volume
        # -----------------------------

        match = re.search(
            r"Daily volume\s+(\$[\d\.A-Za-z]+)",
            text,
        )

        if match:

            profile.daily_volume = match.group(1)

        # -----------------------------
        # Max TPS
        # -----------------------------

        match = re.search(
            r"Max TPS\s+([\d,]+)",
            text,
        )

        if match:

            profile.max_tps = int(
                match.group(1).replace(",", "")
            )

        # -----------------------------
        # Block Time
        # -----------------------------

        match = re.search(
            r"Block time\s+([0-9\.]+\s+\w+)",
            text,
        )

        if match:

            profile.block_time = match.group(1)

        # -----------------------------
        # Native Token
        # -----------------------------

        match = re.search(
            r"through\s+([A-Z]{2,10})",
            text,
        )

        if match:

            profile.token = match.group(1)

        return profile


website_extractor = WebsiteExtractor()
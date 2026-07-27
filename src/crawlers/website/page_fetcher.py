import requests

from src.web_engine.renderer import browser_renderer
from src.crawlers.website.html_quality import html_quality


class PageFetcher:
    """
    Smart webpage downloader.

    Strategy:

    1. Download with requests.
    2. Render with Playwright.
    3. Score both pages.
    4. Keep whichever contains more useful content.
    """

    def __init__(self):

        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/138.0 Safari/537.36"
            )
        }

    def fetch(self, url):

        request_html = ""
        request_status = 0

        # ----------------------------
        # Try normal HTTP request
        # ----------------------------

        try:

            response = requests.get(
                url,
                headers=self.headers,
                timeout=20,
                allow_redirects=True,
            )

            request_status = response.status_code
            request_html = response.text

            print(
                f"✓ Requests downloaded "
                f"{len(request_html):,} characters"
            )

        except Exception as error:

            print("⚠ Requests failed")
            print(error)

        # ----------------------------
        # Try Playwright
        # ----------------------------

        playwright_html = ""

        try:

            playwright_html = browser_renderer.render(url)

            print(
                f"✓ Playwright rendered "
                f"{len(playwright_html):,} characters"
            )

        except Exception as error:

            print("⚠ Playwright failed")
            print(error)

        # ----------------------------
        # Score both
        # ----------------------------

        request_score = html_quality.score(
            request_html
        )

        playwright_score = html_quality.score(
            playwright_html
        )

        print()

        print("========== HTML Quality ==========")

        print(
            f"Requests Score   : {request_score:,}"
        )

        print(
            f"Playwright Score : {playwright_score:,}"
        )

        print()

        # ----------------------------
        # Select best HTML
        # ----------------------------

        if playwright_score > request_score:

            print("✓ Selected Playwright HTML")

            return {
                "html": playwright_html,
                "status_code": 200,
                "source": "Playwright",
                "score": playwright_score,
            }

        print("✓ Selected Requests HTML")

        return {
            "html": request_html,
            "status_code": request_status,
            "source": "Requests",
            "score": request_score,
        }


page_fetcher = PageFetcher()
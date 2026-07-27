from playwright.sync_api import TimeoutError

from src.web_engine.manager import browser_manager


class BrowserRenderer:
    """
    Renders JavaScript websites using Playwright.
    """

    def render(
        self,
        url,
        wait_time=3000,
    ):

        page = browser_manager.new_page()

        try:

            page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=60000,
            )

            page.wait_for_timeout(wait_time)

            html = page.content()

            return html

        except TimeoutError:

            print(f"⚠ Page timeout for {url}")

            try:

                html = page.content()

                return html

            except Exception:

                return None

        finally:

            page.close()


browser_renderer = BrowserRenderer()
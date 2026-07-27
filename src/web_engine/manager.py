from playwright.sync_api import sync_playwright


class BrowserManager:
    """
    Manages a single Playwright browser instance.
    """

    def __init__(self):

        self.playwright = None
        self.browser = None
        self.context = None

    def start(self):

        if self.browser:
            return

        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--no-sandbox",
            ],
        )

        self.context = self.browser.new_context(
            viewport={
                "width": 1600,
                "height": 900,
            },
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/138.0 Safari/537.36"
            ),
            locale="en-US",
        )

        print("✓ Chromium browser started")

    def stop(self):

        if self.context:

            self.context.close()
            self.context = None

        if self.browser:

            self.browser.close()
            self.browser = None

        if self.playwright:

            self.playwright.stop()
            self.playwright = None

        print("✓ Chromium browser stopped")

    def new_page(self):

        if not self.context:
            raise RuntimeError(
                "Browser has not been started."
            )

        page = self.context.new_page()

        page.set_default_navigation_timeout(60000)
        page.set_default_timeout(60000)

        return page


browser_manager = BrowserManager()
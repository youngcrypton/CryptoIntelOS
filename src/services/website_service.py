from src.collectors.websites.collector import website_collector


class WebsiteService:
    """Business logic for website intelligence."""

    def collect(self, url):
        return website_collector.collect(url)


website_service = WebsiteService()
class CrawlerManager:
    """
    Stores every crawler available in the system.
    """

    def __init__(self):

        self._crawlers = []

    def register(self, crawler):

        self._crawlers.append(crawler)

    def get_crawlers(self):

        return self._crawlers


crawler_manager = CrawlerManager()
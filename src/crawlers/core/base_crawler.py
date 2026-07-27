from abc import ABC, abstractmethod


class BaseCrawler(ABC):
    """
    Base class for all crawlers.
    """

    @abstractmethod
    def crawl(self, *args, **kwargs):
        """
        Crawl data from a source.
        """
        raise NotImplementedError
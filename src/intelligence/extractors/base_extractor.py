class BaseExtractor:
    """
    Base class for all intelligence extractors.
    """

    def extract(self, data):
        raise NotImplementedError
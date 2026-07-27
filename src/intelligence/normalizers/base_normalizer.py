class BaseNormalizer:
    """
    Base class for all normalizers.

    Every normalizer converts raw collector objects
    into a standardized dictionary.
    """

    def normalize(self, data):
        raise NotImplementedError(
            "Normalizer must implement normalize()."
        )
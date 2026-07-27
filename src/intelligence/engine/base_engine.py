class BaseEngine:
    """
    Base class for every intelligence engine.

    Every engine must implement the process() method.
    """

    def process(self, project, result):
        raise NotImplementedError(
            "Engine must implement process()."
        )
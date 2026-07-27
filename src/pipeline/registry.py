class ProcessorRegistry:
    """
    Stores every processor available in the system.
    """

    def __init__(self):

        self._processors = []

    def register(self, processor):

        self._processors.append(processor)

    def get_processors(self):

        return self._processors


processor_registry = ProcessorRegistry()
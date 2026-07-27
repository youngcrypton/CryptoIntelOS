from src.pipeline.registry import processor_registry

from src.pipeline.processors.website_processor import website_processor
from src.pipeline.processors.x_processor import x_processor


class IntelligencePipeline:
    """
    Routes collector results to the correct processor.
    """

    def __init__(self):

        # Register every processor here
        processor_registry.register(website_processor)
        processor_registry.register(x_processor)

    def process(self, project, result):

        payload = result.payload

        for processor in processor_registry.get_processors():

            if processor.can_process(payload):
                processor.process(project, result)
                return

        print("✗ No processor available for this collector result.")


pipeline = IntelligencePipeline()
import warnings

from src.platform_sdk import LegacyExecutionAdapter
from src.pipeline.registry import processor_registry

from src.pipeline.processors.website_processor import website_processor
from src.pipeline.processors.x_processor import x_processor


class IntelligencePipeline:
    """
    Routes collector results to the correct processor.
    """

    def __init__(self, runtime_adapter=None):

        warnings.warn(
            "src.pipeline.pipeline is deprecated; use Platform SDK and Runtime",
            DeprecationWarning,
            stacklevel=2,
        )
        self.runtime_adapter = runtime_adapter or LegacyExecutionAdapter()

        # Register every processor here
        processor_registry.register(website_processor)
        processor_registry.register(x_processor)

    def process(self, project, result):

        payload = result.payload

        for processor in processor_registry.get_processors():

            if processor.can_process(payload):
                return self.runtime_adapter.execute_value(
                    result,
                    source=getattr(result, "collector", "legacy-pipeline"),
                    execution_id=f"legacy:{getattr(result, 'project', 'project')}",
                    processor=lambda: processor.process(project, result),
                )

        print("✗ No processor available for this collector result.")


pipeline = IntelligencePipeline()

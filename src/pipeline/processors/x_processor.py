from src.intelligence.core.signal_factory import (
    signal_factory,
)

from src.intelligence.core.intelligence_report import (
    intelligence_report,
)

from src.services.intelligence.x_intelligence_service import (
    x_intelligence_service,
)


class XProcessor:
    """
    Routes X collector results through the
    Intelligence Core before handing them to the
    X Intelligence Service.
    """

    name = "X Processor"

    def can_process(self, payload):

        return hasattr(payload, "followers")

    def process(
        self,
        project,
        result,
    ):

        signal = signal_factory.create(
            project,
            result,
        )

        intelligence_report.display(
            signal,
        )

        x_intelligence_service.process(
            project,
            result,
        )


x_processor = XProcessor()
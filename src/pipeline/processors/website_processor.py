from src.services.intelligence.website_intelligence_service import (
    website_intelligence_service,
)

from src.intelligence.core.signal_factory import (
    signal_factory,
)

from src.intelligence.core.intelligence_report import (
    intelligence_report,
)


class WebsiteProcessor:
    """
    Routes website collector results through the
    Intelligence Core before handing them to the
    Website Intelligence Service.
    """

    name = "Website Processor"

    def can_process(self, payload):

        return hasattr(payload, "html")

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

        website_intelligence_service.process(
            project,
            result,
        )


website_processor = WebsiteProcessor()
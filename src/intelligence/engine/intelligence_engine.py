from src.intelligence.engine.registry import (
    intelligence_registry,
)


class IntelligenceEngine:
    """
    Central intelligence coordinator.

    Routes collector results to the proper
    intelligence service.
    """

    def process(
        self,
        project,
        result,
    ):

        engine = intelligence_registry.get_engine(
            result.collector
        )

        if engine is None:

            print(
                f"⚠ No intelligence engine registered for "
                f"{result.collector}"
            )

            return

        engine.process(
            project,
            result,
        )


intelligence_engine = IntelligenceEngine()
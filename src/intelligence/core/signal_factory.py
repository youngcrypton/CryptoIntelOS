from src.intelligence.core.signal import Signal

from src.intelligence.core.signal_score import (
    signal_score,
)

from src.intelligence.core.signal_classifier import (
    signal_classifier,
)

from src.intelligence.core.confidence_calculator import (
    confidence_calculator,
)


class SignalFactory:
    """
    Creates standardized intelligence signals.
    """

    def create(
        self,
        project,
        result,
    ):

        return Signal(
            project=project.name,
            source=result.collector,
            signal_type=result.signal_type,
            category=signal_classifier.classify(
                result.signal_type
            ),
            severity="Medium",
            confidence=confidence_calculator.calculate(
                result.collector
            ),
            score=signal_score.calculate(
                result.signal_type
            ),
            title=result.title,
            summary=result.summary,
            evidence=result.evidence,
        )


signal_factory = SignalFactory()
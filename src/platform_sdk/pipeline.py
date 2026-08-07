from dataclasses import dataclass, field

from .lifecycle import CANONICAL_LIFECYCLE, LifecycleStage


@dataclass(frozen=True, slots=True)
class IntegrationPipeline:
    stages: tuple[LifecycleStage, ...] = field(default_factory=lambda: CANONICAL_LIFECYCLE)

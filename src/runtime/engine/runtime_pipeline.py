from dataclasses import dataclass
from .pipeline_stage import PipelineStage
@dataclass(frozen=True, slots=True)
class RuntimePipeline:
    stages: tuple[PipelineStage, ...] = ()

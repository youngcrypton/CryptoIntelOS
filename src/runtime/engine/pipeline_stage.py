from enum import StrEnum
class PipelineStage(StrEnum):
    COLLECT="collect"; ANALYZE="analyze"; COMPILE="compile"; RESOLVE="resolve"; CORRELATE="correlate"; ASSESS="assess"; SIGNAL="signal"; MEMORY="memory"

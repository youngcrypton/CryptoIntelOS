from enum import StrEnum


class PipelineStage(StrEnum):
    COLLECT = "collect"
    ANALYZE = "analyze"
    COMPILE = "compile"
    RESOLVE = "resolve"
    GRAPH = "graph"
    CORRELATE = "correlate"
    REASON = "reason"
    ASSESS = "assess"
    SIGNAL = "signal"
    MEMORY = "memory"
    AUTOMATE = "automate"
    DISTRIBUTE = "distribute"

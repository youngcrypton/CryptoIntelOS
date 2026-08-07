from enum import StrEnum


class LifecycleStage(StrEnum):
    INITIALIZE = "initialize"
    COLLECT = "collect"
    TRANSLATE = "translate"
    EXECUTE = "execute"
    SHUTDOWN = "shutdown"


CANONICAL_LIFECYCLE: tuple[LifecycleStage, ...] = tuple(LifecycleStage)

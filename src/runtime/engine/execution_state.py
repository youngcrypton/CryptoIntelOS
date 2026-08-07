from enum import StrEnum
class ExecutionState(StrEnum):
    CREATED="created"; INITIALIZED="initialized"; RUNNING="running"; PAUSED="paused"; COMPLETED="completed"; FAILED="failed"; CANCELLED="cancelled"

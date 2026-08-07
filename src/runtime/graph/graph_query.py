from dataclasses import dataclass
from enum import StrEnum
class GraphQueryType(StrEnum):
    NODES="nodes"; EDGES="edges"; NEIGHBORS="neighbors"; PATHS="paths"; SUBGRAPH="subgraph"
@dataclass(frozen=True, slots=True)
class GraphQuery:
    query_type: GraphQueryType
    parameters: tuple[tuple[str, str], ...] = ()
    version: str | None = None

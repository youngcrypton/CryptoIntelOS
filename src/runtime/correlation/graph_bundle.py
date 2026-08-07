from dataclasses import dataclass
@dataclass(frozen=True, slots=True)
class GraphBundle:
    nodes: tuple[object, ...] = ()
    edges: tuple[object, ...] = ()
    version: str | None = None

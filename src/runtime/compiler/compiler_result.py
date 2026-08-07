from dataclasses import dataclass
from .compiler_context import CompilerContext
from .graph_projection import GraphProjection
@dataclass(frozen=True, slots=True)
class CompilerResult:
    projection: GraphProjection
    context: CompilerContext | None = None

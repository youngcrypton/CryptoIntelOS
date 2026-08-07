from typing import Protocol, Sequence
from .compiler_context import CompilerContext
from .compiler_result import CompilerResult
class Compiler(Protocol):
    def compile(self, objects: Sequence[object], context: CompilerContext) -> CompilerResult: ...

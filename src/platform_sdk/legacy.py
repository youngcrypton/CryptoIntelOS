"""Deprecated orchestration adapters redirected through the canonical Runtime."""

import hashlib
import warnings
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, Callable

from src.core_intelligence.models import Observation
from src.runtime.engine import ExecutionContext
from src.runtime.synchronous import SynchronousRuntime, SynchronousRuntimeResult

from .runtime import execute_synchronously


@dataclass(frozen=True, slots=True)
class LegacyExecutionResult:
    """Preserve a legacy return value alongside its canonical Runtime result."""

    value: Any
    runtime: SynchronousRuntimeResult


class LegacyExecutionAdapter:
    """Compatibility gateway for obsolete scheduler, pipeline, and collector paths."""

    def __init__(self, runtime: SynchronousRuntime | None = None) -> None:
        self.runtime = runtime or SynchronousRuntime()

    def execute_collector(
        self,
        collector: object,
        *,
        project: object | None = None,
        execution_id: str | None = None,
    ) -> LegacyExecutionResult:
        warnings.warn(
            "collector orchestration is deprecated; migrate to Platform SDK canonical adapters",
            DeprecationWarning,
            stacklevel=2,
        )
        collect = getattr(collector, "collect", None)
        value = collect(project) if project is not None else getattr(collector, "execute")()
        return self.execute_value(
            value,
            source=getattr(collector, "name", type(collector).__name__),
            execution_id=execution_id,
        )

    def execute_value(
        self,
        value: object,
        *,
        source: str,
        execution_id: str | None = None,
        processor: Callable[[], object] | None = None,
    ) -> LegacyExecutionResult:
        warnings.warn(
            "legacy pipeline orchestration is deprecated; use canonical Runtime contracts",
            DeprecationWarning,
            stacklevel=2,
        )
        if processor is not None:
            processor()
        now = datetime.now(UTC)
        identifier = execution_id or f"legacy:{source.casefold().replace(' ', '-')}"
        payload = {
            "legacy_type": type(value).__name__,
            "source": source,
            "summary": str(getattr(value, "summary", "")),
            "signal_type": str(getattr(value, "signal_type", "")),
            "project": str(getattr(value, "project", "")),
        }
        observation = Observation(
            identifier,
            "legacy_compatibility",
            source,
            "1",
            now,
            now,
            "platform-sdk-legacy-adapter",
            hashlib.sha256(repr(payload).encode()).hexdigest(),
            payload,
        )
        context = ExecutionContext(
            identifier,
            "1.0",
            now,
            (("legacy_type", type(value).__name__), ("source", source)),
        )
        runtime = execute_synchronously(
            self.runtime, (observation, (), (), (), ()), context
        )
        return LegacyExecutionResult(value, runtime)

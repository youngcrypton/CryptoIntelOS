from __future__ import annotations
import time
from dataclasses import dataclass
from typing import Any, Callable, Protocol

class Transport(Protocol):
    def request(self, operation: str, **kwargs: Any) -> Any: ...
@dataclass(frozen=True, slots=True)
class RetryConfig:
    attempts: int = 3; base_seconds: float = 0.01
class RetryTransport:
    def __init__(self, transport: Transport, config: RetryConfig = RetryConfig(), sleeper: Callable[[float], None] = time.sleep): self.transport=transport; self.config=config; self.sleeper=sleeper
    def request(self, operation: str, **kwargs: Any) -> Any:
        error=None
        for attempt in range(1, self.config.attempts + 1):
            try: return self.transport.request(operation, **kwargs)
            except Exception as exc:
                error=exc
                if attempt < self.config.attempts: self.sleeper(self.config.base_seconds * (2 ** (attempt - 1)))
        raise error
class HttpTransport(RetryTransport): pass
class JsonRpcTransport(RetryTransport):
    def call(self, operation: str, **kwargs: Any) -> Any: return self.request(operation, **kwargs)

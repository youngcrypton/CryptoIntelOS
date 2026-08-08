"""Typed bridge from adapted canonical objects to existing SDK/Runtime contracts."""
from dataclasses import dataclass
from src.core_intelligence.models import Observation, Evidence, Finding, Assessment, Signal
from src.platform_sdk.runtime import CanonicalOutput
from src.providers.adapters import AdapterResult
class ProviderRuntimeProjectionError(TypeError): pass
@dataclass(frozen=True, slots=True)
class ProviderRuntimeProjection:
    def project(self, result: AdapterResult) -> CanonicalOutput:
        observations = tuple(item for item in result.objects if isinstance(item, Observation))
        if len(observations) != 1: raise ProviderRuntimeProjectionError("provider adapter must produce exactly one Observation")
        return (observations[0], tuple(item for item in result.objects if isinstance(item, Evidence)), tuple(item for item in result.objects if isinstance(item, Finding)), tuple(item for item in result.objects if isinstance(item, Assessment)), tuple(item for item in result.objects if isinstance(item, Signal)))

"""Abstract contracts for canonical intelligence components."""

from abc import ABC, abstractmethod
from collections.abc import Mapping, Sequence

from ..models import Assessment, Entity, Evidence, Finding, JsonValue, Observation, Signal
from .context import ExecutionContext


ComponentMetadata = Mapping[str, JsonValue]


class Collector(ABC):
    """Collect observations from an external source."""

    @abstractmethod
    def collect(self, context: ExecutionContext) -> Sequence[Observation]:
        """Collect immutable observations."""

    @abstractmethod
    def validate_source(self) -> bool:
        """Return whether the configured external source is available and valid."""

    @abstractmethod
    def collector_metadata(self) -> ComponentMetadata:
        """Describe this collector and its versioned capabilities."""


class Analyzer(ABC):
    """Transform observations into normalized evidence."""

    @abstractmethod
    def analyze(
        self, observations: Sequence[Observation], context: ExecutionContext
    ) -> Sequence[Evidence]:
        """Analyze observations without accessing external services."""

    @abstractmethod
    def supported_entity_types(self) -> Sequence[str]:
        """Return entity types understood by this analyzer."""

    @abstractmethod
    def supported_sources(self) -> Sequence[str]:
        """Return observation sources understood by this analyzer."""

    @abstractmethod
    def analyzer_metadata(self) -> ComponentMetadata:
        """Describe this analyzer and its versioned capabilities."""


class Resolver(ABC):
    """Resolve observations and evidence into entities and findings."""

    @abstractmethod
    def resolve_entity(
        self,
        observations: Sequence[Observation],
        evidence: Sequence[Evidence],
        context: ExecutionContext,
    ) -> Entity:
        """Resolve source records to one canonical entity."""

    @abstractmethod
    def merge_evidence(
        self, evidence: Sequence[Evidence], context: ExecutionContext
    ) -> Sequence[Evidence]:
        """Return a normalized, merged evidence collection."""

    @abstractmethod
    def produce_findings(
        self, entity: Entity, evidence: Sequence[Evidence], context: ExecutionContext
    ) -> Sequence[Finding]:
        """Produce interpretations from evidence associated with an entity."""

    @abstractmethod
    def resolver_metadata(self) -> ComponentMetadata:
        """Describe this resolver and its versioned capabilities."""


class Scorer(ABC):
    """Transform findings into versioned assessments."""

    @abstractmethod
    def score(
        self, findings: Sequence[Finding], context: ExecutionContext
    ) -> Sequence[Assessment]:
        """Score findings according to the component's declared policy."""

    @abstractmethod
    def scoring_policy(self) -> ComponentMetadata:
        """Identify the scoring policy and version used by this scorer."""

    @abstractmethod
    def scorer_metadata(self) -> ComponentMetadata:
        """Describe this scorer and its versioned capabilities."""


class SignalGenerator(ABC):
    """Transform assessments into explainable, actionable signals."""

    @abstractmethod
    def generate(
        self, assessments: Sequence[Assessment], context: ExecutionContext
    ) -> Sequence[Signal]:
        """Generate signals without performing scoring."""

    @abstractmethod
    def supported_signal_types(self) -> Sequence[str]:
        """Return signal types this generator can produce."""

    @abstractmethod
    def signal_metadata(self) -> ComponentMetadata:
        """Describe this generator and its versioned capabilities."""


class Correlator(ABC):
    """Correlate normalized evidence across intelligence sources."""

    @abstractmethod
    def correlate(
        self, evidence: Sequence[Evidence], context: ExecutionContext
    ) -> Sequence[Evidence]:
        """Return evidence resulting from cross-source correlation."""

    @abstractmethod
    def supported_sources(self) -> Sequence[str]:
        """Return sources this correlator can combine."""

    @abstractmethod
    def correlation_metadata(self) -> ComponentMetadata:
        """Describe this correlator and its versioned capabilities."""

import hashlib
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import TextIO

from src.blockchain_platform.adapters import AdapterContext, BlockchainAdapter, BlockchainProvider
from src.core_intelligence.models import Assessment, Evidence, Finding, Observation, Signal
from src.platform_sdk import RuntimeFacade, execute_synchronously
from src.runtime.engine import ExecutionContext, ExecutionResult
from src.runtime.synchronous import SynchronousRuntime, SynchronousRuntimeResult
from src.wallet_intelligence import WalletClassificationEngine, WalletDiscovery, WalletRuntimeIntegration
from src.wallet_intelligence.classification_result import ClassificationResult

from .scoring_strategy import DeterministicScoringStrategy, Metrics, ScoringStrategy
from .whale_assessment import WhaleAssessment
from .whale_category import WhaleCategory
from .whale_evidence import WhaleEvidence
from .whale_profile import WhaleProfile


@dataclass(frozen=True, slots=True)
class WhaleIntelligenceResult:
    profile: WhaleProfile
    assessments: tuple[WhaleAssessment, ...]
    canonical: tuple[Observation, tuple[Evidence, ...], tuple[Finding, ...], tuple[Assessment, ...], tuple[Signal, ...]]


@dataclass(frozen=True, slots=True)
class WalletIntelligenceExecutionResult:
    intelligence: WhaleIntelligenceResult
    runtime: SynchronousRuntimeResult
    console_summary: str


class WhaleIntelligenceEngine:
    def __init__(self, strategy: ScoringStrategy | None = None) -> None:
        self.strategy = strategy or DeterministicScoringStrategy()

    def analyze(self, classified: ClassificationResult, metrics: Metrics) -> WhaleIntelligenceResult:
        classifications = tuple(label.label_type for label in classified.labels)
        scores = self.strategy.score(classifications, metrics)
        wallet_id = classified.profile.wallet.wallet_id
        evidence = tuple(WhaleEvidence(f"whale:evidence:{wallet_id}:{name}", name, value, f"Explicit {name} metric supplied") for name, value in metrics)
        score_items = (("capital", scores.capital.value), ("behavior", scores.behavior.value), ("influence", scores.influence.value), ("network", scores.network.value), ("historical", scores.historical.value), ("cross_chain", scores.cross_chain.value))
        assessments = tuple(WhaleAssessment(name, value, scores.confidence.value / 100, tuple(item.evidence_id for item in evidence if item.metric == name), f"{name} scored independently") for name, value in score_items)
        categories = self._categories(classifications, dict(metrics))
        profile = WhaleProfile(
            f"whale:{wallet_id}", (wallet_id,), classifications, categories,
            self._metric_group(metrics, "capital"), self._metric_group(metrics, "behavior"),
            self._metric_group(metrics, "influence"), self._metric_group(metrics, "network"),
            self._metric_group(metrics, "historical"), self._metric_group(metrics, "cross_chain"),
            scores, scores.confidence.value / 100, evidence,
        )
        return WhaleIntelligenceResult(profile, assessments, self._canonical(profile, assessments))

    @staticmethod
    def _metric_group(metrics: Metrics, prefix: str) -> Metrics:
        return tuple(item for item in metrics if item[0] == prefix or item[0].startswith(f"{prefix}."))

    @staticmethod
    def _categories(classifications, metrics) -> tuple[WhaleCategory, ...]:
        mapping = {"vc": WhaleCategory.VC, "smart_money": WhaleCategory.SMART_MONEY, "foundation": WhaleCategory.FOUNDATION, "treasury": WhaleCategory.TREASURY, "exchange": WhaleCategory.EXCHANGE, "market_maker": WhaleCategory.MARKET_MAKER}
        result = [mapping[item.value] for item in classifications if item.value in mapping]
        if metrics.get("behavior", 0) >= 80 and metrics.get("historical", 0) >= 80:
            result.append(WhaleCategory.HIGH_CONVICTION)
        if metrics.get("capital", 0) >= 50 and not result:
            result.append(WhaleCategory.EMERGING_WHALE)
        return tuple(dict.fromkeys(result))

    @staticmethod
    def _canonical(profile: WhaleProfile, assessments: tuple[WhaleAssessment, ...]):
        now = datetime.now(UTC)
        checksum = hashlib.sha256(repr(profile).encode()).hexdigest()
        observation = Observation(profile.canonical_identifier, "wallet", profile.wallet_references[0], "whale-intelligence", now, now, "0.5.0", checksum, {"categories": tuple(item.value for item in profile.categories), "confidence": profile.confidence})
        evidence = tuple(Evidence(item.evidence_id, profile.canonical_identifier, observation.observation_id, f"whale.{item.metric}", item.value, profile.confidence, item.source, {"explanation": item.explanation}, now) for item in profile.supporting_evidence)
        evidence_ids = tuple(item.evidence_id for item in evidence)
        finding = Finding(f"whale:finding:{checksum[:16]}", profile.canonical_identifier, "Whale Intelligence Profile", profile.confidence, evidence_ids, "Independent whale intelligence dimensions were evaluated deterministically", now)
        canonical_assessments = tuple(Assessment(f"whale:assessment:{profile.wallet_references[0]}:{item.dimension}", profile.canonical_identifier, f"Whale {item.dimension.title()}", item.score, item.confidence, item.evidence or evidence_ids, "whale-deterministic", "1.0", now) for item in assessments)
        signals = tuple(Signal(f"whale:signal:{profile.wallet_references[0]}:{category.value}", profile.canonical_identifier, category.value, "medium", profile.confidence, "Monitor future canonical wallet observations", f"Wallet classified as {category.value}", evidence_ids, now) for category in profile.categories)
        return observation, evidence, (finding,), canonical_assessments, signals


class WalletIntelligenceVerticalSlice:
    def __init__(self, *, discovery=None, classification=None, intelligence=None, runtime=None) -> None:
        self.discovery = discovery or WalletDiscovery()
        self.classification = classification or WalletClassificationEngine()
        self.intelligence = intelligence or WhaleIntelligenceEngine()
        self.runtime = runtime or SynchronousRuntime()

    def run(self, provider: BlockchainProvider, adapter: BlockchainAdapter, identifier: str, context: AdapterContext, metrics: Metrics, *, metadata=None, output: TextIO | None = None) -> WalletIntelligenceExecutionResult:
        adapted = adapter.adapt(provider, identifier, context)
        discovered = self.discovery.discover(adapted, metadata)
        classified = self.classification.classify(discovered, metadata)
        if not classified:
            raise ValueError("provider and adapter produced no wallets")
        intelligence = self.intelligence.analyze(classified[0], metrics)
        captured = []

        def execute(canonical, execution_context):
            result = execute_synchronously(self.runtime, canonical, execution_context)
            captured.append(result)
            return result.execution

        execution_context = ExecutionContext(f"wallet:{identifier}", "1.0", datetime.now(UTC))
        WalletRuntimeIntegration(RuntimeFacade(execute)).integrate(intelligence.canonical, execution_context)
        runtime = captured[0]
        summary = self._summary(provider, adapter, intelligence, runtime)
        print(summary, file=output or sys.stdout)
        return WalletIntelligenceExecutionResult(intelligence, runtime, summary)

    @staticmethod
    def _summary(provider, adapter, intelligence, runtime) -> str:
        return "\n".join((f"Provider: {provider.metadata().provider_id}", f"Adapter: {adapter.adapter_id}", f"Canonical Wallet: {intelligence.profile.wallet_references[0]}", "Wallet Discovery: completed", "Wallet Classification: completed", f"Whale Intelligence: {len(intelligence.profile.categories)} categories", f"Compiler Executed: {len(runtime.compilation.projection.nodes)} nodes", f"Knowledge Graph Updated: {len(runtime.graph.nodes)} nodes", f"Correlation Completed: {runtime.correlation.status.value}", f"Reasoning Completed: {runtime.reasoning.status.value}", f"Automation Plan Created: {len(runtime.automation.actions)} actions", f"Distribution Plan Created: {len(runtime.distribution.requests)} requests", f"Execution Successful: {runtime.execution.final_state.value}"))

from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import NAMESPACE_URL, uuid5

from src.core_intelligence.models import Assessment, Evidence, Finding, Observation, Signal

from .automation import (
    AutomationAction,
    AutomationContext,
    AutomationEngine,
    AutomationPlan,
    AutomationPolicy,
    AutomationPriority,
)
from .compiler import CompilerContext, CompilerResult, GraphProjection as CompilerProjection, NodeIR, ProvenanceIR
from .correlation import (
    Correlation,
    CorrelationContext,
    CorrelationEngine,
    CorrelationResult,
    CorrelationStatus,
    CorrelationType,
)
from .distribution import (
    DistributionChannel,
    DistributionContext,
    DistributionEngine,
    DistributionMessage,
    DistributionPlan,
    DistributionPriority,
    DistributionRequest,
    DistributionResult,
    DistributionStatus,
    DistributionTarget,
)
from .engine import ExecutionEngine, ExecutionResult, RuntimePipeline
from .engine.pipeline_stage import PipelineStage
from .graph import GraphNode, GraphProjection
from .reasoning import (
    ReasoningChain,
    ReasoningConfidence,
    ReasoningContext,
    ReasoningEngine,
    ReasoningExplanation,
    ReasoningRequest,
    ReasoningResult,
    ReasoningStatus,
    ReasoningStep,
    ReasoningType,
)


CanonicalObject = Observation | Evidence | Finding | Assessment | Signal


@dataclass(frozen=True, slots=True)
class SynchronousRuntimeResult:
    compilation: CompilerResult
    graph: GraphProjection
    correlation: CorrelationResult
    reasoning: ReasoningResult
    automation: AutomationPlan
    distribution: DistributionPlan
    distribution_results: tuple[DistributionResult, ...]
    execution: ExecutionResult


class CanonicalCompiler:
    def compile(self, objects: tuple[CanonicalObject, ...], context: CompilerContext) -> CompilerResult:
        nodes = tuple(
            NodeIR(
                node_id=uuid5(NAMESPACE_URL, self._identifier(item)),
                entity_reference=getattr(item, "entity_reference", self._identifier(item)),
                node_type=type(item).__name__.lower(),
                provenance=(ProvenanceIR(context.source, self._identifier(item), context.timestamp),),
                timestamp=getattr(item, "timestamp", context.timestamp),
            )
            for item in objects
        )
        return CompilerResult(CompilerProjection(nodes=nodes), context)

    @staticmethod
    def _identifier(value: CanonicalObject) -> str:
        for name in ("observation_id", "evidence_id", "finding_id", "assessment_id", "signal_id"):
            identifier = getattr(value, name, None)
            if identifier:
                return str(identifier)
        raise ValueError(f"canonical object has no identifier: {type(value).__name__}")


class DeterministicCorrelationStrategy:
    def correlate(self, objects: tuple[object, ...], context: CorrelationContext) -> CorrelationResult:
        correlation = Correlation(
            correlation_type=CorrelationType.PROJECT_MOMENTUM,
            participating_evidence=objects,
            confidence=1.0,
            explanation="Canonical GitHub intelligence belongs to one execution.",
            provenance=context,
            timestamp=context.timestamp,
        )
        return CorrelationResult(CorrelationStatus.CONFIRMED, (correlation,))


class DeterministicReasoningStrategy:
    def execute(self, request: ReasoningRequest, context: ReasoningContext) -> ReasoningResult:
        explanation = ReasoningExplanation(
            "Canonical evidence, findings, assessments, and signals were processed deterministically.",
            tuple(str(item) for item in request.metadata),
            limitations=("No external AI provider participated.",),
        )
        step = ReasoningStep("runtime-summary", "Summarize canonical runtime inputs", output=explanation.summary, explanation=explanation)
        return ReasoningResult(
            ReasoningStatus.COMPLETED,
            conclusion=explanation.summary,
            chain=ReasoningChain((step,), "deterministic"),
            confidence=ReasoningConfidence(1.0, "deterministic_runtime"),
            explanation=explanation,
        )


class SingleStrategyRegistry:
    def __init__(self, strategy: object) -> None:
        self.strategy = strategy

    def register(self, name: str, strategy: object) -> None:
        self.strategy = strategy

    def get(self, name: str) -> object:
        return self.strategy


class WatchAutomationStrategy:
    def decide(self, context: AutomationContext, policy: AutomationPolicy) -> tuple[AutomationPlan, ...]:
        action = AutomationAction("watch", {"object_count": len(context.runtime_objects)}, "Continue monitoring")
        return (
            AutomationPlan(
                actions=(action,),
                priority=policy.default_priority,
                explanation="Canonical signal produced a monitoring action plan.",
                supporting_reasoning=("deterministic reasoning completed",),
            ),
        )


class PlanningDistributionStrategy:
    def distribute(self, plan: DistributionPlan, context: DistributionContext, registry: object) -> tuple[DistributionResult, ...]:
        return tuple(
            DistributionResult(request.request_id, DistributionStatus.ACCEPTED, detail="Planned for console presentation")
            for request in plan.requests
        )


class SynchronousRuntime:
    """Source-agnostic synchronous orchestration for canonical Runtime objects."""

    def execute(self, execution_id: str, objects: tuple[CanonicalObject, ...]) -> SynchronousRuntimeResult:
        timestamp = datetime.now(UTC)
        compiler = CanonicalCompiler()
        compilation = compiler.compile(objects, CompilerContext(execution_id, "canonical", timestamp))
        graph = GraphProjection(
            nodes=tuple(
                GraphNode(node.node_id, node.entity_reference, (node.node_type,), provenance=node.provenance, timestamp=node.timestamp)
                for node in compilation.projection.nodes
            )
        )
        correlation = CorrelationEngine().correlate(
            DeterministicCorrelationStrategy(),
            objects,
            CorrelationContext(execution_id, "canonical", timestamp),
        )
        reasoning = ReasoningEngine().reason(
            DeterministicReasoningStrategy(),
            ReasoningRequest(reasoning_type=ReasoningType.PROJECT_ASSESSMENT, inputs=objects),
            ReasoningContext(execution_id, "canonical", timestamp),
        )
        registry = SingleStrategyRegistry(WatchAutomationStrategy())
        automation_result = AutomationEngine(registry).decide(
            AutomationContext(objects),
            AutomationPolicy("vertical-slice", default_priority=AutomationPriority.NORMAL),
            "watch",
        )
        automation = automation_result.plans[0]
        message = DistributionMessage(automation.plan_id, body=automation.explanation)
        target = DistributionTarget("console", DistributionChannel("console", "console"))
        request = DistributionRequest(automation.plan_id, message, target, DistributionPriority.NORMAL)
        distribution = DistributionPlan(requests=(request,), strategy_name="console")
        distribution_results = DistributionEngine(SingleStrategyRegistry(object())).distribute(
            distribution,
            DistributionContext(correlation_id=execution_id),
            PlanningDistributionStrategy(),
        )
        pipeline = RuntimePipeline(tuple(PipelineStage))
        engine = ExecutionEngine()
        execution = engine.execute(engine.initialize(execution_id, pipeline), pipeline)
        return SynchronousRuntimeResult(
            compilation,
            graph,
            correlation,
            reasoning,
            automation,
            distribution,
            distribution_results,
            execution,
        )

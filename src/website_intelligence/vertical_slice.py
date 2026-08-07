import sys
from dataclasses import dataclass
from typing import TextIO

from src.core_intelligence.models import Observation
from src.platform_sdk import RuntimeFacade
from src.platform_sdk.runtime import CanonicalOutput
from src.runtime.engine import ExecutionContext, ExecutionResult, ExecutionState
from src.runtime.synchronous import SynchronousRuntime, SynchronousRuntimeResult

from .analysis import AnalysisOutput, WebsiteAnalysisEngine
from .discovery import DiscoveryResult, WebsiteDiscoveryEngine
from .models import Document, Link, Page, Website
from .runtime import WebsiteRuntimeIntegration
from .signals import SignalOutput, WebsiteSignalEngine


@dataclass(frozen=True, slots=True)
class WebsiteVerticalSliceResult:
    discoveries: tuple[DiscoveryResult, ...]
    canonical: SignalOutput
    runtime: SynchronousRuntimeResult
    console_summary: str


class WebsiteVerticalSlice:
    """Run Website resources through the complete synchronous platform."""

    def __init__(
        self,
        *,
        discovery: WebsiteDiscoveryEngine | None = None,
        analysis: WebsiteAnalysisEngine | None = None,
        signals: WebsiteSignalEngine | None = None,
        runtime: SynchronousRuntime | None = None,
    ) -> None:
        self.discovery = discovery or WebsiteDiscoveryEngine()
        self.analysis = analysis or WebsiteAnalysisEngine()
        self.signals = signals or WebsiteSignalEngine()
        self.runtime = runtime or SynchronousRuntime()

    def run(
        self,
        website: Website,
        *,
        pages: tuple[Page, ...] = (),
        documents: tuple[Document, ...] = (),
        links: tuple[Link, ...] = (),
        output: TextIO | None = None,
    ) -> WebsiteVerticalSliceResult:
        discoveries = (
            self.discovery.discover_website(website),
            *(self.discovery.discover_page(page) for page in pages),
            *(self.discovery.discover_document(document) for document in documents),
            *(self.discovery.discover_link(link, base_url=website.url) for link in links),
        )
        batch_observation = self._batch_observation(discoveries)
        analyses = tuple(self.analysis.analyze(item.observation) for item in discoveries)
        combined_analysis = AnalysisOutput(
            batch_observation,
            tuple(evidence for result in analyses for evidence in result.evidence),
            tuple(finding for result in analyses for finding in result.findings),
            tuple(assessment for result in analyses for assessment in result.assessments),
        )
        generated = tuple(self.signals.generate(result) for result in analyses)
        canonical = SignalOutput(
            combined_analysis.observation,
            combined_analysis.evidence,
            combined_analysis.findings,
            combined_analysis.assessments,
            tuple(signal for result in generated for signal in result.signals),
        )
        runtime = self._execute_runtime(canonical, website.website_id)
        summary = self._summary(website, pages, documents, discoveries, canonical, runtime)
        print(summary, file=output or sys.stdout)
        return WebsiteVerticalSliceResult(discoveries, canonical, runtime, summary)

    def _batch_observation(self, discoveries: tuple[DiscoveryResult, ...]) -> Observation:
        captured: list[CanonicalOutput] = []

        def capture(canonical: CanonicalOutput, context: ExecutionContext) -> ExecutionResult:
            captured.append(canonical)
            return ExecutionResult(context.execution_id, ExecutionState.COMPLETED)

        context = ExecutionContext(
            f"website:discovery:{discoveries[0].observation.source_identifier}",
            "1.0",
            discoveries[0].observation.collected_at,
        )
        self.discovery.enter_runtime(
            discoveries,
            WebsiteRuntimeIntegration(RuntimeFacade(capture)),
            context,
        )
        return captured[0][0]

    def _execute_runtime(
        self, canonical: SignalOutput, website_id: str
    ) -> SynchronousRuntimeResult:
        captured: list[SynchronousRuntimeResult] = []

        def execute(canonical_output: CanonicalOutput, context: ExecutionContext) -> ExecutionResult:
            objects = (
                canonical_output[0],
                *canonical_output[1],
                *canonical_output[2],
                *canonical_output[3],
                *canonical_output[4],
            )
            result = self.runtime.execute(context.execution_id, objects)
            captured.append(result)
            return result.execution

        context = ExecutionContext(
            f"website:{website_id}", "1.0", canonical.observation.observed_at
        )
        self.signals.enter_runtime(
            canonical,
            WebsiteRuntimeIntegration(RuntimeFacade(execute)),
            context,
        )
        return captured[0]

    @staticmethod
    def _summary(
        website: Website,
        pages: tuple[Page, ...],
        documents: tuple[Document, ...],
        discoveries: tuple[DiscoveryResult, ...],
        canonical: SignalOutput,
        runtime: SynchronousRuntimeResult,
    ) -> str:
        return "\n".join(
            (
                f"Website Processed: {website.url}",
                f"Pages Discovered: {len(pages)}",
                f"Documents Discovered: {len(documents)}",
                f"Observations Created: {len(discoveries)}",
                f"Evidence Generated: {len(canonical.evidence)}",
                f"Findings Generated: {len(canonical.findings)}",
                f"Assessments Produced: {len(canonical.assessments)}",
                f"Signals Generated: {len(canonical.signals)}",
                f"Compiler Executed: {len(runtime.compilation.projection.nodes)} nodes",
                f"Knowledge Graph Updated: {len(runtime.graph.nodes)} nodes",
                f"Correlation Completed: {runtime.correlation.status.value}",
                f"Reasoning Completed: {runtime.reasoning.status.value}",
                f"Automation Plan Created: {len(runtime.automation.actions)} actions",
                f"Distribution Plan Created: {len(runtime.distribution.requests)} requests",
                f"Execution Successful: {runtime.execution.final_state.value}",
            )
        )

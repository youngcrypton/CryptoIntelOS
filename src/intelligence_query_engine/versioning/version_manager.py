"""Version snapshots and structural change tracking for the IQE."""

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Literal, Mapping

from intelligence_query_engine.common.documentation_generator import (
    IQEDocumentation,
    IQEDocumentationGenerator,
)
from intelligence_query_engine.common.query_pipeline import ProcessedQueryPlan


ChangeType = Literal[
    "builder_added",
    "builder_removed",
    "category_added",
    "category_removed",
    "knowledge_pack_added",
    "knowledge_pack_removed",
    "query_count_change",
    "breaking_change",
]


@dataclass(frozen=True)
class IQEVersion:
    """Human-readable version metadata for an IQE snapshot."""

    version: str
    description: str
    build_date: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


@dataclass(frozen=True)
class QueryChange:
    """One structural or query-count change between two version snapshots."""

    change_type: ChangeType
    subject: str
    previous_value: int | str | None
    current_value: int | str | None
    breaking_change: bool = False


@dataclass(frozen=True)
class VersionSnapshot:
    """Structural metrics captured for one IQE version."""

    version: IQEVersion
    builder_count: int
    knowledge_pack_count: int
    total_categories: int
    total_queries: int
    supported_sources: list[str]


class IQEVersionManager:
    """Create, compare, and export IQE version snapshots."""

    def create_snapshot(
        self,
        version: IQEVersion,
        query_plan: ProcessedQueryPlan | Mapping[str, list[str]],
        documentation: IQEDocumentation | None = None,
    ) -> VersionSnapshot:
        """Capture query-plan and architecture metrics for one IQE version."""

        documented_iqe = documentation or IQEDocumentationGenerator().generate()
        queries = self._extract_queries(query_plan)
        return VersionSnapshot(
            version=version,
            builder_count=documented_iqe.statistics.builder_count,
            knowledge_pack_count=documented_iqe.total_knowledge_packs,
            total_categories=len(queries),
            total_queries=sum(len(category_queries) for category_queries in queries.values()),
            supported_sources=list(
                documented_iqe.statistics.supported_intelligence_sources
            ),
        )

    def compare_versions(
        self,
        previous: VersionSnapshot,
        current: VersionSnapshot,
    ) -> list[QueryChange]:
        """Return structural changes from a previous snapshot to a current one."""

        changes = [
            *self._count_changes(
                previous.builder_count,
                current.builder_count,
                "builder",
                "builder_added",
                "builder_removed",
            ),
            *self._count_changes(
                previous.knowledge_pack_count,
                current.knowledge_pack_count,
                "knowledge pack",
                "knowledge_pack_added",
                "knowledge_pack_removed",
            ),
            *self._count_changes(
                previous.total_categories,
                current.total_categories,
                "query category",
                "category_added",
                "category_removed",
            ),
        ]
        if previous.total_queries != current.total_queries:
            changes.append(
                QueryChange(
                    change_type="query_count_change",
                    subject="total queries",
                    previous_value=previous.total_queries,
                    current_value=current.total_queries,
                )
            )

        changes.extend(self._source_changes(previous, current))
        return changes

    @staticmethod
    def export_version(snapshot: VersionSnapshot) -> dict[str, object]:
        """Export a snapshot as plain Python data for any future file format."""

        return asdict(snapshot)

    @staticmethod
    def _extract_queries(
        query_plan: ProcessedQueryPlan | Mapping[str, list[str]],
    ) -> Mapping[str, list[str]]:
        """Return the categorized queries from supported plan representations."""

        if isinstance(query_plan, ProcessedQueryPlan):
            return query_plan.processed_queries

        return query_plan

    @staticmethod
    def _count_changes(
        previous_value: int,
        current_value: int,
        subject: str,
        added_type: ChangeType,
        removed_type: ChangeType,
    ) -> list[QueryChange]:
        """Describe additions or removals for one structural count."""

        if previous_value == current_value:
            return []

        removed = current_value < previous_value
        change_type = removed_type if removed else added_type
        changes = [
            QueryChange(
                change_type=change_type,
                subject=subject,
                previous_value=previous_value,
                current_value=current_value,
                breaking_change=removed,
            )
        ]
        if removed:
            changes.append(
                QueryChange(
                    change_type="breaking_change",
                    subject=f"{subject} removal",
                    previous_value=previous_value,
                    current_value=current_value,
                    breaking_change=True,
                )
            )
        return changes

    @staticmethod
    def _source_changes(
        previous: VersionSnapshot,
        current: VersionSnapshot,
    ) -> list[QueryChange]:
        """Describe supported-source additions and removals."""

        changes: list[QueryChange] = []
        for source in sorted(set(current.supported_sources) - set(previous.supported_sources)):
            changes.append(
                QueryChange(
                    change_type="builder_added",
                    subject=f"supported source: {source}",
                    previous_value=None,
                    current_value=source,
                )
            )
        for source in sorted(set(previous.supported_sources) - set(current.supported_sources)):
            changes.append(
                QueryChange(
                    change_type="breaking_change",
                    subject=f"supported source removed: {source}",
                    previous_value=source,
                    current_value=None,
                    breaking_change=True,
                )
            )
        return changes

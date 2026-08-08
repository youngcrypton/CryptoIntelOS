"""Compatibility projections from Unified Intelligence containers to Runtime contracts."""

import hashlib

from src.core_intelligence.models import Assessment, Evidence, Finding, Observation
from src.platform_sdk import CanonicalOutput
from src.runtime.engine import ExecutionContext

from .assessment_fusion.assessment_group import ProjectAssessmentGroup
from .entity_linking.identity_bundle import IdentityBundle
from .evidence_fusion.evidence_bundle import UnifiedEvidenceBundle
from .finding_fusion.finding_group import ProjectFindingGroup


def project_identity_bundle(
    bundle: IdentityBundle, context: ExecutionContext
) -> CanonicalOutput:
    """Represent a legacy identity bundle as a provenance-preserving observation."""

    identifiers = tuple(
        (identifier.identifier_type.value, identifier.value)
        for identifier in (
            *bundle.github_references,
            *bundle.twitter_references,
            *bundle.website_references,
            *bundle.wallet_references,
        )
    )
    payload = {
        "canonical_project_identifier": bundle.canonical_project_identifier,
        "entity_id": str(bundle.project_entity.entity_id),
        "identifiers": identifiers,
        "supporting_evidence": bundle.supporting_evidence,
        "traceability": bundle.traceability,
        "confidence": bundle.confidence.value,
    }
    observation = Observation(
        observation_id=f"identity:{bundle.canonical_project_identifier}",
        source="unified_intelligence",
        source_identifier=bundle.canonical_project_identifier,
        source_version=context.runtime_version,
        collected_at=context.started_at,
        observed_at=context.started_at,
        collector_version="identity-bundle-compatibility",
        checksum=hashlib.sha256(repr(payload).encode()).hexdigest(),
        raw_payload=payload,
    )
    return observation, (), (), (), ()


def project_evidence_bundle(
    bundle: UnifiedEvidenceBundle, context: ExecutionContext
) -> CanonicalOutput:
    observation, _, _, _, _ = project_identity_bundle(bundle.identity, context)
    evidence = tuple(reference.evidence for group in bundle.groups for reference in group.references)
    return observation, evidence, (), (), ()


def project_finding_group(
    group: ProjectFindingGroup, context: ExecutionContext
) -> CanonicalOutput:
    identity = group.findings[0].identity if group.findings else None
    if identity is None:
        raise ValueError("an empty legacy finding group cannot be projected")
    observation, _, _, _, _ = project_identity_bundle(identity, context)
    findings: tuple[Finding, ...] = tuple(
        reference.finding
        for project_finding in group.findings
        for reference in project_finding.supporting_findings
    )
    return observation, (), findings, (), ()


def project_assessment_group(
    group: ProjectAssessmentGroup, context: ExecutionContext
) -> CanonicalOutput:
    identity = group.assessments[0].identity if group.assessments else None
    if identity is None:
        raise ValueError("an empty legacy assessment group cannot be projected")
    observation, _, _, _, _ = project_identity_bundle(identity, context)
    assessments: tuple[Assessment, ...] = tuple(
        reference.assessment
        for project_assessment in group.assessments
        for reference in project_assessment.supporting_assessments
    )
    return observation, (), (), assessments, ()

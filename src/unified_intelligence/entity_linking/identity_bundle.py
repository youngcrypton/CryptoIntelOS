from dataclasses import dataclass

from src.core_intelligence.identity import Entity, Identifier

from .confidence import LinkingConfidence


@dataclass(frozen=True, slots=True)
class IdentityBundle:
    canonical_project_identifier: str
    project_entity: Entity
    github_references: tuple[Identifier, ...] = ()
    twitter_references: tuple[Identifier, ...] = ()
    website_references: tuple[Identifier, ...] = ()
    wallet_references: tuple[Identifier, ...] = ()
    supporting_evidence: tuple[str, ...] = ()
    confidence: LinkingConfidence = LinkingConfidence(0.0, "no deterministic links")
    traceability: tuple[tuple[str, str], ...] = ()

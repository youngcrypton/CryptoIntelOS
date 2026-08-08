from uuid import NAMESPACE_URL, uuid5

from src.core_intelligence.identity import Entity, EntityType, Identifier, IdentifierType, Identity

from .confidence import LinkingConfidence
from .entity_candidate import EntityCandidate
from .entity_match import EntityMatch
from .identity_bundle import IdentityBundle
from .linking_context import LinkingContext
from .linking_result import LinkingResult


class DeterministicEntityResolution:
    """Resolve candidates using exact canonical identifiers only."""

    strategy_id = "deterministic-identity-v1"

    def link(self, candidates: tuple[EntityCandidate, ...], context: LinkingContext) -> LinkingResult:
        if not candidates:
            raise ValueError("at least one entity candidate is required")
        base = candidates[0]
        matches = []
        linked = [base]
        for candidate in candidates[1:]:
            shared = tuple(sorted({left.value for left in base.identifiers} & {right.value for right in candidate.identifiers}))
            same_name = bool(base.canonical_name and base.canonical_name.casefold() == candidate.canonical_name.casefold())
            if shared or same_name:
                evidence = shared or (f"canonical_name:{base.canonical_name}",)
                confidence = LinkingConfidence(1.0 if shared else 0.9, "exact canonical identifier match" if shared else "exact canonical name match")
                matches.append(EntityMatch(base, candidate, evidence, confidence, confidence.rationale))
                linked.append(candidate)
        identifiers = tuple(identifier for candidate in linked for identifier in candidate.identifiers)
        deduped = tuple(dict((identifier.identifier_type.value + ":" + identifier.value, identifier) for identifier in identifiers).values())
        project_id = f"project:{base.canonical_name.casefold().replace(' ', '-') or base.entity.entity_id}"
        entity = Entity(entity_id=uuid5(NAMESPACE_URL, project_id), entity_type=EntityType.PROJECT, identity=Identity(canonical_name=base.canonical_name, identifiers=deduped))
        all_identifiers = tuple(item for candidate in linked for item in candidate.identifiers)
        bundle = IdentityBundle(project_id, entity, self._identifiers(all_identifiers, (IdentifierType.GITHUB_REPOSITORY_ID,)), self._identifiers(all_identifiers, (IdentifierType.TWITTER_USERNAME,)), self._identifiers(all_identifiers, (IdentifierType.URL, IdentifierType.WEBSITE_DOMAIN)), self._identifiers(all_identifiers, (IdentifierType.WALLET_ADDRESS, IdentifierType.ENS_NAME)), tuple(item for match in matches for item in match.matched_identifiers), LinkingConfidence(1.0 if matches else .5, "exact deterministic links" if matches else "single canonical candidate"), tuple((candidate.source, candidate.entity.entity_id.hex) for candidate in linked))
        return LinkingResult(bundle, tuple(matches))

    @staticmethod
    def _identifiers(identifiers: tuple[Identifier, ...], types: tuple[IdentifierType, ...]) -> tuple[Identifier, ...]:
        return tuple(item for item in identifiers if item.identifier_type in types)

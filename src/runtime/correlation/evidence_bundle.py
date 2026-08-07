from dataclasses import dataclass
@dataclass(frozen=True, slots=True)
class EvidenceBundle:
    evidence: tuple[object, ...] = ()
    references: tuple[str, ...] = ()

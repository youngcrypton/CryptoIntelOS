"""Direction semantics for relationships."""
from enum import StrEnum

class RelationshipDirection(StrEnum):
    DIRECTED = "directed"
    UNDIRECTED = "undirected"
    BIDIRECTIONAL = "bidirectional"

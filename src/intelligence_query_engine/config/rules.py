"""Processing rules for the Intelligence Query Engine."""

from dataclasses import dataclass, fields
from typing import Literal, Mapping


DuplicatePolicy = Literal["remove", "allow", "report"]
OptimizationPolicy = Literal["normalize", "preserve"]
ValidationPolicy = Literal["strict", "report_only"]
ScoringPolicy = Literal["standard", "disabled"]


@dataclass(frozen=True)
class IQERules:
    """Configurable validation, optimization, and scoring constraints."""

    minimum_query_length: int = 1
    maximum_query_length: int = 500
    duplicate_policy: DuplicatePolicy = "remove"
    optimization_policy: OptimizationPolicy = "normalize"
    validation_policy: ValidationPolicy = "strict"
    scoring_policy: ScoringPolicy = "standard"

    @classmethod
    def from_mapping(cls, values: Mapping[str, object]) -> "IQERules":
        """Create rules from a file-format-independent mapping."""

        field_names = {field.name for field in fields(cls)}
        return cls(
            **{
                key: value
                for key, value in values.items()
                if key in field_names
            }
        )

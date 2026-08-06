"""Format-agnostic settings for the Intelligence Query Engine."""

from dataclasses import dataclass, fields
from typing import Mapping


@dataclass(frozen=True)
class IQESettings:
    """Runtime feature settings with conservative production defaults."""

    max_queries_per_category: int = 100
    enable_cache: bool = True
    enable_validation: bool = True
    enable_deduplication: bool = True
    enable_quality_scoring: bool = True
    enable_optimization: bool = True
    enable_documentation: bool = True
    plugin_auto_registration: bool = False
    statistics_enabled: bool = True

    @classmethod
    def from_mapping(cls, values: Mapping[str, object]) -> "IQESettings":
        """Create settings from a file-format-independent mapping.

        Unknown keys are ignored so configuration files can evolve without
        requiring callers to pre-filter their parsed data.
        """

        field_names = {field.name for field in fields(cls)}
        return cls(
            **{
                key: value
                for key, value in values.items()
                if key in field_names
            }
        )

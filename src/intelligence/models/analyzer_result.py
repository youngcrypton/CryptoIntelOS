"""
Analyzer Result

Represents the standardized output produced by any intelligence analyzer.

Every analyzer in CryptoIntel OS returns an AnalyzerResult, allowing
engines to orchestrate analyzers without needing to understand their
internal implementation.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class AnalyzerResult:
    """
    Standardized output from an analyzer.
    """

    analyzer: str

    section: str

    success: bool

    data: Dict[str, Any] = field(default_factory=dict)

    warnings: List[str] = field(default_factory=list)

    errors: List[str] = field(default_factory=list)

    duration: float = 0.0

    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the analyzer result into a serializable dictionary.
        """

        return {
            "analyzer": self.analyzer,
            "section": self.section,
            "success": self.success,
            "data": self.data,
            "warnings": self.warnings,
            "errors": self.errors,
            "duration": self.duration,
            "metadata": self.metadata,
        }
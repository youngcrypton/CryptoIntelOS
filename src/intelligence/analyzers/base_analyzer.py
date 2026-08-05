"""
Base Analyzer

Defines the common interface for every analyzer used throughout
CryptoIntel OS.

Every analyzer is responsible for inspecting one aspect of a project
and returning an AnalyzerResult.

Analyzers never modify the LivingIntelligenceProfile directly.

The Repository Intelligence Engine is responsible for combining
analyzer results into the profile.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict

from src.intelligence.models.analyzer_result import AnalyzerResult


class BaseAnalyzer(ABC):
    """
    Base class for every intelligence analyzer.

    Every analyzer must declare the profile section that it enriches.
    """

    def __init__(self, section: str):
        """
        Parameters
        ----------
        section : str
            Name of the LivingIntelligenceProfile section that this
            analyzer contributes to.

        Examples
        --------
        metadata
        documentation
        technology
        activity
        community
        ecosystem
        security
        """

        self.name = self.__class__.__name__
        self.section = section

    @abstractmethod
    def analyze(
        self,
        repository: Dict[str, Any],
    ) -> AnalyzerResult:
        """
        Analyze a repository and return structured intelligence.

        Parameters
        ----------
        repository : dict
            Repository information collected during discovery.

        Returns
        -------
        AnalyzerResult
            Structured intelligence produced by the analyzer.
        """
        raise NotImplementedError
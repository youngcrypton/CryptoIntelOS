from typing import Protocol

from src.platform_sdk import SourceAdapter

from .models import Blockchain


class BlockchainAdapter(SourceAdapter[Blockchain], Protocol):
    """Translate blockchain infrastructure records into observations."""

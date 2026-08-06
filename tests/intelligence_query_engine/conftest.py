"""Shared fixtures and import setup for Intelligence Query Engine tests."""

from pathlib import Path
import sys

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SOURCE_ROOT = PROJECT_ROOT / "src"

for path in (PROJECT_ROOT, SOURCE_ROOT):
    path_string = str(path)
    if path_string not in sys.path:
        sys.path.insert(0, path_string)


@pytest.fixture
def project_name() -> str:
    """Return a deterministic project name for query-builder tests."""

    return "Monad"

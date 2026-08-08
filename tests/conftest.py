"""
Shared pytest configuration for CryptoIntel OS.
"""

from pathlib import Path

import pytest


@pytest.fixture
def project_root():
    """Return the project root directory."""
    return Path(__file__).resolve().parent.parent


@pytest.fixture
def sample_project():
    """Example project data used by tests."""
    return {
        "id": 1,
        "name": "Bitcoin",
        "symbol": "BTC",
        "website": "https://bitcoin.org",
    }


@pytest.fixture
def sample_website():
    """Example website snapshot."""
    return {
        "url": "https://bitcoin.org",
        "status": 200,
        "content": "<html><body>Hello</body></html>",
    }
from pathlib import Path


def pytest_ignore_collect(collection_path: Path, config) -> bool:
    """Exclude the legacy executable pipeline smoke script from collection.

    It intentionally performs work at import time and is retained as a manual
    compatibility script. The actual pipeline behavior is covered by focused
    tests elsewhere in the suite.
    """

    legacy_manual_scripts = {
        "test_github_search.py",
        "test_multi_query_search.py",
        "test_pipeline.py",
        "test_query_loader.py",
    }
    return collection_path.name in legacy_manual_scripts and collection_path.parent.name == "tests"

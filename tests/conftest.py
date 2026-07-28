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
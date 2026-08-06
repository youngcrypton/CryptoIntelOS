"""Compatibility test for the optional legacy query loader."""

import importlib.util

import pytest


def test_query_loader_loads_ecosystems_when_available() -> None:
    module_name = "intelligence_query_engine.query_loader"
    if importlib.util.find_spec(module_name) is None:
        pytest.skip("legacy query_loader module is not present")

    module = __import__(module_name, fromlist=["query_loader"])
    ecosystems = module.query_loader.load_ecosystems()

    assert ecosystems

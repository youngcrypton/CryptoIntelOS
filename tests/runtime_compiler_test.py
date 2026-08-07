from dataclasses import FrozenInstanceError, asdict
from datetime import UTC, datetime
from typing import get_type_hints
from uuid import UUID
import pytest
from src.runtime.compiler import *
def test_projection_construction_and_serialization():
    provenance=ProvenanceIR("github", "repo:1", datetime.now(UTC))
    node=NodeIR(node_id=UUID(int=1), entity_reference="entity-1", node_type="entity", provenance=(provenance,))
    edge=EdgeIR(edge_id=UUID(int=2), source_node=node.node_id, target_node="node-2", relationship_reference="rel-1", direction="directed")
    projection=GraphProjection(nodes=(node,), edges=(edge,), timeline=TimelineIR(sequence=1))
    result=CompilerResult(projection=projection)
    assert asdict(result)["projection"]["nodes"] == (asdict(node),)
    assert projection.edges[0].source_node == node.node_id
def test_immutability_and_typing():
    with pytest.raises(FrozenInstanceError): CompilerPolicy().version="2"
    assert get_type_hints(NodeIR)["entity_reference"] == UUID | str
def test_registry_contract():
    assert "register" in CompilerRegistry.__dict__ and "get" in CompilerRegistry.__dict__

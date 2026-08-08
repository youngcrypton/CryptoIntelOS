import ast
from pathlib import Path

from src.core_intelligence import (
    Assessment, Contract, Entity, Evidence, Finding, Identity, MemoryObject,
    Observation, Policy, Relationship, Signal, Token, Wallet,
)
from src.core_intelligence.identity import Entity as IdentityEntity
from src.core_intelligence.models import Entity as LegacyEntity
from src.core_intelligence.onchain import Contract as OnChainContract
from src.core_intelligence.onchain import Token as OnChainToken
from src.core_intelligence.onchain import Wallet as OnChainWallet
from src.core_intelligence.relationships import Relationship as SemanticRelationship


def test_root_exports_authoritative_models() -> None:
    assert Entity is IdentityEntity
    assert Relationship is SemanticRelationship
    assert Wallet is OnChainWallet
    assert Token is OnChainToken
    assert Contract is OnChainContract
    assert LegacyEntity.__name__ == "LegacyEntity"
    assert all(value is not None for value in (Identity, Observation, Evidence, Finding, Assessment, Signal, MemoryObject, Policy))


def test_authoritative_class_names_have_single_definitions() -> None:
    expected = {
        "Entity": "src/core_intelligence/identity/entity.py",
        "Observation": "src/core_intelligence/models.py",
        "Evidence": "src/core_intelligence/models.py",
        "Finding": "src/core_intelligence/models.py",
        "Assessment": "src/core_intelligence/models.py",
        "Signal": "src/core_intelligence/models.py",
        "Relationship": "src/core_intelligence/relationships/relationship.py",
        "Wallet": "src/core_intelligence/onchain/wallet.py",
        "Token": "src/core_intelligence/onchain/token.py",
        "Contract": "src/core_intelligence/onchain/contract.py",
        "Policy": "src/core_intelligence/policy/policy.py",
        "MemoryObject": "src/core_intelligence/memory/memory_object.py",
    }
    definitions: dict[str, list[str]] = {name: [] for name in expected}
    for path in Path("src").rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8-sig"))
        for node in tree.body:
            if isinstance(node, ast.ClassDef) and node.name in definitions:
                definitions[node.name].append(path.as_posix())
    assert definitions == {name: [path] for name, path in expected.items()}

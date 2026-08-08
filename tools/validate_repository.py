"""Repository health checks used locally and by CI."""

from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUTHORITATIVE = {
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


def check_compile() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "compileall", "-q", "src", "tests"],
        cwd=ROOT,
    )
    if result.returncode:
        raise RuntimeError("compileall failed")


def check_imports() -> None:
    modules = (
        "src",
        "src.core_intelligence",
        "src.platform_sdk",
        "src.runtime",
        "src.github_intelligence",
        "src.website_intelligence",
        "src.twitter_intelligence",
        "src.unified_intelligence",
    )
    for module in modules:
        result = subprocess.run([sys.executable, "-c", f"import {module}"], cwd=ROOT)
        if result.returncode:
            raise RuntimeError(f"import failed: {module}")


def check_model_ownership() -> None:
    definitions = {name: [] for name in AUTHORITATIVE}
    for path in (ROOT / "src").rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8-sig"))
        relative = path.relative_to(ROOT).as_posix()
        for node in tree.body:
            if isinstance(node, ast.ClassDef) and node.name in definitions:
                definitions[node.name].append(relative)
    for name, expected in AUTHORITATIVE.items():
        if definitions[name] != [expected]:
            raise RuntimeError(f"canonical ownership violation for {name}: {definitions[name]}")


def check_runtime_boundaries() -> None:
    forbidden = ("ExecutionEngine", "RuntimePipeline")
    for path in (ROOT / "src").rglob("*.py"):
        relative = path.relative_to(ROOT)
        if relative.parts[:2] == ("src", "runtime"):
            continue
        text = path.read_text(encoding="utf-8-sig")
        if any(token in text for token in forbidden):
            raise RuntimeError(f"legacy Runtime orchestration import in {relative}")
    core = ROOT / "src" / "core_intelligence"
    for path in core.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8-sig"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import) and any(alias.name.startswith("src.runtime") for alias in node.names):
                raise RuntimeError("core_intelligence must not depend on Runtime")
            if isinstance(node, ast.ImportFrom) and (node.module or "").startswith("src.runtime"):
                raise RuntimeError("core_intelligence must not depend on Runtime")


def check_git_diff() -> None:
    result = subprocess.run(["git", "diff", "--check"], cwd=ROOT)
    if result.returncode:
        raise RuntimeError("git diff --check failed")


def validate() -> None:
    check_compile()
    check_imports()
    check_model_ownership()
    check_runtime_boundaries()
    check_git_diff()


if __name__ == "__main__":
    try:
        validate()
    except Exception as error:
        print(f"repository validation failed: {error}", file=sys.stderr)
        raise SystemExit(1)
    print("repository validation passed")

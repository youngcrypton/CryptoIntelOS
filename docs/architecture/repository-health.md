# Repository Health and Production Engineering

## Repository layout

- `src/` contains importable platform and application packages. `src/__main__.py` is the canonical module startup entry.
- `tests/` contains unit, integration, architecture, and vertical-slice tests.
- `tools/` contains reusable engineering validation.
- `.github/workflows/` contains continuous-integration and security workflows.
- `docs/architecture/` records architectural boundaries and contributor expectations.

Some package trees intentionally use Python namespace-package discovery and therefore do not require an `__init__.py` in every directory. Import verification covers the supported top-level packages.

## CI pipeline

The Python quality workflow runs on pushes and pull requests targeting `main`. It installs the pinned repository requirements, executes `tools/validate_repository.py`, and then runs the complete pytest suite. Any command returning a non-zero status fails the workflow. CodeQL remains a separate scheduled security workflow.

## Repository validation

Run this command before every commit:

```text
python tools/validate_repository.py
```

The validator executes `compileall`, imports supported packages in isolated Python processes, verifies authoritative canonical-model ownership, rejects direct use of `ExecutionEngine` or `RuntimePipeline` outside Runtime, enforces the Kernel-to-Runtime dependency direction, and runs `git diff --check`.

The validator is deliberately standard-library-only so it can run before optional development tooling is installed.

## Docker startup

Docker starts the application with `python -m src`. The module entry is implemented by `src/__main__.py` and delegates to the existing `src.core.app.run` function without changing startup behavior. The root `main.py` remains a compatible local entry point.

## Testing strategy

Pytest discovers both conventional `test_*.py` files and the repository's established `*_test.py` files. Tests beneath `tests/` are not intentionally excluded. Focused repository-health tests cover discovery configuration, package imports, validator architecture checks, and the Docker module entry point.

## Contribution workflow and quality gates

Before committing:

1. Keep changes scoped to the approved sprint or fix.
2. Run `python tools/validate_repository.py`.
3. Run `python -m pytest` when pytest is installed.
4. Review `git status --short` and stage only intended files.
5. Confirm generated files, credentials, local environment files, and unrelated work are not staged.

Changes are ready for review only when compilation, imports, architecture checks, whitespace validation, and the discoverable test suite pass.

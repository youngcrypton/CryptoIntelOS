# Contributing to CryptoIntel OS

Thank you for helping improve CryptoIntel OS. Contributions should solve a clear user, operator, reliability, security, or maintainability problem while preserving the established architecture.

## Before contributing

1. Read [AGENTS.md](AGENTS.md), [ARCHITECTURE.md](ARCHITECTURE.md), and the relevant documentation under [`docs/`](docs/).
2. Search existing issues and pull requests.
3. Open an issue for substantial changes, describing the user problem, affected boundaries, security implications, tests, and migration impact.

## Architecture requirements

- Keep canonical model ownership in `src/core_intelligence`.
- Create canonical business objects only in adapters.
- Enter Runtime through Platform SDK.
- Do not add alternate orchestration paths or duplicate Kernel contracts.
- Preserve identifiers, provenance, traceability, confidence, and execution metadata.
- Keep live network tests optional and deterministic tests credential-free.

## Development setup

```bash
python -m venv .venv
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
playwright install chromium
```

## Quality gates

Run before opening a pull request:

```bash
python tools/validate_repository.py
python -m compileall -q src tests
python -m pytest
git diff --check
```

Add focused unit, integration, contract, failure, recovery, security, or regression coverage proportional to the change.

## Pull requests

- Keep each pull request focused.
- Explain user impact and known limitations.
- Document configuration and operational changes.
- Do not include credentials, private payloads, generated caches, local databases, or unrelated formatting changes.
- Update public documentation and `CHANGELOG.md` when behavior or public interfaces change.

By participating, you agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md) and [Security Policy](SECURITY.md).

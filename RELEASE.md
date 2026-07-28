# CryptoIntel OS Release Process

## Versioning

CryptoIntel OS follows Semantic Versioning (SemVer).

Format:

MAJOR.MINOR.PATCH

Example:

0.2.0

---

## Version Types

### PATCH

Increment for:

- Bug fixes
- Documentation updates
- Internal improvements

Example:

0.2.0 → 0.2.1

---

### MINOR

Increment for:

- New features
- New collectors
- New analyzers
- New intelligence engines

Example:

0.2.0 → 0.3.0

---

### MAJOR

Increment for:

- Breaking API changes
- Major architecture redesign
- Database schema redesign

Example:

0.9.0 → 1.0.0

---

## Release Checklist

Before every release:

- All tests pass
- Black passes
- Flake8 passes
- isort passes
- MyPy passes
- README updated
- CHANGELOG updated
- VERSION updated

---

## Git Release

Example:

git tag v0.2.0

git push origin v0.2.0

GitHub Actions will create the release artifacts.

---

## Current Stable Version

See:

VERSION
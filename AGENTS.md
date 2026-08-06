# CryptoIntel OS AI Engineering Handbook

## 1. Project Mission

CryptoIntel OS is an autonomous crypto intelligence platform that continuously collects, analyzes, scores, and distributes high-value intelligence from:

- X (Twitter)
- Discord
- Telegram
- GitHub
- News
- Documentation
- On-chain data

The platform must operate 24/7 with minimal human intervention.

---

## 2. Vision

CryptoIntel OS is designed to become the Bloomberg Terminal of Crypto Intelligence: a trusted operating layer that turns a large, fast-moving information landscape into timely, useful intelligence.

Its direction is guided by:

- **Automation:** Collect, process, and distribute intelligence with minimal manual work.
- **Intelligence:** Surface meaningful signals, context, and priorities rather than raw noise.
- **Accuracy:** Validate sources, preserve provenance, and communicate uncertainty clearly.
- **Reliability:** Deliver dependable operation and graceful handling of partial failures.
- **Scalability:** Support growing data sources, users, and workloads without compromising quality.

---

## 3. AI Team Roles

### Project Owner

**Responsibilities:**

- Owns the vision.
- Approves architecture.
- Approves releases.

### Chief Software Architect (ChatGPT)

**Responsibilities:**

- Designs architecture.
- Defines implementation plans.
- Reviews engineering decisions.
- Defines coding standards.
- Defines AI behaviour.

### Software Engineer (Codex)

**Responsibilities:**

- Implements approved architecture.
- Writes code.
- Creates files.
- Updates files.
- Runs tests.
- Fixes bugs.

Codex must never redesign architecture without explicit approval.

---

## 4. Engineering Principles

- Build first, refactor later.
- Never break working code.
- Keep modules small and focused.
- Prefer readability over cleverness.
- Prefer explicit code over implicit or surprising behaviour.
- Never modify unrelated files.
- Preserve backwards compatibility where possible.

---

## 5. Architecture Rules

- Apply the single-responsibility principle: each component should have one clear purpose.
- Design for modularity so components can be developed, tested, and replaced independently.
- Keep coupling loose by depending on stable interfaces rather than implementation details.
- Maintain separation of concerns between presentation, application logic, domain logic, data access, and external integrations.
- Do not introduce circular imports.
- Create reusable components when behaviour is genuinely shared and stable.

---

## 6. Coding Standards

Python code must follow these standards:

- Use descriptive names for modules, classes, functions, variables, and tests.
- Use type hints when appropriate, especially at public interfaces and system boundaries.
- Keep functions small, focused, and easy to test.
- Document public APIs and non-obvious decisions.
- Add comments only when they provide useful context that the code itself cannot express.
- Follow the established formatting, linting, and import conventions of the project.

---

## 7. Testing Standards

After every implementation:

1. Run relevant tests.
2. Fix failures.
3. Summarize changes.
4. Never claim success without verification.

Tests should cover changed behaviour, important failure paths, and integrations through suitable fixtures or mocks.

---

## 8. Knowledge Layer Standards

Every knowledge pack must maintain a consistent structure containing:

- `hashtags`
- `keywords`
- `boolean_queries`

Knowledge packs should prioritize completeness over arbitrary limits. Add all relevant, validated terms and query patterns needed to represent the subject accurately; do not truncate useful intelligence merely to meet a fixed count.

---

## 9. General Rules

Codex must:

- Never delete files unless instructed.
- Never rename folders unless instructed.
- Never introduce dependencies unless instructed.
- Never change project architecture unless instructed.
- Explain all changes before completion.

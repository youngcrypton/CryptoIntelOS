# Architectural Decisions

---

This document records important architectural decisions.

Future contributors should understand these decisions before modifying the codebase.

---

# Decision 001

## Modular Architecture

Decision

Use independent packages.

Reason

Improves maintainability and scalability.

Status

Accepted.

---

# Decision 002

## SQLite

Decision

Use SQLite during early development.

Reason

Simple.

Portable.

Zero configuration.

Future migration to PostgreSQL remains possible.

Status

Accepted.

---

# Decision 003

## Repository Pattern

Decision

All database operations occur inside repositories.

Reason

Separates persistence from business logic.

Status

Accepted.

---

# Decision 004

## Service Layer

Decision

Business logic belongs inside services.

Reason

Collectors should only collect.

Repositories should only store.

Status

Accepted.

---

# Decision 005

## Playwright

Decision

Use Playwright for JavaScript rendering.

Reason

Modern crypto websites frequently require JavaScript.

Status

Accepted.

---

# Decision 006

## Requests Fallback

Decision

Attempt Requests before Playwright.

Reason

Improves speed and reduces browser usage.

Status

Accepted.

---

# Decision 007

## Rule Based Intelligence

Decision

Use independent intelligence rules.

Reason

Allows easy expansion.

Status

Accepted.

---

# Decision 008

## Historical Snapshots

Decision

Store snapshots.

Reason

Historical intelligence is more valuable than current state alone.

Status

Accepted.

---

# Decision 009

## Scheduler

Decision

Single Scheduler controls execution.

Reason

Centralized orchestration.

Status

Accepted.

---

# Decision 010

## AI Layer

Decision

AI consumes structured findings instead of raw HTML.

Reason

Improves reliability.

Reduces hallucinations.

Status

Accepted.

---

# Future Decisions

Future architectural decisions should continue using this numbering system.

Each decision should include:

- Decision
- Reason
- Alternatives
- Status
- Date
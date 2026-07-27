# CryptoIntel OS Development Guide

---

# Purpose

This document explains how CryptoIntel OS is developed and extended.

It is intended for contributors, maintainers, and AI coding agents.

Following this guide ensures that new features integrate cleanly with the existing architecture without introducing unnecessary coupling or duplication.

---

# Development Philosophy

CryptoIntel OS is built around a small set of engineering principles.

- Single responsibility
- Modular architecture
- Reusable components
- Clear separation of concerns
- Testability
- Extensibility
- Readability over cleverness
- Documentation first

Every change to the codebase should preserve these principles.

---

# Development Workflow

Every new feature should follow the same workflow.

```
Idea

↓

Design

↓

Architecture Review

↓

Implementation

↓

Testing

↓

Documentation

↓

Commit

↓

Pull Request

↓

Review

↓

Merge
```

Documentation is considered part of the implementation.

---

# Project Structure

```
CryptoIntelOS/

assets/
config/
docs/
logs/
tests/

src/
    collectors/
    core/
    crawlers/
    database/
    discovery/
    intelligence/
    models/
    pipeline/
    scheduler/
    services/
    web_engine/

main.py
```

Every package has one clearly defined responsibility.

---

# Adding a New Collector

Collectors are responsible only for retrieving raw information.

Collectors must **never**:

- analyze data
- write directly to the database
- generate findings
- create events

Collectors should only collect.

## Step 1

Create a new folder.

Example:

```
src/collectors/telegram/
```

---

## Step 2

Create:

```
collector.py
```

The collector should expose one public entry point.

Example:

```python
class TelegramCollector:
    def collect(self, project):
        ...
```

---

## Step 3

Register the collector inside:

```
src/collectors/registry.py
```

Use the existing registration pattern.

---

## Step 4

Enable it through configuration.

The Scheduler should automatically detect it.

---

# Adding a New Intelligence Rule

Rules belong inside:

```
src/intelligence/rules/
```

Every rule should detect exactly one type of information.

Examples:

- Documentation
- Whitepaper
- GitHub
- Audit
- Team
- Investor

Rules must never perform crawling.

Rules only analyze extracted information.

---

# Rule Design

Every rule should:

Receive normalized data.

Return Findings.

Never write directly to the database.

Example:

```
Input

↓

Normalized Website

↓

Rule

↓

Finding
```

---

# Adding an Extractor

Extractors convert normalized information into structured entities.

Examples:

```
Website

↓

Extractor

↓

GitHub Repository
```

or

```
Website

↓

Extractor

↓

Documentation Link
```

Extractors should not contain business logic.

---

# Adding a New Service

Services coordinate business logic.

Services may:

- compare snapshots
- create events
- process findings
- call repositories

Services should never perform crawling.

---

# Adding a Repository

Repositories isolate database access.

Every table should have its own repository.

Example:

```
Projects

↓

ProjectRepository
```

Repositories should contain SQL only.

Business decisions belong inside Services.

---

# Adding a Model

Models belong inside:

```
src/models/
```

Models represent business entities.

Examples:

- Project
- Event
- Finding
- WebsiteSnapshot

Models should avoid application logic.

---

# Database Changes

Whenever adding a table:

1. Update the schema.
2. Create a Repository.
3. Create a Service if required.
4. Update documentation.

Never access SQLite directly outside repositories.

---

# Scheduler Integration

New collectors must be executed by the Scheduler.

The Scheduler controls:

- execution order
- progress reporting
- future retries
- future parallel execution

Collectors should never start themselves.

---

# Logging

Every major action should generate a log entry.

Examples:

```
Collector started

Collector finished

Website crawled

Event created

Snapshot stored
```

Sensitive information must never be written to logs.

---

# Error Handling

Recoverable errors should be handled gracefully.

Examples:

- network timeout
- missing webpage
- invalid HTML

The application should continue processing other projects whenever possible.

---

# Testing

Every new feature should include tests.

Recommended structure:

```
tests/

test_collectors.py

test_services.py

test_rules.py

test_database.py
```

Future versions will include integration and end-to-end tests.

---

# Documentation Requirements

Every significant feature should update:

- README.md (if user-facing)
- ARCHITECTURE.md (if architecture changes)
- SPECIFICATION.md (if scope changes)
- CHANGELOG.md
- PROJECT_STATE.md

Documentation should evolve alongside the code.

---

# Code Review Checklist

Before merging, confirm:

- Architecture remains modular.
- No duplicated logic.
- Services contain business logic.
- Repositories contain persistence logic only.
- Collectors do not analyze data.
- Rules do not access the database.
- Documentation is updated.
- Logging is appropriate.
- Tests pass.

---

# Long-Term Goal

The development process is designed so CryptoIntel OS can continue growing for years without requiring major architectural rewrites.

Every contribution should improve maintainability, readability, and scalability.
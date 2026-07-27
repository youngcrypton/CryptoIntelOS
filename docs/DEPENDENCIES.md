# Dependency Map

---

# Overview

CryptoIntel OS follows a layered architecture.

Higher layers depend on lower layers.

Lower layers should never depend on higher layers.

---

# Layer Diagram

```
Application

↓

Core

↓

Scheduler

↓

Discovery

↓

Collectors

↓

Pipeline

↓

Intelligence

↓

Services

↓

Repositories

↓

SQLite
```

---

# Core

Depends on

- Configuration
- Logger

Used By

- Application

---

# Scheduler

Depends on

- Discovery
- Collector Registry
- Pipeline

Used By

- Application

---

# Discovery

Depends on

- Project Repository

Used By

- Scheduler

---

# Collectors

Depends on

- Crawlers

Must NOT depend on

- Database
- Rule Engine

---

# Crawlers

Depends on

- Requests
- Playwright
- Web Engine

Used By

- Website Collector

---

# Pipeline

Depends on

- Intelligence Services

Used By

- Scheduler

---

# Intelligence

Depends on

- Models

Produces

- Findings

Consumes

- Normalized Data

---

# Services

Depends on

- Repositories

Consumes

- Findings

Produces

- Events

---

# Repositories

Depends on

- SQLite

Must NOT depend on

- Services
- Scheduler
- Collectors

---

# Models

Shared by

- Collectors
- Services
- Intelligence
- Repositories

Models should contain no application logic.

---

# Web Engine

Depends on

- Playwright

Used By

- Website Crawler

---

# Dependency Rules

Allowed

Scheduler → Collectors

Collectors → Crawlers

Pipeline → Intelligence

Services → Repositories

Repositories → SQLite

Forbidden

Collectors → Database

Collectors → Rule Engine

Rules → SQLite

Repositories → Scheduler

Repositories → Collectors

Services → Browser

---

# Architectural Goal

Dependencies should always flow downward.

No circular dependencies should ever exist.
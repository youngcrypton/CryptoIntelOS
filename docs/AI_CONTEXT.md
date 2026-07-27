# AI Context

---

# Purpose

This document provides architectural context for AI coding assistants working on CryptoIntel OS.

Its purpose is to reduce onboarding time and preserve architectural consistency across future development sessions.

Any AI modifying this repository should read this document before generating code.

---

# Project Summary

CryptoIntel OS is a modular intelligence platform that continuously monitors blockchain projects.

Its purpose is to collect information from multiple sources, transform raw information into structured intelligence, detect meaningful changes, and store historical knowledge for future analysis.

The system is not a traditional web scraper.

Instead, it is an intelligence platform.

---

# Core Philosophy

The architecture is based on strict separation of responsibilities.

Every component has exactly one responsibility.

Examples:

Collectors collect.

Crawlers download.

Normalizers normalize.

Extractors extract.

Rules analyze.

Services coordinate.

Repositories persist data.

Schedulers orchestrate execution.

Do not combine responsibilities.

---

# Architecture Overview

```
Application

↓

Scheduler

↓

Discovery

↓

Collectors

↓

Pipeline

↓

Normalizer

↓

Extractor

↓

Rule Engine

↓

Findings

↓

Services

↓

Repositories

↓

SQLite
```

No component should bypass this pipeline.

---

# Current Implemented Modules

Current packages include:

```
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
```

These packages already define the architectural boundaries.

New functionality should fit into one of these packages.

Avoid creating unnecessary top level packages.

---

# Current Collectors

Implemented:

- Website Collector
- X Collector

Planned:

- Discord
- Telegram
- GitHub
- RSS
- Medium
- Mirror
- CoinGecko
- CoinMarketCap

New collectors should follow the existing registration pattern inside:

```
src/collectors/registry.py
```

---

# Intelligence Engine

The intelligence package converts raw information into structured findings.

Current stages include:

Normalization

↓

Extraction

↓

Rule Evaluation

↓

Findings

↓

Events

Every intelligence module should be independent.

Avoid tightly coupling rules together.

---

# Database Design

Database access must always occur through repositories.

Never execute SQL directly from:

- Collectors
- Services
- Scheduler
- Pipeline

Repositories own persistence.

Services own business logic.

---

# Services

Services coordinate application logic.

Typical responsibilities include:

- Comparing snapshots
- Recording events
- Managing projects
- Processing findings

Services should never perform crawling.

---

# Scheduler

The Scheduler is the application's central controller.

Responsibilities include:

- Loading projects
- Executing collectors
- Passing results into the pipeline
- Reporting execution progress

Collectors must never start themselves.

---

# Browser Management

Browser rendering is centralized inside:

```
src/web_engine/
```

Do not instantiate Playwright browsers inside collectors.

Always use the Web Engine.

This reduces browser startup overhead.

---

# Current Database Tables

Current tables include:

- Projects
- Events
- WebsiteSnapshots
- XProfileSnapshots

Future tables should continue using repository abstractions.

---

# Coding Expectations

Future code should prioritize:

Readability over cleverness.

Small functions.

Small classes.

Single responsibility.

Low coupling.

High cohesion.

Avoid unnecessary inheritance.

Prefer composition.

---

# Error Handling

Recoverable failures should not terminate the application.

Examples:

Website unavailable.

Network timeout.

Rate limiting.

Missing HTML.

The Scheduler should continue processing remaining projects.

---

# Logging

Every major operation should generate useful logs.

Examples:

Collector started.

Collector finished.

Snapshot stored.

Event recorded.

Browser started.

Browser stopped.

Avoid excessive logging.

Never log secrets.

---

# Documentation Requirements

Whenever architecture changes:

Update:

README.md

ARCHITECTURE.md

SPECIFICATION.md

PROJECT_STATE.md

CHANGELOG.md

Documentation is considered part of implementation.

---

# Long Term Vision

CryptoIntel OS is intended to evolve into a complete Web3 intelligence platform.

Future capabilities include:

AI summaries.

Risk scoring.

Relationship graphs.

Wallet monitoring.

Governance tracking.

Token intelligence.

Historical analytics.

REST API.

Dashboard.

Cloud deployment.

Plugin architecture.

Distributed workers.

When implementing new features, preserve architectural consistency rather than introducing shortcuts.

---

# Important Rules For Future AI Agents

Always preserve modularity.

Never mix responsibilities.

Do not bypass repositories.

Do not bypass services.

Do not let collectors analyze data.

Do not let rules write to the database.

Avoid duplicate logic.

Document architectural changes.

Follow existing package boundaries.

When uncertain, prefer consistency over convenience.

---

# Repository Goal

The long term objective is to create a maintainable, scalable, AI friendly codebase capable of continuous development by both human contributors and AI coding assistants.

Every contribution should move the repository closer to that goal.
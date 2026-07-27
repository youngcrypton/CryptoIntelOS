# CryptoIntel OS Style Guide

---

# Purpose

This document defines the coding, documentation, and repository standards used throughout CryptoIntel OS.

Following these standards keeps the project consistent, maintainable, and easy for both human developers and AI coding assistants to understand.

---

# General Principles

Code should be:

- Simple
- Readable
- Predictable
- Modular
- Well documented

Always prefer readability over clever implementations.

---

# Python Style

Follow the PEP 8 style guide.

Additional conventions:

- Four spaces for indentation.
- Maximum line length of approximately 100 characters.
- Use descriptive variable names.
- Use meaningful function names.
- Avoid unnecessary abbreviations.

Example:

```python
def collect_project_information(project):
    pass
```

Instead of:

```python
def c(p):
    pass
```

---

# File Naming

Use lowercase file names.

Examples:

```
collector.py

manager.py

config_manager.py

project_repository.py
```

Avoid spaces.

Avoid camelCase.

---

# Class Naming

Use PascalCase.

Examples:

```
WebsiteCollector

ProjectRepository

Scheduler

RuleEngine
```

---

# Function Naming

Use snake_case.

Examples:

```
collect_projects()

save_snapshot()

generate_events()
```

---

# Variable Naming

Choose descriptive names.

Good:

```
project

website_snapshot

collector_result

normalized_data
```

Avoid:

```
x

tmp

obj

data1
```

unless the context is extremely small.

---

# Comments

Comments should explain *why*, not *what*.

Good:

```python
# Requests is attempted first because it is significantly faster than browser rendering.
```

Avoid:

```python
# Increment i
i += 1
```

---

# Docstrings

Every public class and function should include a docstring.

Example:

```python
def collect(self, project):
    """
    Collect raw website information for a project.
    """
```

---

# Imports

Organize imports into three groups:

Standard library

Third party libraries

Local project imports

Example:

```python
import logging

from rich.console import Console

from src.database.manager import database_manager
```

---

# Error Handling

Handle expected exceptions gracefully.

Example:

```python
try:
    page = downloader.fetch(url)
except Exception:
    logger.exception("Unable to download page.")
```

Avoid empty exception handlers.

---

# Logging

Use the project logger.

Log important actions.

Examples:

- Collector started
- Snapshot saved
- Event created
- Browser launched

Avoid excessive logging.

Never log secrets.

---

# Architecture Rules

Collectors collect.

Crawlers download.

Normalizers normalize.

Extractors extract.

Rules analyze.

Services coordinate.

Repositories store.

Each component has exactly one responsibility.

---

# Database Rules

Never execute SQL outside repositories.

Business logic belongs inside services.

---

# Documentation

Documentation should always be updated whenever:

- Architecture changes
- New packages are added
- Public interfaces change
- New features are introduced

---

# Git Commit Messages

Use clear commit messages.

Examples:

```
Add Telegram collector

Improve website snapshot comparison

Refactor scheduler execution

Add AI documentation
```

Avoid vague messages such as:

```
Update

Fix

Changes
```

---

# Pull Requests

Every pull request should:

- Solve one problem.
- Include documentation updates.
- Preserve architecture.
- Pass tests.
- Avoid unrelated changes.

---

# Repository Goal

Maintain a clean, professional codebase that remains understandable years into the future.
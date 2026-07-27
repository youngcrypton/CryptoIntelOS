# Contributing to CryptoIntel OS

First of all, thank you for considering contributing to CryptoIntel OS.

This project aims to become an open source blockchain intelligence platform capable of monitoring, analyzing, and understanding the rapidly evolving crypto ecosystem.

Every contribution, whether it is code, documentation, testing, design, or ideas, helps move the project closer to that vision.

---

# Table of Contents

- Philosophy
- Before You Start
- Development Environment
- Project Architecture
- Branch Strategy
- Commit Message Guidelines
- Coding Standards
- Documentation Standards
- Pull Requests
- Reporting Bugs
- Requesting Features
- Development Roadmap
- Community Expectations

---

# Project Philosophy

CryptoIntel OS follows several core engineering principles.

## Single Responsibility Principle

Every module should have one clearly defined responsibility.

Examples:

- Collectors collect data.
- Crawlers download webpages.
- Extractors extract information.
- Rules analyze intelligence.
- Services coordinate workflows.
- Repositories interact with the database.

Avoid combining multiple responsibilities into a single module.

---

## Modular Architecture

Every new feature should fit naturally into the existing architecture.

Rather than modifying unrelated files, add new functionality through dedicated modules whenever possible.

This keeps the codebase maintainable and scalable.

---

## Extensibility

When implementing new functionality, think about future expansion.

For example:

Instead of writing a GitHub specific intelligence rule, consider whether the rule could be generalized so it may later support GitLab or Bitbucket.

---

# Before You Start

Before writing code:

- Read the README.
- Read the ROADMAP.
- Search existing GitHub Issues.
- Open a discussion for major architectural changes.
- Keep pull requests focused on one feature or fix.

---

# Development Environment

Clone the repository.

```bash
git clone https://github.com/youngcrypton/CryptoIntelOS.git
```

Move into the project.

```bash
cd CryptoIntelOS
```

Create a virtual environment.

```bash
python -m venv .venv
```

Activate the environment.

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Run CryptoIntel OS.

```bash
python main.py
```

---

# Project Architecture

The project follows a layered architecture.

```text
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

New features should respect this flow.

For example:

- Collectors should never write directly to the database.
- Rules should never communicate directly with Playwright.
- Repositories should never contain business logic.

---

# Branch Strategy

Create a new branch for every feature.

Examples:

```text
feature/github-collector

feature/token-detector

feature/discord-collector

fix/scheduler-timeout

fix/database-lock

docs/update-readme

refactor/project-service
```

Avoid committing directly to the `main` branch.

---

# Commit Message Guidelines

Write clear, descriptive commit messages.

Good examples:

```text
Add GitHub collector

Improve website extractor

Implement audit detection rule

Optimize HTML quality scoring

Refactor scheduler execution
```

Avoid generic commit messages such as:

```text
update

changes

fix

work

done
```

---

# Coding Standards

CryptoIntel OS follows modern Python development practices.

## General Guidelines

- Follow PEP 8.
- Prefer readability over cleverness.
- Write descriptive variable names.
- Keep functions focused.
- Keep modules cohesive.
- Avoid duplicated logic.

---

## Naming Conventions

Classes

```python
WebsiteCollector
```

Functions

```python
collect_project()
```

Variables

```python
project_name
```

Constants

```python
MAX_RETRIES
```

---

## Docstrings

Every public class and function should include a meaningful docstring.

Example:

```python
class WebsiteCollector:
    """
    Collects website data for monitored blockchain projects.
    """
```

---

# Documentation Standards

Whenever functionality changes:

Update:

- README.md
- CHANGELOG.md
- ROADMAP.md (if necessary)
- Relevant inline documentation

Documentation is considered part of the implementation.

---

# Pull Requests

Before submitting a Pull Request:

- Ensure the project runs successfully.
- Update documentation.
- Test your changes.
- Keep changes focused.
- Explain why the change is necessary.

A good Pull Request answers:

- What changed?
- Why did it change?
- How was it tested?

---

# Reporting Bugs

Please include:

- Operating system
- Python version
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- Console output
- Error traceback

Detailed reports significantly improve debugging.

---

# Feature Requests

Feature requests should explain:

- The problem
- The proposed solution
- Possible alternatives
- Benefits
- Implementation ideas (optional)

---

# Testing

Future releases will include automated testing.

Current expectations:

- Verify the application starts.
- Ensure collectors execute correctly.
- Confirm database changes.
- Verify no existing functionality is broken.

---

# Development Roadmap

Current priorities include:

- Website Intelligence
- X Intelligence
- Telegram Collector
- Discord Collector
- GitHub Collector
- AI Intelligence
- Dashboard
- Notification System

See **ROADMAP.md** for complete milestones.

---

# Community Expectations

We welcome contributors from all backgrounds.

Whether you are:

- Python developer
- Blockchain engineer
- Security researcher
- Data scientist
- Student
- Technical writer

Your contributions are valuable.

Constructive discussion, respectful collaboration, and thoughtful feedback help CryptoIntel OS continue to improve.

---

Thank you for contributing to CryptoIntel OS.

Together we are building an intelligent, open source platform for blockchain research and automated crypto intelligence.
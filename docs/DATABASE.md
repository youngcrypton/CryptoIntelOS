# Database Documentation

## Overview

CryptoIntel OS uses a lightweight local SQLite database as its primary persistence layer.

The database stores:

- Projects
- Websites
- Website snapshots
- X (Twitter) profile snapshots
- Intelligence findings
- Events
- Crawl history
- Metadata

The database is intentionally designed using a repository pattern to isolate business logic from storage implementation.

---

# Database Location

Default location:

```

data/cryptointel.db

```

The database file is automatically created if it does not exist.

---

# Database Architecture

```

Application
│
▼
Services
│
▼
Repositories
│
▼
Database Manager
│
▼
SQLite

```

Business logic never communicates directly with SQLite.

All database access passes through repositories.

---

# Repository Pattern

Repositories encapsulate all SQL operations.

Advantages:

- Separation of concerns
- Easier testing
- Easier migration
- Cleaner services
- Reduced SQL duplication

Current repositories include:

```

database/repositories/

event_repository.py
project_repository.py
website_snapshot_repository.py
x_profile_repository.py

```

Future repositories may include:

```

finding_repository.py
crawl_repository.py
notification_repository.py
user_repository.py

```

---

# Core Entities

## Project

Represents a cryptocurrency project.

Typical fields:

- id
- name
- slug
- description
- website
- github
- discord
- telegram
- created_at
- updated_at

---

## Website

Represents an official website belonging to a project.

Stores:

- URL
- crawl status
- discovery source
- metadata

---

## Website Snapshot

Represents a complete crawl of a website at a point in time.

Contains:

- timestamp
- extracted pages
- metadata
- hashes
- content statistics

Snapshots enable historical comparisons.

---

## X Profile Snapshot

Stores information collected from X.

Includes:

- followers
- following
- bio
- pinned post
- profile image
- verified status
- engagement metrics

Historical snapshots allow trend detection.

---

## Event

Represents significant project events.

Examples:

- Website update
- New documentation
- GitHub activity
- Partnership announcement
- Whitepaper release
- Team changes

Events become intelligence signals.

---

# Intelligence Storage

Future versions may include dedicated tables for:

```

Findings
Signals
Confidence Scores
Entities
Keywords
Topics
Relationships

```

This will support AI-powered analysis.

---

# Crawl History

Crawler metadata may include:

- crawl started
- crawl finished
- pages visited
- pages skipped
- response codes
- failures
- retries

Useful for debugging and monitoring.

---

# Relationships

```

Project
│
├──────── Websites
│               │
│               ├──────── Website Snapshots
│               │
│               └──────── Crawl History
│
├──────── X Profiles
│               │
│               └──────── X Snapshots
│
├──────── Events
│
└──────── Intelligence Findings

```

---

# Database Manager

Database access is coordinated through:

```

database/manager.py

```

Responsibilities:

- Open connections
- Close connections
- Transactions
- Error handling
- Initialization

No other module should manage raw database connections directly.

---

# Transactions

All write operations should use transactions.

Benefits:

- Atomic updates
- Rollback support
- Consistency
- Error recovery

---

# Future Migration Strategy

SQLite is intentionally used during early development.

Future supported databases may include:

- PostgreSQL
- MySQL
- MariaDB

Because repositories isolate storage logic, migration should require minimal business logic changes.

---

# Backup Strategy

Recommended backups:

- Daily database copy
- Snapshot before upgrades
- Snapshot before schema migrations

Never modify the live database manually.

---

# Schema Versioning

Future releases should introduce migration support.

Potential tools:

- Alembic
- SQLAlchemy Migrations

Version-controlled schema evolution ensures compatibility across releases.

---

# Performance Considerations

Current workload is expected to remain lightweight.

Potential optimizations include:

- Indexes
- Query optimization
- Batch inserts
- Connection pooling
- Cached lookups

These should only be introduced after profiling.

---

# Security

Sensitive information should never be stored in plaintext.

Examples:

- API Keys
- Tokens
- Passwords

Secrets belong inside:

```

.env

```

Never commit secrets into the database.

---

# Development Notes

When adding new tables:

1. Create the model.
2. Create the repository.
3. Register migrations.
4. Update documentation.
5. Add unit tests.

Following this workflow keeps the persistence layer maintainable.

---

# Long-Term Vision

The database will evolve into the central knowledge store powering CryptoIntel OS.

It will support:

- Historical intelligence
- Trend analysis
- AI-assisted reasoning
- Project scoring
- Alert generation
- Relationship mapping
- Cross-platform correlation

The repository architecture ensures that storage technology can evolve without disrupting the rest of the application.
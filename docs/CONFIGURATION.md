# Configuration Documentation

# Overview

CryptoIntel OS is designed around centralized configuration.

Rather than hardcoding values throughout the codebase, configuration is loaded from dedicated files and environment variables.

This allows:

- Easy deployment
- Environment separation
- Cleaner code
- Better security
- Easier maintenance

---

# Configuration Sources

The application loads configuration from multiple sources.

Priority (highest to lowest):

```
Environment Variables
↓

.env

↓

JSON Configuration

↓

Default Values
```

This hierarchy allows production environments to override development settings without modifying source code.

---

# Configuration Files

## .env

Contains sensitive configuration.

Examples:

```
OPENAI_API_KEY=

DISCORD_TOKEN=

GITHUB_TOKEN=

DATABASE_PATH=data/cryptointel.db

LOG_LEVEL=INFO
```

Never commit this file.

---

## .env.example

Contains the same variables without secrets.

Example:

```
OPENAI_API_KEY=

DISCORD_TOKEN=

DATABASE_PATH=data/cryptointel.db

LOG_LEVEL=INFO
```

This file documents required configuration.

---

## config/collectors.json

Stores collector configuration.

Example:

```
{
    "website": {
        "enabled": true
    },
    "x": {
        "enabled": true
    }
}
```

This allows collectors to be enabled or disabled without modifying code.

---

# Configuration Manager

Main implementation:

```
src/core/config_manager.py
```

Responsibilities:

- Load .env
- Parse JSON
- Apply defaults
- Validate values
- Expose configuration globally

Other modules should never load .env directly.

---

# Configuration Flow

```
Application Starts

↓

Configuration Manager

↓

Load Environment Variables

↓

Load JSON Configuration

↓

Apply Defaults

↓

Validate Configuration

↓

Expose Settings
```

---

# Core Configuration Categories

## Database

Examples:

```
DATABASE_PATH

DATABASE_TIMEOUT

DATABASE_POOL_SIZE
```

Controls persistence.

---

## Logging

Examples:

```
LOG_LEVEL

LOG_FILE

LOG_ROTATION
```

Controls application logging.

---

## Crawlers

Examples:

```
MAX_CONCURRENT_CRAWLERS

REQUEST_TIMEOUT

MAX_RETRIES

CRAWL_DELAY
```

Controls crawling behavior.

---

## Browser Engine

Examples:

```
HEADLESS

BROWSER_TIMEOUT

USER_AGENT
```

Used by Playwright.

---

## Discovery Engine

Configuration may include:

```
MAX_DISCOVERY_DEPTH

MAX_PROJECTS

DISCOVERY_INTERVAL
```

Controls automatic project discovery.

---

## AI

Potential settings:

```
OPENAI_API_KEY

OPENAI_MODEL

MAX_TOKENS

TEMPERATURE
```

Controls AI processing.

---

## Notifications

Examples:

```
DISCORD_WEBHOOK

SLACK_WEBHOOK

EMAIL_SERVER
```

Used for alerts.

---

## Scheduler

Examples:

```
SCAN_INTERVAL

FULL_SCAN_INTERVAL

DAILY_REPORT_TIME
```

Controls automated execution.

---

# Default Values

Every configuration option should have a sensible default.

Example:

```
Timeout

↓

30 seconds
```

If a value is missing, the application should continue operating whenever possible.

---

# Validation

Configuration Manager validates:

- Required values
- Invalid values
- Missing secrets
- Invalid paths
- Unsupported options

Invalid configuration should produce descriptive errors.

---

# Environment Types

Recommended environments:

Development

```
.env
```

Testing

```
.env.test
```

Production

```
.env.production
```

Future deployments can swap environments easily.

---

# Sensitive Data

Never store:

- API Keys
- Passwords
- Tokens
- Secrets

inside:

- Python files
- JSON configuration
- Git repository

Always use:

```
.env
```

---

# Configuration Loading Example

```
Start

↓

Load .env

↓

Load JSON

↓

Merge Values

↓

Validate

↓

Initialize Services
```

---

# Future Configuration Expansion

Future versions may introduce:

- YAML support
- Remote configuration
- Configuration hot reload
- Secret vault integration
- Cloud configuration providers

---

# Best Practices

Always:

✓ Use environment variables for secrets

✓ Use JSON for application settings

✓ Validate everything

✓ Document new settings

✓ Keep defaults reasonable

---

# Developer Workflow

When introducing new configuration:

1. Add the variable to `.env.example`
2. Update `config_manager.py`
3. Add validation
4. Update this documentation
5. Update README if user-facing

---

# Troubleshooting

Common issues include:

Missing API keys

↓

Check `.env`

---

Collector disabled

↓

Check `collectors.json`

---

Database cannot open

↓

Verify `DATABASE_PATH`

---

Playwright fails

↓

Verify browser installation

```
playwright install
```

---

# Long-Term Vision

CryptoIntel OS configuration is designed to remain modular and scalable.

As new collectors, AI providers, notification systems, and deployment targets are added, configuration should expand through centralized management rather than scattered constants.

This keeps the platform maintainable, portable, and production-ready.
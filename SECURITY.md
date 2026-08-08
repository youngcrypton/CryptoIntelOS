# Security Policy

## Reporting a vulnerability

Do not disclose suspected vulnerabilities in a public issue.

Use the repository's **Private vulnerability reporting** or **Security Advisories** feature on GitHub. Include:

- affected component and revision;
- reproducible steps or proof of concept;
- potential impact;
- suggested mitigation, if known;
- whether credentials or sensitive data may have been exposed.

Maintainers should acknowledge complete reports promptly, validate impact, coordinate remediation, and publish an advisory when appropriate. No guaranteed response or remediation timeline is currently published.

## Secrets and credentials

- Never commit `.env` files, API tokens, private keys, RPC credentials, OAuth secrets, cloud credentials, or wallet material.
- Use `.env.example` only for documented variable names and non-secret placeholders.
- Inject provider authentication through configuration and transport boundaries.
- Redact authorization headers and sensitive payloads from logs, traces, fixtures, and error reports.
- Keep live integration tests optional and isolated from pull-request workflows.

## Supported versions

Until formal release tags and maintenance windows are published, security fixes target the latest commit on the default branch.

## Scope

Reports concerning dependency vulnerabilities, credential exposure, provider authentication, transport security, canonical mapping, serialization, Runtime boundaries, or sensitive logging are in scope. Third-party service availability and vulnerabilities in external providers should be reported to their respective maintainers unless CryptoIntel OS introduces the exposure.

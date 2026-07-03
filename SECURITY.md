# Security Policy

## Supported Versions

This project is in early public preparation and has not published a stable release yet.

## Reporting a Vulnerability

Please do not open public issues for security vulnerabilities.

Report security concerns privately to the maintainer through GitHub at:

https://github.com/aaindex

Include:

- A short description of the issue.
- Steps to reproduce, if available.
- The affected component.
- Any logs or screenshots that do not expose private information.

## Security Principles

- Bind local telemetry services to trusted interfaces by default. The current Mac agent binds to `127.0.0.1`.
- Do not expose unauthenticated monitoring endpoints to the public internet.
- Do not collect more system data than the dashboard needs.
- Do not commit signing keys, tokens, passwords, or local device identifiers.

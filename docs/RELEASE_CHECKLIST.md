# Release Checklist

Use this checklist before publishing a public GitHub release.

## Repository

- README explains what the project does.
- License is present.
- Source code is committed.
- Setup instructions are tested from a clean checkout.
- Screenshots are current.
- Issue and pull request templates are present.

## Security

- No secrets are committed.
- No signing keys are committed.
- No private device IDs, serial numbers, or local IP assumptions are committed.
- Network binding and authentication behavior are documented.

## Android App

- Debug-only configuration is removed from release builds.
- App version is bumped.
- Release artifact is generated.
- Install instructions are verified on a Samsung phone.

## Mac Agent

- Startup command is documented.
- Required macOS permissions are documented.
- Telemetry commands and APIs are documented.
- Agent stops cleanly.

## GitHub

- Repository description is set.
- Topics are added.
- First release tag is created.
- Release notes include setup and known limitations.

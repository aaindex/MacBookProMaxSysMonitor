# MacBook Pro Max System Monitor

An open source monitoring system that lets a Samsung phone display live health and performance information from a MacBook Pro Max.

This project is intended for people who want a lightweight second-screen dashboard for macOS telemetry: CPU, memory, thermals, battery, storage, network, and high-signal process information surfaced on an Android phone.

## Project Status

Early public release preparation. The repository currently contains the open source project structure and documentation. The running Samsung phone app and Mac telemetry components should be added here before the first tagged release.

## Goals

- Show live MacBook Pro Max system metrics on a Samsung phone.
- Keep the Mac-side collector lightweight and local-first.
- Make setup simple for personal use on a trusted network.
- Provide a clean Android dashboard suited for always-on monitoring.
- Document the project well enough for other people to install, run, and contribute.

## Planned Components

- `mac-agent/` - macOS telemetry service that gathers system metrics.
- `android-app/` - Samsung/Android dashboard app.
- `docs/` - architecture, setup, release, and contributor documentation.
- `.github/` - GitHub issue and pull request templates.

## Recommended Repository Layout

```text
MacBookProMaxSysMonitor/
├── android-app/
├── mac-agent/
├── docs/
├── .github/
├── LICENSE
└── README.md
```

## Local Development

The app code is not yet committed to this repository. Once the code is added, this section should include:

1. macOS prerequisites.
2. Android Studio or Gradle requirements.
3. How to run the Mac telemetry agent.
4. How to install or sideload the Samsung phone app.
5. How to connect the phone to the Mac over USB, local Wi-Fi, or ADB reverse.

## Security Model

This project is designed for personal devices on a trusted local connection. It should not expose unauthenticated telemetry endpoints to the public internet.

Before the first public release, the project should document:

- Which port or transport the Mac agent uses.
- Whether telemetry is encrypted in transit.
- Whether pairing, tokens, or local-only binding are required.
- What system information is collected.

## Roadmap

See [docs/ROADMAP.md](docs/ROADMAP.md).

## Contributing

Contributions are welcome once the source code lands in the repository. Please read [CONTRIBUTING.md](CONTRIBUTING.md) and open an issue before large changes.

## License

Released under the [MIT License](LICENSE).

## Maintainer

Created and maintained by [aaindex](https://github.com/aaindex).

# MacBook Pro Max System Monitor

An open source monitoring system that lets a Samsung phone display live health and performance information from a MacBook Pro Max.

This project is intended for people who want a lightweight second-screen dashboard for macOS telemetry: CPU, memory pressure, disk, network, GPU status, and high-signal process information surfaced on an Android phone.

## Project Status

Working prototype. The current version runs a local Python server on the Mac and displays the dashboard in Samsung Internet through `adb reverse`.

## Goals

- Show live MacBook Pro Max system metrics on a Samsung phone.
- Keep the Mac-side collector lightweight and local-first.
- Make setup simple for personal use on a trusted network.
- Provide a clean Android dashboard suited for always-on monitoring.
- Document the project well enough for other people to install, run, and contribute.

## Components

- `mac-agent/` - macOS telemetry service that gathers system metrics.
- `docs/` - architecture, setup, release, and contributor documentation.
- `.github/` - GitHub issue and pull request templates.

## Repository Layout

```text
MacBookProMaxSysMonitor/
├── mac-agent/
│   ├── index.html
│   └── mac_monitor_server.py
├── docs/
├── .github/
├── LICENSE
└── README.md
```

## Run It

Requirements:

- macOS.
- Python 3.
- Android Debug Bridge (`adb`).
- A Samsung phone with USB debugging enabled.

Start the Mac agent:

```bash
cd mac-agent
python3 mac_monitor_server.py
```

In another terminal, forward the phone's local port to the Mac agent:

```bash
adb reverse tcp:8765 tcp:8765
```

On the Samsung phone, open Samsung Internet or Chrome to:

```text
http://127.0.0.1:8765
```

The dashboard refreshes every 2 seconds.

## Metrics

The prototype currently shows:

- CPU usage, core count, and load average.
- Top CPU processes.
- Memory pressure and estimated used memory.
- System volume disk usage.
- Network receive/send totals.
- Apple GPU model/status note.

## Security Model

This project is designed for personal devices on a trusted local connection. The Mac agent binds to `127.0.0.1` by default and is intended to be reached from the phone through `adb reverse`.

Do not expose the unauthenticated telemetry endpoint to the public internet.

## Roadmap

See [docs/ROADMAP.md](docs/ROADMAP.md).

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) and open an issue before large changes.

## License

Released under the [MIT License](LICENSE).

## Maintainer

Created and maintained by [aaindex](https://github.com/aaindex).

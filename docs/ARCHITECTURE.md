# Architecture

MacBook Pro Max System Monitor is a two-device local monitoring system.

## Components

### Mac Agent

The Mac agent runs on macOS and collects telemetry from local system APIs and command-line tools. It exposes a minimal HTTP API and serves the phone dashboard.

Current metrics:

- CPU load and usage.
- Memory pressure and estimated used memory.
- Disk capacity and available space.
- Network receive/send totals.
- Top resource-consuming processes.
- GPU model/status note.

### Android Dashboard

The Samsung phone currently displays the dashboard in Samsung Internet or Chrome. The dashboard is a static HTML/CSS/JavaScript page served by the Mac agent and optimized for phone display.

### Transport

The current transport is USB debugging with ADB port reverse:

```bash
adb reverse tcp:8765 tcp:8765
```

This lets the phone open `http://127.0.0.1:8765`, while the Mac agent remains bound to the Mac's loopback interface.

## Security Notes

The Mac agent defaults to `127.0.0.1`. Do not bind to public interfaces without authentication.

## Data Flow

```text
macOS system APIs/tools -> Python Mac agent -> ADB reverse -> Samsung browser dashboard
```

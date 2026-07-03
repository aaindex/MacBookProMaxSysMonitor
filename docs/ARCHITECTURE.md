# Architecture

MacBook Pro Max System Monitor is planned as a two-device local monitoring system.

## Components

### Mac Agent

The Mac agent runs on macOS and collects telemetry from local system APIs and command-line tools. It should expose only the data needed by the phone dashboard.

Candidate metrics:

- CPU load and usage.
- Memory pressure, used memory, and swap.
- Battery percentage, charging state, and cycle health where available.
- Thermal state.
- Disk capacity and available space.
- Network throughput.
- Top resource-consuming processes.

### Android Dashboard

The Samsung phone app displays live metrics from the Mac agent. It should be optimized for glanceable monitoring, persistent display, and fast reconnects.

### Transport

The project should support a trusted local connection. Possible transports include:

- Local Wi-Fi HTTP or WebSocket.
- USB with ADB reverse during development.
- A future authenticated local pairing flow.

## Security Notes

The Mac agent should default to local or trusted-network access. Do not bind to public interfaces without authentication.

## Data Flow

```text
macOS system APIs/tools -> Mac agent -> local transport -> Samsung phone dashboard
```

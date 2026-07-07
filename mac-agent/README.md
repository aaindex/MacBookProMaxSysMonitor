# Mac Agent

This folder contains the working prototype:

- `mac_monitor_server.py` - Python HTTP server and macOS telemetry collector.
- `index.html` - phone-sized dashboard served by the agent.

## Run

```bash
python3 mac_monitor_server.py
```

For live Apple GPU percent/power, allow `powermetrics` before starting or while the
server is running:

```bash
sudo -v
```

The server calls `sudo -n powermetrics --samplers gpu_power` and falls back to the
GPU model/status note when macOS has not granted privilege.

The server listens on:

```text
http://127.0.0.1:8765
```

## Samsung Phone Access

With the phone connected over USB and USB debugging enabled:

```bash
adb reverse tcp:8765 tcp:8765
```

Then open this URL on the phone:

```text
http://127.0.0.1:8765
```

## API

```text
GET /api/metrics
```

Returns live JSON metrics for CPU, memory, disk, network, GPU, host name, and top CPU processes.

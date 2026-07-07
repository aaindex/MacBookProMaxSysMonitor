#!/usr/bin/env python3
import json
import os
import re
import subprocess
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


ROOT = os.path.dirname(os.path.abspath(__file__))
START = time.time()
GPU_SAMPLE = {"time": 0.0, "data": None}


def run(cmd):
    try:
        return subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return ""


def run_with_timeout(cmd, timeout):
    try:
        return subprocess.check_output(
            cmd,
            text=True,
            stderr=subprocess.DEVNULL,
            timeout=timeout,
        ).strip()
    except Exception:
        return ""


def number(value, default=0.0):
    try:
        return float(value)
    except Exception:
        return default


def cpu_percent():
    cores = os.cpu_count() or 1
    total = 0.0
    output = run(["ps", "-A", "-o", "%cpu="])
    for line in output.splitlines():
        total += number(line.strip())
    return max(0.0, min(100.0, total / cores))


def cpu_top_processes():
    rows = []
    output = run(["ps", "-A", "-o", "%cpu=,comm="])
    for line in output.splitlines():
        match = re.match(r"\s*([0-9.]+)\s+(.+)$", line)
        if not match:
            continue
        rows.append((number(match.group(1)), os.path.basename(match.group(2))))
    rows.sort(reverse=True)
    return [{"name": name, "cpu": round(cpu, 1)} for cpu, name in rows[:5]]


def memory():
    total = number(run(["sysctl", "-n", "hw.memsize"]))
    page_size = number(run(["sysctl", "-n", "hw.pagesize"]), 4096)
    vm = run(["vm_stat"])
    values = {}
    for line in vm.splitlines():
        if ":" not in line:
            continue
        key, raw = line.split(":", 1)
        values[key.strip()] = number(raw.strip().rstrip("."))
    free_pages = values.get("Pages free", 0) + values.get("Pages speculative", 0)
    purgeable_pages = values.get("Pages purgeable", 0)
    file_backed_pages = values.get("File-backed pages", 0)
    anonymous_pages = values.get("Anonymous pages", values.get("Pages active", 0))
    compressed_pages = values.get("Pages occupied by compressor", 0)
    wired_pages = values.get("Pages wired down", 0)
    used = (anonymous_pages + wired_pages + compressed_pages) * page_size
    reclaimable = (free_pages + purgeable_pages + file_backed_pages) * page_size
    if total <= 0:
        total = used + reclaimable

    pressure_percent = None
    pressure = run(["memory_pressure"])
    match = re.search(r"System-wide memory free percentage:\s+(\d+)%", pressure)
    if match:
        pressure_percent = 100 - number(match.group(1))

    return {
        "used": used,
        "free": max(0, total - used),
        "reclaimable": reclaimable,
        "total": total,
        "percent": (
            max(0, min(100, pressure_percent))
            if pressure_percent is not None
            else 0 if total <= 0 else max(0, min(100, used / total * 100))
        ),
    }


def disk():
    stats = os.statvfs("/")
    total = stats.f_blocks * stats.f_frsize
    free = stats.f_bavail * stats.f_frsize
    used = total - free
    return {
        "used": used,
        "free": free,
        "total": total,
        "percent": 0 if total <= 0 else used / total * 100,
    }


def network():
    output = run(["netstat", "-ibn"])
    rx = tx = 0
    seen = set()
    for line in output.splitlines()[1:]:
        parts = line.split()
        if len(parts) < 10:
            continue
        iface = parts[0]
        if iface in seen or iface.startswith(("lo", "utun")):
            continue
        seen.add(iface)
        rx += int(number(parts[6]))
        tx += int(number(parts[9]))
    return {"rx": rx, "tx": tx}


def gpu():
    profile = run(["system_profiler", "SPDisplaysDataType"])
    model = "Apple GPU"
    for line in profile.splitlines():
        if "Chipset Model:" in line:
            model = line.split(":", 1)[1].strip()
            break
    data = {
        "model": model,
        "status": "Active",
        "note": "Live GPU % needs privileged powermetrics on macOS.",
    }
    power = gpu_power_metrics()
    if power:
        data.update(power)
    return data


def gpu_power_metrics():
    now = time.time()
    if GPU_SAMPLE["data"] is not None and now - GPU_SAMPLE["time"] < 8:
        return GPU_SAMPLE["data"]

    output = run_with_timeout(
        ["sudo", "-n", "powermetrics", "--samplers", "gpu_power", "-i", "1000", "-n", "1"],
        5,
    )
    parsed = parse_powermetrics_gpu(output) if output else None
    GPU_SAMPLE["time"] = now
    GPU_SAMPLE["data"] = parsed
    return parsed


def parse_powermetrics_gpu(output):
    active_match = re.search(r"GPU(?:\s+HW)?\s+active\s+residency:\s*([0-9.]+)%", output, re.I)
    power_match = re.search(r"GPU\s+Power:\s*([0-9.]+)\s*([mun]?W)", output, re.I)
    if not active_match and not power_match:
        return None

    active = number(active_match.group(1)) if active_match else None
    result = {
        "status": f"{active:.1f}%" if active is not None else "Active",
        "note": "Live GPU metrics from powermetrics.",
    }
    if active is not None:
        result["percent"] = round(active, 1)
    if power_match:
        value = number(power_match.group(1))
        unit = power_match.group(2)
        result["powerText"] = f"{value:.0f} {unit}" if unit.lower() == "mw" else f"{value:.2f} {unit}"
    return result


def bytes_human(size):
    units = ["B", "KB", "MB", "GB", "TB"]
    value = float(size)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} B"
        value /= 1024


def metrics():
    mem = memory()
    dsk = disk()
    net = network()
    load = os.getloadavg()
    return {
        "time": time.strftime("%I:%M:%S %p"),
        "uptimeSeconds": int(time.time() - START),
        "host": run(["scutil", "--get", "ComputerName"]) or "MacBook",
        "cpu": {
            "percent": round(cpu_percent(), 1),
            "cores": os.cpu_count() or 1,
            "load": [round(x, 2) for x in load],
            "top": cpu_top_processes(),
        },
        "memory": {
            **mem,
            "usedText": bytes_human(mem["used"]),
            "totalText": bytes_human(mem["total"]),
            "percent": round(mem["percent"], 1),
        },
        "disk": {
            **dsk,
            "usedText": bytes_human(dsk["used"]),
            "totalText": bytes_human(dsk["total"]),
            "percent": round(dsk["percent"], 1),
        },
        "network": {
            **net,
            "rxText": bytes_human(net["rx"]),
            "txText": bytes_human(net["tx"]),
        },
        "gpu": gpu(),
    }


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/api/metrics"):
            body = json.dumps(metrics()).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        path = "index.html" if self.path in ("/", "/index.html") else self.path.lstrip("/")
        full = os.path.join(ROOT, path)
        if not os.path.isfile(full):
            self.send_error(404)
            return
        with open(full, "rb") as f:
            body = f.read()
        content_type = "text/html; charset=utf-8" if full.endswith(".html") else "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        print("%s - %s" % (self.address_string(), fmt % args))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8765"))
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"Mac Monitor running at http://127.0.0.1:{port}")
    server.serve_forever()

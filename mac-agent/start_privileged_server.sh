#!/bin/sh
set -eu

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
PYTHON="${PYTHON:-/opt/homebrew/bin/python3}"
LOG="/private/tmp/mac_monitor_server.log"

pid="$(/usr/sbin/lsof -tiTCP:8765 -sTCP:LISTEN || true)"
if [ -n "$pid" ]; then
  /bin/kill "$pid"
  /bin/sleep 1
fi

cd "$ROOT"
"$PYTHON" mac_monitor_server.py < /dev/null > "$LOG" 2>&1 &

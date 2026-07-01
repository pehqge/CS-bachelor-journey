#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
for name in interceptor server; do
  if [[ -f "logs/$name.pid" ]]; then
    pid="$(cat "logs/$name.pid")"
    if kill "$pid" 2>/dev/null; then
      echo "matando $name (PID=$pid)"
    fi
    rm -f "logs/$name.pid"
  fi
done
echo "OK."

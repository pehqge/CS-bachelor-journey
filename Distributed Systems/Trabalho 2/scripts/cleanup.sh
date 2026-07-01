#!/bin/bash

# Stops the cluster and throws away all of its runtime state.

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( dirname "$SCRIPT_DIR" )"

cd "$PROJECT_ROOT"

echo "Stopping running replica processes..."

for pid_file in test-env/pids/node_1.pid test-env/pids/node_2.pid test-env/pids/node_3.pid; do
    if [ -f "$pid_file" ]; then
        pid=$(cat "$pid_file")
        if kill -0 "$pid" 2>/dev/null; then
            echo "Killing process $pid ($pid_file)..."
            kill -9 "$pid" 2>/dev/null
        fi
        rm -f "$pid_file"
    fi
done

# in case a pid file went missing, sweep up any leftover server
pkill -9 -f "src/server.py" 2>/dev/null

echo "Removing test-env directories..."
rm -rf test-env

echo "Cleanup complete."

#!/bin/bash

# Brings up a local 3-node cluster (1 leader, 2 followers).

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( dirname "$SCRIPT_DIR" )"

# everything below assumes we're at the project root
cd "$PROJECT_ROOT"

# wipe whatever was left from a previous run first
./scripts/cleanup.sh

mkdir -p test-env/pids
mkdir -p test-env/logs

# every node gets the full address list so a follower can find the new leader on
# its own after a leader change -- nobody has to restart or repoint it by hand
PEERS="127.0.0.1:5050,127.0.0.1:5051,127.0.0.1:5052"

echo "Starting Leader (Node 1) on port 5050..."
python3 src/server.py --role leader --host 127.0.0.1 --port 5050 --node-id node_1 --epoch 1 --snapshot-threshold 5 --peers "$PEERS" > test-env/logs/node_1.log 2>&1 &
echo $! > test-env/pids/node_1.pid

# let the leader grab its port before the followers try to reach it
sleep 1

echo "Starting Follower (Node 2) on port 5051..."
python3 src/server.py --role follower --host 127.0.0.1 --port 5051 --node-id node_2 --leader-host 127.0.0.1 --leader-port 5050 --snapshot-threshold 5 --peers "$PEERS" > test-env/logs/node_2.log 2>&1 &
echo $! > test-env/pids/node_2.pid

echo "Starting Follower (Node 3) on port 5052..."
python3 src/server.py --role follower --host 127.0.0.1 --port 5052 --node-id node_3 --leader-host 127.0.0.1 --leader-port 5050 --snapshot-threshold 5 --peers "$PEERS" > test-env/logs/node_3.log 2>&1 &
echo $! > test-env/pids/node_3.pid

echo "Cluster is up."
echo "Node 1 PID: $(cat test-env/pids/node_1.pid)"
echo "Node 2 PID: $(cat test-env/pids/node_2.pid)"
echo "Node 3 PID: $(cat test-env/pids/node_3.pid)"
echo "Logs are written to test-env/logs/ and PIDs to test-env/pids/."

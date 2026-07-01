# ===================== server.py =====================
# entry point for a replica node. wires up the application (FileSystemApp)
# and the SMR engine (ReplicationNode), then just sits there while the
# background threads do the real work.
#
# a node starts as leader or follower. a follower needs to know how to reach
# the cluster -- either a single --leader-host/--port hint, or the full --peers
# list (which also lets it rediscover the leader on its own after a flip).
# =====================================================

import argparse
import sys
import time
import logging
from filesystem_app import FileSystemApp
from replication import ReplicationNode

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("ServerEntry")

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Distributed Filesystem Replica Node (SMR)")
    parser.add_argument("--role", choices=["leader", "follower"], required=True, help="Role of this node in the cluster")
    parser.add_argument("--host", default="127.0.0.1", help="Binding address of this node")
    parser.add_argument("--port", type=int, required=True, help="Port of this node")
    parser.add_argument("--node-id", required=True, help="Unique identifier of this node (e.g., node_1)")
    parser.add_argument("--leader-host", help="Leader's IP address (initial hint for followers)")
    parser.add_argument("--leader-port", type=int, help="Leader's port (initial hint for followers)")
    parser.add_argument("--epoch", type=int, default=1, help="Starting epoch number for the leader")
    parser.add_argument("--snapshot-threshold", type=int, default=1000, help="Log threshold to trigger snapshotting")
    parser.add_argument("--peers", help="Comma-separated host:port of the full cluster; lets followers rediscover the leader on their own after a leader change")
    return parser.parse_args()

def parse_peers(peers_str):
    # "h1:p1,h2:p2" -> [(h1, p1), (h2, p2)]
    peers = []
    if not peers_str:
        return peers
    for pair in peers_str.split(","):
        pair = pair.strip()
        if not pair:
            continue
        host, port = pair.split(":")
        peers.append((host, int(port)))
    return peers

def main() -> None:
    args = parse_arguments()

    peers = parse_peers(args.peers)

    # a follower has to know where to start: either an explicit leader hint or
    # the full peer list it can discover the leader from
    if args.role == "follower" and not peers and (not args.leader_host or not args.leader_port):
        logger.error("Follower role requires --peers or --leader-host/--leader-port")
        sys.exit(1)

    logger.info(f"Starting {args.role} node '{args.node_id}' on {args.host}:{args.port}")

    # app layer first -- it creates its own storage sandbox on disk
    app = FileSystemApp(args.node_id)

    # then the SMR engine that drives consensus / replication
    replication_node = ReplicationNode(
        node_id=args.node_id,
        role=args.role,
        host=args.host,
        port=args.port,
        leader_host=args.leader_host,
        leader_port=args.leader_port,
        epoch=args.epoch,
        snapshot_threshold=args.snapshot_threshold,
        peers=peers
    )

    # hand the app to the engine so delivered ops get applied to the filesystem
    replication_node.set_app_listener(app)

    # spins up the networking threads (server loop + heartbeat/follower client)
    replication_node.start()

    # nothing left to do on the main thread -- just keep the process alive
    try:
        while True:
            time.sleep(1.0)
    except KeyboardInterrupt:
        logger.info("Shutdown signal received. Stopping node...")
        replication_node.is_running = False

if __name__ == "__main__":
    main()

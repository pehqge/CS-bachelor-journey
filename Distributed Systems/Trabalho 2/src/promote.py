# ===================== promote.py =====================
# tiny admin tool: promotes one running follower to leader in place, no restart.
#
#   usage:  python3 src/promote.py <host> <port>
#
# this is the manual, operator-driven reconfiguration step. leader election is a
# separate building block and intentionally out of scope: a human (or a script)
# picks one up-to-date follower and promotes it, and the surviving followers
# then find the new leader on their own through their static peer list.
# =====================================================

import socket
import sys

import replication.protocol as protocol


def promote(host: str, port: int) -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3.0)
    sock.connect((host, port))
    sock.sendall(bytes([protocol.OP_PROMOTE]))
    try:
        # best-effort: read the leader's ack frame, then close
        sock.recv(64)
    except socket.timeout:
        pass
    finally:
        sock.close()
    print(f"Promote command sent to {host}:{port}")


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: python3 src/promote.py <host> <port>")
        sys.exit(1)
    promote(sys.argv[1], int(sys.argv[2]))


if __name__ == "__main__":
    main()

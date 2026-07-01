# ===================== client.py =====================
# interactive CLI client. talks to the cluster over a raw TCP socket using
# the app protocol (no HTTP, no JSON on the wire except the list dump).
#
# the client is handed the *whole* node list and finds the leader itself:
# if it lands on a follower it gets a WRONG_LEADER redirect, and it skips
# dead nodes. so from the user's side replication is transparent -- you
# never tell it which node is the leader.
# =====================================================

import argparse
import socket
import sys
import os
import uuid
import json
import shlex
import logging
from typing import List, Tuple, Optional
import app_protocol as protocol
import replication.protocol as rep_protocol
from replication import Communicator

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("Client")

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Distributed Filesystem Client CLI")
    parser.add_argument("--nodes", required=True, help="Comma-separated list of host:port pairs of cluster nodes")
    return parser.parse_args()

def parse_nodes(nodes_str: str) -> List[Tuple[str, int]]:
    # "h1:p1,h2:p2" -> [(h1, p1), (h2, p2)]
    nodes = []
    for pair in nodes_str.split(","):
        try:
            host, port = pair.strip().split(":")
            nodes.append((host, int(port)))
        except ValueError:
            logger.error(f"Invalid node format: {pair}")
    return nodes

class DFSClient:
    def __init__(self, nodes: List[Tuple[str, int]]):
        self.nodes = nodes
        self.sock: Optional[socket.socket] = None
        self.comm: Optional[Communicator] = None
        self.connect()

    def connect(self) -> None:
        # walk the node list until something answers; follow the redirect if
        # we hit a follower
        for host, port in self.nodes:
            try:
                logger.info(f"Connecting to node {host}:{port}...")
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((host, port))
                sock.sendall(bytes([rep_protocol.OP_I_AM_CLIENT]))

                # a follower answers right away with a WRONG_LEADER frame; the
                # real leader stays quiet, so a short read timeout tells them apart
                sock.settimeout(0.5)
                try:
                    comm = Communicator(sock)
                    frame = comm.receive_frame()
                    if len(frame) >= 9:
                        _, _, opcode = rep_protocol.unpack_replication_header(frame[:9])
                        if opcode == rep_protocol.OP_WRONG_LEADER:
                            leader_host, leader_port = rep_protocol.unpack_wrong_leader(frame[9:])
                            logger.info(f"Redirected to Leader at {leader_host}:{leader_port}")
                            sock.close()

                            # reconnect straight to the real leader
                            leader_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            leader_sock.connect((leader_host, leader_port))
                            leader_sock.sendall(bytes([rep_protocol.OP_I_AM_CLIENT]))
                            leader_sock.settimeout(60.0)
                            self.sock = leader_sock
                            self.comm = Communicator(leader_sock, timeout=60.0)
                            logger.info("Successfully connected to Leader.")
                            return
                except socket.timeout:
                    # silence == this node is the leader
                    sock.settimeout(60.0)
                    self.sock = sock
                    self.comm = Communicator(sock, timeout=60.0)
                    logger.info("Connected to Leader.")
                    return
                except Exception as e:
                    logger.warning(f"Error checking node handshake: {e}")
                sock.close()
            except Exception as e:
                logger.warning(f"Failed to connect to node {host}:{port}: {e}")

        raise ConnectionError("Could not connect to any cluster node or find the active Leader.")

    def close(self) -> None:
        if self.comm:
            self.comm.close()

    def list_files(self) -> None:
        if not self.comm:
            return
        try:
            request = bytes([protocol.OP_LIST_REQUEST])
            self.comm.send_frame(request)

            response = self.comm.receive_frame()
            json_str = protocol.unpack_app_list_response(response)
            files = json.loads(json_str)

            if not files:
                print("No files stored in DFS.")
                return

            print("\nFiles in Distributed Filesystem:")
            print(f"{'Filename':<30} | {'Size (Bytes)':<15} | {'Upload Time':<20}")
            print("-" * 71)
            for filename, info in files.items():
                print(f"{filename:<30} | {info['size']:<15} | {info['uploaded_at']:<20}")
            print()
        except Exception as e:
            logger.error(f"List command failed: {e}")
            self._handle_disconnect()

    def delete_file(self, filename: str) -> None:
        if not self.comm:
            return
        try:
            payload = protocol.pack_app_delete(filename)
            request = bytes([protocol.OP_DELETE_FILE]) + payload
            self.comm.send_frame(request)

            response = self.comm.receive_frame()
            if response[0] == 0x00:
                print(f"Successfully deleted file: {filename}")
            else:
                print(f"Failed to delete file: {filename}")
        except Exception as e:
            logger.error(f"Delete command failed: {e}")
            self._handle_disconnect()

    def download_file(self, remote_name: str, local_path: str) -> None:
        if not self.comm:
            return
        try:
            payload = protocol.pack_app_read_request(remote_name)
            request = bytes([protocol.OP_READ_REQUEST]) + payload
            self.comm.send_frame(request)

            response = self.comm.receive_frame()
            status, content = protocol.unpack_app_read_response(response)

            if status == 0:
                with open(local_path, "wb") as f:
                    f.write(content)
                print(f"Successfully downloaded file to: {local_path}")
            else:
                print(f"Failed to download file: {content.decode('utf-8')}")
        except Exception as e:
            logger.error(f"Download command failed: {e}")
            self._handle_disconnect()

    def upload_file(self, local_path: str, remote_name: str) -> None:
        if not self.comm:
            return
        if not os.path.exists(local_path):
            print(f"Local file does not exist: {local_path}")
            return

        # one upload = one session uuid. keeps concurrent uploads of the same
        # name from stepping on each other (chunks land in separate .part files)
        session_uuid = uuid.uuid4()

        try:
            # START: open the session
            start_payload = protocol.pack_app_start(session_uuid)
            self.comm.send_frame(bytes([protocol.OP_START]) + start_payload)
            response = self.comm.receive_frame()
            if response[0] != 0x00:
                print("Failed to initialize file upload session.")
                return

            # CHUNK: stream the file 4MB at a time so we never load it all in RAM
            chunk_size = 4 * 1024 * 1024  # 4MB
            total_size = os.path.getsize(local_path)
            uploaded = 0

            with open(local_path, "rb") as f:
                while True:
                    chunk_data = f.read(chunk_size)
                    if not chunk_data:
                        break

                    chunk_payload = protocol.pack_app_chunk(session_uuid, chunk_data)
                    self.comm.send_frame(bytes([protocol.OP_CHUNK]) + chunk_payload)
                    response = self.comm.receive_frame()
                    if response[0] != 0x00:
                        print("Failed during file chunk upload.")
                        return

                    uploaded += len(chunk_data)
                    print(f"Uploaded {uploaded}/{total_size} bytes ({(uploaded/total_size)*100:.1f}%)")

            # COMMIT: atomically rename .part -> final name (leader picks the name)
            commit_payload = protocol.pack_app_commit(session_uuid, remote_name)
            self.comm.send_frame(bytes([protocol.OP_COMMIT]) + commit_payload)
            response = self.comm.receive_frame()
            if response[0] == 0x00:
                print(f"Successfully committed file upload as: {remote_name}")
            else:
                print("Failed to commit file upload.")
        except Exception as e:
            logger.error(f"Upload command failed: {e}")
            self._handle_disconnect()

    def _handle_disconnect(self) -> None:
        # lost the leader mid-command -> try to find it again from scratch
        logger.warning("Disconnected from leader. Attempting to reconnect...")
        self.close()
        try:
            self.connect()
        except Exception as e:
            logger.error(f"Reconnection failed: {e}")
            self.sock = None
            self.comm = None


def main() -> None:
    args = parse_args()
    nodes = parse_nodes(args.nodes)

    try:
        client = DFSClient(nodes)
    except Exception as e:
        logger.error(f"Initialization error: {e}")
        sys.exit(1)

    print("\nDistributed Filesystem CLI Client")
    print("Commands:")
    print("  upload <local_path> <remote_name>")
    print("  download <remote_name> <local_path>")
    print("  list")
    print("  delete <remote_name>")
    print("  exit")
    print('  (tip: quote names with spaces, e.g. delete "file (1).txt")\n')

    while True:
        try:
            cmd_line = input("DFS> ").strip()
            if not cmd_line:
                continue

            # shlex preserves filenames containing spaces when quoted, e.g.
            #   delete "relatorio (1).pdf"
            try:
                parts = shlex.split(cmd_line)
            except ValueError as e:
                print(f"Invalid command syntax: {e}")
                continue
            if not parts:
                continue
            cmd = parts[0].lower()

            if cmd == "exit":
                client.close()
                break
            elif cmd == "list":
                if len(parts) != 1:
                    print("Usage: list")
                else:
                    client.list_files()
            elif cmd == "delete":
                if len(parts) != 2:
                    print("Usage: delete <remote_name>")
                else:
                    client.delete_file(parts[1])
            elif cmd == "download":
                if len(parts) != 3:
                    print("Usage: download <remote_name> <local_path>")
                else:
                    client.download_file(parts[1], parts[2])
            elif cmd == "upload":
                if len(parts) != 3:
                    print("Usage: upload <local_path> <remote_name>")
                else:
                    client.upload_file(parts[1], parts[2])
            else:
                print(f"Unknown command: {cmd}")
        except KeyboardInterrupt:
            print("\nExiting CLI Client.")
            client.close()
            break
        except Exception as e:
            logger.error(f"Unexpected CLI error: {e}")

if __name__ == "__main__":
    main()

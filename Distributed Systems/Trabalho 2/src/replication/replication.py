# ===================== replication.py =====================
# the SMR engine -- the actual "building block". this is the reusable bit:
# it knows about leaders, followers, sequencing, ACKs, heartbeats, catch-up
# and snapshots, but it does NOT know what a file is. it moves opaque byte
# payloads around in a total order and hands them to whatever AppListener is
# plugged in. swap FileSystemApp for a key-value store and this wouldn't change.
#
# leader: sequences client writes, broadcasts them, blocks on follower ACKs.
# follower: discovers the leader, connects, catches up, applies the live stream.
# a follower can also be promoted to leader at runtime, with no restart.
# =========================================================

import threading
import time
import socket
import logging
import struct
from typing import Dict, List, Tuple, Optional, Set
from .communicator import Communicator
from . import protocol

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("ReplicationNode")

class AppListener:
    # the seam between consensus and the application. the engine talks to the
    # app only through these methods, so it stays oblivious to filesystem stuff.

    def on_deliver(self, sequence_id: int, payload: bytes) -> bool:
        # a sequenced op is ready to apply to the state machine
        raise NotImplementedError()

    def execute_snapshot(self, sequence_id: int) -> bool:
        # dump a snapshot and return True if it worked
        raise NotImplementedError()

    def get_latest_snapshot(self) -> Optional[Tuple[int, bytes]]:
        # (seq, raw bytes) of the newest snapshot, or None
        raise NotImplementedError()

    def load_snapshot(self, snapshot_path: str) -> bool:
        # restore state from a snapshot archive on disk
        raise NotImplementedError()

    def preprocess_request(self, request: bytes) -> Tuple[bool, bytes, bytes]:
        # runs on the leader before sequencing. returns:
        #   is_write           -> True if it modifies state and must be sequenced
        #   immediate_response -> what to send back (now, or after sequencing)
        #   proposed_payload   -> the (possibly rewritten) payload to propose
        raise NotImplementedError()


class ReplicationNode:
    def __init__(
        self,
        node_id: str,
        role: str,
        host: str,
        port: int,
        leader_host: Optional[str] = None,
        leader_port: Optional[int] = None,
        epoch: int = 1,
        snapshot_threshold: int = 1000,
        peers: Optional[List[Tuple[str, int]]] = None
    ):
        self.node_id = node_id
        self.role = role  # "leader" or "follower"
        self.host = host
        self.port = port
        self.leader_host = leader_host
        self.leader_port = leader_port

        # full static cluster membership (every node's host:port, us included).
        # followers use it to find the leader again after a leader change without
        # being restarted or repointed by hand. it's plain config, not a
        # membership/election building block: the set is fixed at boot.
        self.peers: List[Tuple[str, int]] = peers or []
        # the live follower->leader connection, so a runtime promotion can close
        # it, break a blocked recv() and let the follower loop notice and exit.
        self.follower_comm: Optional[Communicator] = None
        # don't start the heartbeat thread twice across a promotion
        self._heartbeat_started = (role == "leader")

        self.current_epoch = epoch
        self.current_sequence_id = 0
        self.expected_sequence_id = 1

        self.snapshot_threshold = snapshot_threshold
        self.app_listener: Optional[AppListener] = None

        # runtime state
        self.is_running = True
        self.state = "ACTIVE"  # "ACTIVE" or "RECOVERING"
        self.in_memory_log: Dict[int, bytes] = {}

        # locks
        self.lock = threading.Lock()
        # serializes the resolve -> sequence -> deliver path for client writes so
        # that concurrent ops (e.g. two COMMITs for the same filename) get ordered
        # deterministically by the sequencer instead of racing in preprocess_request.
        self.write_lock = threading.Lock()
        self.ack_events: Dict[int, Dict[str, threading.Event]] = {}  # seq -> {follower_node_id: Event}

        # leader-side connection tracking
        self.active_followers: Dict[str, Tuple[Communicator, socket.socket]] = {}  # node_id -> (comm, socket)
        self.active_clients: Set[socket.socket] = set()

        # follower-side buffering during recovery
        self.recovery_queue: List[bytes] = []
        self.catchup_target_seq: int = -1

    def set_app_listener(self, listener: AppListener) -> None:
        # plug in the app, and seed our sequence counters from whatever it last
        # persisted -- so a rebooted node resumes instead of starting from 0
        self.app_listener = listener
        last_seq = listener.last_applied_sequence_id
        if self.role == "leader":
            self.current_sequence_id = last_seq
            logger.info(f"Leader initialized sequence tracking to current_sequence_id={self.current_sequence_id}")
        else:
            self.expected_sequence_id = last_seq + 1
            logger.info(f"Follower initialized sequence tracking to expected_sequence_id={self.expected_sequence_id}")

    def start(self) -> None:
        # everything runs on background threads; the server loop is always on,
        # plus heartbeats (leader) or the follower client loop (follower)
        threading.Thread(target=self._run_server, daemon=True).start()
        if self.role == "leader":
            threading.Thread(target=self._run_heartbeat_loop, daemon=True).start()
        else:
            threading.Thread(target=self._run_follower_client, daemon=True).start()

    def promote_to_leader(self) -> None:
        # turn this follower into the leader on the spot -- no restart. an operator
        # aims this at one chosen, up-to-date follower. we bump the epoch so the new
        # leader outranks any stale broadcast from a recovered ghost leader (lower
        # epoch -> rejected by the followers). the other followers aren't touched;
        # they find us on their own through the peer list. it's a deliberate
        # reconfiguration step, not an election algorithm.
        with self.lock:
            if self.role == "leader":
                return
            self.role = "leader"
            self.current_epoch += 1
            # pick the sequencing back up exactly where the log left off
            self.current_sequence_id = self.expected_sequence_id - 1
            self.state = "ACTIVE"
            # as leader, redirect targets are now ourselves
            self.leader_host, self.leader_port = self.host, self.port
            start_heartbeat = not self._heartbeat_started
            self._heartbeat_started = True

        logger.info(
            f"PROMOTED to leader. epoch={self.current_epoch}, "
            f"resuming sequence at {self.current_sequence_id}"
        )

        # if the follower loop is mid-session on a live socket, closing it raises
        # in recv() so the loop sees role != follower and bails out
        if self.follower_comm:
            self.follower_comm.close()

        if start_heartbeat:
            threading.Thread(target=self._run_heartbeat_loop, daemon=True).start()

    # ================= Leader Operations =================

    def propose_operation(self, app_payload: bytes) -> bool:
        # assign the next seq, log it, broadcast, then block until the followers
        # ACK (or get dropped). only after that do we apply it locally.
        with self.lock:
            self.current_sequence_id += 1
            seq = self.current_sequence_id
            epoch = self.current_epoch
            self.in_memory_log[seq] = app_payload

            # one ACK event per follower we expect to hear back from
            followers_to_wait = list(self.active_followers.keys())
            self.ack_events[seq] = {fid: threading.Event() for fid in followers_to_wait}

        header = protocol.pack_replication_header(epoch, seq, protocol.OP_APP_DATA)
        frame = header + app_payload

        self._broadcast_to_followers(frame)

        success = self._wait_for_acks(seq, followers_to_wait)

        # apply on the leader too
        if self.app_listener:
            self.app_listener.on_deliver(seq, app_payload)

        self._check_snapshot_threshold(seq)

        return success

    def _broadcast_to_followers(self, frame: bytes) -> None:
        with self.lock:
            for fid, (comm, _) in list(self.active_followers.items()):
                try:
                    comm.send_frame(frame)
                except Exception:
                    logger.warning(f"Failed to broadcast to follower {fid}. Dropping node.")
                    self._drop_follower(fid)

    def _wait_for_acks(self, seq: int, followers: List[str]) -> bool:
        # wait for each follower's ACK, but only up to a timeout. a follower that
        # doesn't answer in time gets dropped (the Drop Rule) so one dead node
        # can't freeze the whole cluster.
        timeout_seconds = 2.0
        start_time = time.time()

        for fid in followers:
            elapsed = time.time() - start_time
            remaining = max(0.1, timeout_seconds - elapsed)

            with self.lock:
                event = self.ack_events[seq].get(fid)

            if event:
                acquired = event.wait(timeout=remaining)
                if not acquired:
                    logger.warning(f"Follower {fid} failed to ACK sequence {seq} in time. Dropping.")
                    self._drop_follower(fid)

        with self.lock:
            if seq in self.ack_events:
                del self.ack_events[seq]
        return True

    def _drop_follower(self, node_id: str) -> None:
        # kick a follower out: forget it and close its socket
        with self.lock:
            if node_id in self.active_followers:
                comm, sock = self.active_followers.pop(node_id)
                comm.close()
                logger.info(f"Evicted follower node: {node_id}")

    def _check_snapshot_threshold(self, seq: int) -> None:
        # every `threshold` ops, snapshot and drop the now-redundant log entries
        if seq % self.snapshot_threshold == 0:
            logger.info(f"Log threshold reached at sequence {seq}. Triggering snapshot...")
            if self.app_listener and self.app_listener.execute_snapshot(seq):
                with self.lock:
                    self.in_memory_log = {k: v for k, v in self.in_memory_log.items() if k > seq}
                logger.info(f"Log successfully truncated up to sequence {seq}")

    def _run_server(self) -> None:
        # accept loop -- followers and clients both land here first
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((self.host, self.port))
        server_sock.listen(10)
        logger.info(f"Node listening on {self.host}:{self.port}")

        while self.is_running:
            try:
                sock, addr = server_sock.accept()
                threading.Thread(target=self._handle_incoming_connection, args=(sock,), daemon=True).start()
            except Exception as e:
                logger.error(f"Error accepting connection: {e}")

    def _handle_incoming_connection(self, sock: socket.socket) -> None:
        # first byte is an identity handshake telling us who's calling and why
        comm = Communicator(sock, timeout=5.0)
        try:
            identity_bytes = sock.recv(1)
            if not identity_bytes:
                return

            opcode = identity_bytes[0]
            if opcode == protocol.OP_I_AM_FOLLOWER:
                if self.role == "leader":
                    self._handle_follower_handshake(comm, sock)
                else:
                    logger.warning("Follower received follower connection. Rejects.")
                    sock.close()
            elif opcode == protocol.OP_I_AM_CLIENT:
                if self.role == "leader":
                    self._handle_client_connection(comm, sock)
                else:
                    # client hit a follower -> hand it the leader address. the
                    # follower's discovery loop keeps leader_host/port fresh, so
                    # this points at the CURRENT leader even after a promotion.
                    logger.info("Redirecting client to the true Leader.")
                    redirection_payload = protocol.pack_wrong_leader(self.leader_host, self.leader_port)
                    header = protocol.pack_replication_header(self.current_epoch, 0, protocol.OP_WRONG_LEADER)
                    comm.send_frame(header + redirection_payload)
                    sock.close()
            elif opcode == protocol.OP_WHO_IS_LEADER:
                # leader-discovery probe. only a leader answers (with its epoch in
                # the header); followers stay quiet and the prober moves on. the
                # prober keeps whichever announcer has the highest epoch.
                if self.role == "leader":
                    header = protocol.pack_replication_header(self.current_epoch, 0, protocol.OP_LEADER_ANNOUNCE)
                    comm.send_frame(header)
                sock.close()
            elif opcode == protocol.OP_PROMOTE:
                # admin command: flip this follower to leader
                logger.info("Received PROMOTE admin command.")
                self.promote_to_leader()
                try:
                    ack = protocol.pack_replication_header(self.current_epoch, 0, protocol.OP_LEADER_ANNOUNCE)
                    comm.send_frame(ack)
                except Exception:
                    pass
                sock.close()
            else:
                logger.warning(f"Unknown connection identity opcode: {hex(opcode)}")
                sock.close()
        except Exception as e:
            logger.error(f"Connection setup failed: {e}")
            sock.close()

    def _handle_follower_handshake(self, comm: Communicator, sock: socket.socket) -> None:
        # register the follower, then sit in its read loop
        try:
            node_id_bytes = comm.receive_frame()
            node_id = node_id_bytes.decode('utf-8')

            # longer timeout now that it's an active session
            sock.settimeout(10.0)

            with self.lock:
                # if it was already connected, drop the stale one first
                if node_id in self.active_followers:
                    self._drop_follower(node_id)
                self.active_followers[node_id] = (comm, sock)
                logger.info(f"Follower {node_id} successfully connected.")

            self._run_follower_reader(node_id, comm)
        except Exception as e:
            logger.error(f"Follower registration failed: {e}")
            sock.close()

    def _run_follower_reader(self, node_id: str, comm: Communicator) -> None:
        # leader side: read ACKs and catch-up requests coming back from a follower
        while self.is_running:
            try:
                frame = comm.receive_frame()
                if len(frame) < 9:
                    continue
                epoch, seq, opcode = protocol.unpack_replication_header(frame[:9])

                if opcode == protocol.OP_REPLICATION_ACK:
                    self._handle_replication_ack(node_id, seq)
                elif opcode == protocol.OP_CATCHUP_REQUEST:
                    self._handle_catchup_request(comm, frame[9:])
            except Exception:
                logger.warning(f"Follower {node_id} reader crashed or disconnected.")
                self._drop_follower(node_id)
                break

    def _handle_replication_ack(self, node_id: str, seq: int) -> None:
        # an ACK arrived -> wake up whoever is blocked in _wait_for_acks for it
        with self.lock:
            if seq in self.ack_events and node_id in self.ack_events[seq]:
                self.ack_events[seq][node_id].set()

    def _handle_catchup_request(self, comm: Communicator, payload: bytes) -> None:
        # a follower wants to catch up from `follower_seq`. if we still have the
        # missing ops in the log, stream them; otherwise it's too far behind and
        # we send a full snapshot, then stream whatever happened after it.
        follower_seq, = struct.unpack("!I", payload)
        logger.info(f"Follower requested catchup starting from sequence {follower_seq}")

        with self.lock:
            current_seq = self.current_sequence_id

        # first tell the follower our current seq -- that's its catch-up target
        header = protocol.pack_replication_header(self.current_epoch, current_seq, protocol.OP_CATCHUP_REQUEST)
        comm.send_frame(header)

        # do we still have every op it's missing?
        in_log = True
        with self.lock:
            for seq in range(follower_seq + 1, current_seq + 1):
                if seq not in self.in_memory_log:
                    in_log = False
                    break

        if in_log:
            logger.info("Streaming missed SMR operations to follower...")
            with self.lock:
                for seq in range(follower_seq + 1, current_seq + 1):
                    app_payload = self.in_memory_log[seq]
                    header = protocol.pack_replication_header(self.current_epoch, seq, protocol.OP_APP_DATA)
                    comm.send_frame(header + app_payload)
        else:
            logger.info("Requested sequence too old. Transmitting snapshot...")
            if self.app_listener:
                snapshot_info = self.app_listener.get_latest_snapshot()
                if snapshot_info:
                    snapshot_seq, snapshot_bytes = snapshot_info
                    header = protocol.pack_replication_header(self.current_epoch, snapshot_seq, protocol.OP_SNAPSHOT_TRANSMIT)
                    comm.send_frame(header + snapshot_bytes)

                    # the snapshot only covers up to snapshot_seq, so stream the rest
                    logger.info(f"Streaming remaining logs after snapshot: {snapshot_seq + 1} to {current_seq}")
                    with self.lock:
                        for seq in range(snapshot_seq + 1, current_seq + 1):
                            if seq in self.in_memory_log:
                                app_payload = self.in_memory_log[seq]
                                header = protocol.pack_replication_header(self.current_epoch, seq, protocol.OP_APP_DATA)
                                comm.send_frame(header + app_payload)
                else:
                    logger.error("No snapshot available to transmit!")

    def _handle_client_connection(self, comm: Communicator, sock: socket.socket) -> None:
        logger.info("Client connected.")
        # interactive CLI -> no timeout, the user may idle between commands
        sock.settimeout(None)
        while self.is_running:
            try:
                frame = comm.receive_frame()
                if len(frame) < 1:
                    continue

                if not self.app_listener:
                    continue

                # hold write_lock across the whole resolve -> sequence -> deliver
                # path. preprocess_request resolves the filename collision and
                # propose_operation delivers/mutates the directory, so keeping
                # both under one lock means two concurrent COMMITs for the same
                # name get ordered: the second sees the first's entry and gets the
                # right "(1)" suffix instead of silently clobbering it.
                with self.write_lock:
                    is_write, immediate_response, proposed_payload = self.app_listener.preprocess_request(frame)
                    if is_write:
                        success = self.propose_operation(proposed_payload)
                        response = immediate_response if success else struct.pack("!B", 0x01)
                    else:
                        response = immediate_response

                comm.send_frame(response)
            except Exception as e:
                logger.info(f"Client disconnected: {e}")
                break
        sock.close()

    def _run_heartbeat_loop(self) -> None:
        # leader pings the followers every couple seconds so they know it's alive
        while self.is_running:
            time.sleep(2.0)
            if not self.active_followers:
                continue
            with self.lock:
                epoch = self.current_epoch
                seq = self.current_sequence_id
            header = protocol.pack_replication_header(epoch, seq, protocol.OP_HEARTBEAT)
            self._broadcast_to_followers(header)

    # ================= Follower Operations =================

    def _discover_leader(self) -> Optional[Tuple[str, int]]:
        # find the current leader by probing every peer (pull discovery). send
        # OP_WHO_IS_LEADER to each one; only a leader answers, carrying its epoch.
        # the highest-epoch claimant wins, so a freshly promoted leader (epoch N+1)
        # always beats a recovered ghost leader (epoch N). returns None if nobody
        # claims it yet (e.g. mid-promotion) -- the caller just retries.
        #
        # with no peer list, fall back to the boot-time leader address so a minimal
        # single-leader setup still works.
        if not self.peers:
            if self.leader_host and self.leader_port:
                return self.leader_host, self.leader_port
            return None

        best: Optional[Tuple[int, str, int]] = None  # (epoch, host, port)
        for host, port in self.peers:
            if (host, port) == (self.host, self.port):
                continue
            sock = None
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1.0)
                sock.connect((host, port))
                sock.sendall(bytes([protocol.OP_WHO_IS_LEADER]))
                comm = Communicator(sock, timeout=1.0)
                frame = comm.receive_frame()
                if len(frame) >= 9:
                    epoch, _, opcode = protocol.unpack_replication_header(frame[:9])
                    if opcode == protocol.OP_LEADER_ANNOUNCE and (best is None or epoch > best[0]):
                        best = (epoch, host, port)
            except Exception:
                # peer down or not a leader -> just skip it
                pass
            finally:
                if sock is not None:
                    try:
                        sock.close()
                    except OSError:
                        pass

        if best is not None:
            return best[1], best[2]
        return None

    def _run_follower_client(self) -> None:
        # follower side: find the current leader, connect, replicate. when the
        # leader dies the connection drops and we loop back to discovery, latching
        # onto whoever is leader now -- no restart, no hand repointing. if THIS node
        # gets promoted, role flips and the loop exits.
        while self.is_running and self.role == "follower":
            leader = self._discover_leader()
            if leader is None:
                # no leader right now (old one died, none promoted yet) -> wait
                time.sleep(1.5)
                continue

            host, port = leader
            try:
                # keep WRONG_LEADER redirects pointing at the leader we found
                with self.lock:
                    self.leader_host, self.leader_port = host, port

                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                logger.info(f"Connecting to Leader at {host}:{port}")
                sock.connect((host, port))

                # identify ourselves as a follower, then send our node id
                sock.sendall(bytes([protocol.OP_I_AM_FOLLOWER]))

                comm = Communicator(sock, timeout=6.0)
                self.follower_comm = comm
                comm.send_frame(self.node_id.encode('utf-8'))

                # enter recovery and ask for everything past our last seq
                self.state = "RECOVERING"
                self.recovery_queue = []
                self.catchup_target_seq = -1

                catchup_header = protocol.pack_replication_header(self.current_epoch, 0, protocol.OP_CATCHUP_REQUEST)
                payload = struct.pack("!I", self.expected_sequence_id - 1)
                comm.send_frame(catchup_header + payload)

                self._run_follower_receiver(comm)
            except Exception as e:
                logger.error(f"Follower lost connection or failed to connect: {e}")
                time.sleep(1.5)
            finally:
                self.follower_comm = None

    def _run_follower_receiver(self, comm: Communicator) -> None:
        # main follower loop: read frames from the leader and dispatch them
        while self.is_running and self.role == "follower":
            frame = comm.receive_frame()
            if len(frame) < 9:
                continue
            epoch, seq, opcode = protocol.unpack_replication_header(frame[:9])

            # epoch guard: ignore a stale (ghost) leader, adopt a newer one
            if epoch < self.current_epoch:
                logger.warning(f"Stale leader detected. Rejected Epoch {epoch} (current is {self.current_epoch})")
                continue
            if epoch > self.current_epoch:
                with self.lock:
                    self.current_epoch = epoch

            if self.state == "RECOVERING":
                if opcode == protocol.OP_CATCHUP_REQUEST:
                    # leader told us its current seq -> that's our target
                    self.catchup_target_seq = seq
                    logger.info(f"Catchup target sequence set to {self.catchup_target_seq}")
                    self._check_catchup_completion()
                elif opcode == protocol.OP_SNAPSHOT_TRANSMIT:
                    self._apply_snapshot(frame[9:], seq)
                    self._check_catchup_completion()
                elif opcode == protocol.OP_APP_DATA:
                    if seq == self.expected_sequence_id:
                        if self.app_listener and self.app_listener.on_deliver(seq, frame[9:]):
                            self.expected_sequence_id = seq + 1
                            self._check_snapshot_threshold(seq)
                        self._check_catchup_completion()
                    else:
                        # not our turn yet -> stash it until we get there
                        self.recovery_queue.append(frame)
            else:
                self._apply_replication_message(comm, opcode, seq, frame[9:])

    def _apply_replication_message(self, comm: Communicator, opcode: int, seq: int, payload: bytes) -> None:
        # live (post-recovery) path: apply an op and ACK it, or answer a heartbeat
        if opcode == protocol.OP_HEARTBEAT:
            ack = protocol.pack_replication_header(self.current_epoch, seq, protocol.OP_REPLICATION_ACK)
            comm.send_frame(ack)
            return

        if seq != self.expected_sequence_id:
            logger.warning(f"Out of order sequence received. Expected {self.expected_sequence_id}, got {seq}")
            return

        if opcode == protocol.OP_APP_DATA:
            if self.app_listener and self.app_listener.on_deliver(seq, payload):
                self.expected_sequence_id = seq + 1
                self._check_snapshot_threshold(seq)
                # ACK only goes out *after* on_deliver fsync'd it -> durable
                ack = protocol.pack_replication_header(self.current_epoch, seq, protocol.OP_REPLICATION_ACK)
                comm.send_frame(ack)

    def _apply_snapshot(self, snapshot_payload: bytes, snapshot_seq: int) -> None:
        # dump the incoming snapshot to a temp file and let the app restore from it
        logger.info(f"Applying snapshot up to sequence {snapshot_seq}")
        if self.app_listener:
            import os
            formatted_node_id = self.node_id.replace("_", "-")
            storage_dir = f"test-env/{formatted_node_id}-fs"
            os.makedirs(storage_dir, exist_ok=True)
            filename = f"{storage_dir}/snapshot_incoming.tar.gz"
            with open(filename, "wb") as f:
                f.write(snapshot_payload)
            if self.app_listener.load_snapshot(filename):
                self.expected_sequence_id = snapshot_seq + 1
                logger.info("Snapshot successfully loaded by application.")
            else:
                logger.error("Application failed to load snapshot!")

    def _flush_recovery_queue(self) -> None:
        # recovery done -> drain the frames we buffered while restoring, in order
        self.state = "ACTIVE"
        logger.info("Transitioning to ACTIVE state. Processing buffered messages...")

        # sort by seq so we apply them in the right order
        self.recovery_queue.sort(key=lambda f: protocol.unpack_replication_header(f[:9])[1])

        for frame in list(self.recovery_queue):
            epoch, seq, opcode = protocol.unpack_replication_header(frame[:9])
            if seq < self.expected_sequence_id:
                continue
            if seq == self.expected_sequence_id:
                if opcode == protocol.OP_APP_DATA:
                    if self.app_listener and self.app_listener.on_deliver(seq, frame[9:]):
                        self.expected_sequence_id = seq + 1
                        self._check_snapshot_threshold(seq)
        self.recovery_queue = []
        logger.info(f"Recovery complete. Expected sequence is now {self.expected_sequence_id}")

    def _check_catchup_completion(self) -> None:
        # once we've reached the target the leader gave us, go live. doing it this
        # way means recovery finishes even when there's no new traffic to ride on.
        if self.catchup_target_seq != -1 and (self.expected_sequence_id - 1) >= self.catchup_target_seq:
            self._flush_recovery_queue()

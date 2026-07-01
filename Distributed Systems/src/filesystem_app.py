# ===================== filesystem_app.py =====================
# the application layer: a tiny filesystem that plugs into the SMR engine.
# it implements AppListener, so the replication layer just calls on_deliver()
# with sequenced ops and this class turns them into actual files on disk.
#
# the tricky parts live here, not in replication:
#   - uploads are chunked and only become "real" on COMMIT (atomic rename
#     out of a .UUID.part temp file -> no half-written files ever visible)
#   - name collisions are resolved by the leader only (determinism)
#   - snapshots tar up the whole sandbox so a wiped node can be rebuilt
# ============================================================

import os
import json
import tarfile
import time
import shutil
import logging
from typing import Dict, Tuple, Optional
import uuid
import app_protocol as protocol
from replication import AppListener

logger = logging.getLogger("FileSystemApp")

class FileSystemApp(AppListener):
    def __init__(self, node_id: str):
        self.node_id = node_id
        formatted_node_id = node_id.replace("_", "-")
        # every node gets its own isolated storage dir under test-env/
        self.storage_dir = f"test-env/{formatted_node_id}-fs"
        os.makedirs(self.storage_dir, exist_ok=True)

        self.metadata_path = os.path.join(self.storage_dir, "metadata.json")
        self.files_metadata: Dict[str, dict] = {}
        self.last_applied_sequence_id = 0

        self._load_metadata_from_disk()

    def _load_metadata_from_disk(self) -> None:
        # pull back whatever state survived a previous run
        if os.path.exists(self.metadata_path):
            try:
                with open(self.metadata_path, "r") as f:
                    data = json.load(f)
                    self.last_applied_sequence_id = data.get("last_applied_sequence_id", 0)
                    self.files_metadata = data.get("files", {})
                logger.info(f"Loaded metadata from disk. Last sequence: {self.last_applied_sequence_id}")
            except Exception as e:
                logger.error(f"Failed to load metadata.json: {e}")

    def _save_metadata_to_disk(self) -> None:
        # write to a .tmp then rename, so a crash never leaves a half-written
        # metadata.json behind. fsync forces it down to the platter first.
        try:
            temp_path = self.metadata_path + ".tmp"
            with open(temp_path, "w") as f:
                json.dump({
                    "last_applied_sequence_id": self.last_applied_sequence_id,
                    "files": self.files_metadata
                }, f, indent=2)
                f.flush()
                os.fsync(f.fileno())
            os.replace(temp_path, self.metadata_path)
        except Exception as e:
            logger.error(f"Failed to write metadata.json: {e}")

    def has_file(self, filename: str) -> bool:
        return filename in self.files_metadata

    def resolve_collision(self, filename: str) -> str:
        # only the leader calls this. if the name is free, keep it; otherwise
        # bump a "(1)", "(2)", ... suffix until it's free. has to be
        # deterministic -- followers apply whatever string the leader picked.
        if filename not in self.files_metadata:
            return filename

        name, ext = os.path.splitext(filename)
        counter = 1
        while True:
            candidate = f"{name} ({counter}){ext}"
            if candidate not in self.files_metadata:
                return candidate
            counter += 1

    def on_deliver(self, sequence_id: int, payload: bytes) -> bool:
        # this is the state machine: a sequenced write op comes in, we apply it
        # to disk. same ops in the same order -> same state on every replica.
        if not payload:
            return False

        opcode = payload[0]
        self.last_applied_sequence_id = sequence_id

        try:
            if opcode == protocol.OP_START:
                session_uuid = protocol.unpack_app_start(payload[1:])
                part_file = os.path.join(self.storage_dir, f".{session_uuid}.part")
                # fresh (empty) .part file for this upload session
                with open(part_file, "wb") as f:
                    f.flush()
                    os.fsync(f.fileno())
                return True

            elif opcode == protocol.OP_CHUNK:
                session_uuid, chunk_data = protocol.unpack_app_chunk(payload[1:])
                part_file = os.path.join(self.storage_dir, f".{session_uuid}.part")
                with open(part_file, "ab") as f:
                    f.write(chunk_data)
                    f.flush()
                    os.fsync(f.fileno())
                return True

            elif opcode == protocol.OP_COMMIT:
                session_uuid, filename = protocol.unpack_app_commit(payload[1:])
                part_file = os.path.join(self.storage_dir, f".{session_uuid}.part")
                target_file = os.path.join(self.storage_dir, filename)

                if not os.path.exists(part_file):
                    logger.error(f"Part file for session {session_uuid} not found. Cannot commit.")
                    return False

                # filename was already resolved on the leader, so just rename
                os.replace(part_file, target_file)

                self.files_metadata[filename] = {
                    "size": os.path.getsize(target_file),
                    "uploaded_at": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                self._save_metadata_to_disk()
                logger.info(f"Committed file: {filename} (seq: {sequence_id})")
                return True

            elif opcode == protocol.OP_DELETE_FILE:
                filename = protocol.unpack_app_delete(payload[1:])
                target_file = os.path.join(self.storage_dir, filename)

                if filename in self.files_metadata:
                    del self.files_metadata[filename]

                if os.path.exists(target_file):
                    os.remove(target_file)

                self._save_metadata_to_disk()
                logger.info(f"Deleted file: {filename} (seq: {sequence_id})")
                return True

        except Exception as e:
            logger.error(f"Error applying operation {hex(opcode)}: {e}")

        return False

    def execute_snapshot(self, sequence_id: int) -> bool:
        # snapshot = tar up metadata + all live files so the log can be thrown
        # away. written to a .tmp and renamed so a partial snapshot is never seen.
        try:
            self._save_metadata_to_disk()

            snapshot_path = os.path.join(self.storage_dir, f"snapshot_{sequence_id}.tar.gz")
            temp_snapshot = snapshot_path + ".tmp"

            with tarfile.open(temp_snapshot, "w:gz") as tar:
                tar.add(self.metadata_path, arcname="metadata.json")
                # committed files
                for filename in self.files_metadata:
                    filepath = os.path.join(self.storage_dir, filename)
                    if os.path.exists(filepath):
                        tar.add(filepath, arcname=filename)
                # in-flight .part files too -- a commit might still be coming for
                # them after a recovering follower restores this snapshot
                for filename in os.listdir(self.storage_dir):
                    if filename.startswith(".") and filename.endswith(".part"):
                        filepath = os.path.join(self.storage_dir, filename)
                        tar.add(filepath, arcname=filename)

            os.replace(temp_snapshot, snapshot_path)
            logger.info(f"Snapshot created successfully: snapshot_{sequence_id}.tar.gz")
            return True
        except Exception as e:
            logger.error(f"Failed to execute snapshot: {e}")
            return False

    def get_latest_snapshot(self) -> Optional[Tuple[int, bytes]]:
        # newest snapshot wins -- pick the file with the highest seq in its name
        highest_seq = -1
        for filename in os.listdir(self.storage_dir):
            if filename.startswith("snapshot_") and filename.endswith(".tar.gz"):
                try:
                    seq = int(filename.split("_")[1].split(".")[0])
                    if seq > highest_seq:
                        highest_seq = seq
                except (ValueError, IndexError):
                    continue

        if highest_seq == -1:
            return None

        snapshot_path = os.path.join(self.storage_dir, f"snapshot_{highest_seq}.tar.gz")
        try:
            with open(snapshot_path, "rb") as f:
                return highest_seq, f.read()
        except Exception as e:
            logger.error(f"Failed to read snapshot file: {e}")
            return None

    def read_file(self, filename: str) -> Tuple[int, bytes]:
        # returns (status, content): 0 ok, 1 not found, 2 read error
        if filename not in self.files_metadata:
            return 1, b"File not found."

        target_file = os.path.join(self.storage_dir, filename)
        if not os.path.exists(target_file):
            return 1, b"File missing from storage."

        try:
            with open(target_file, "rb") as f:
                return 0, f.read()
        except Exception as e:
            return 2, f"Error reading file: {e}".encode('utf-8')

    def list_files(self) -> str:
        # the in-memory directory, as a json string for the wire
        return json.dumps(self.files_metadata)

    def load_snapshot(self, snapshot_path: str) -> bool:
        # rebuild the whole sandbox from a snapshot tarball
        try:
            # extract somewhere safe first; only swap things in once it's whole
            temp_extract_dir = os.path.join(self.storage_dir, "snapshot_extract_temp")
            if os.path.exists(temp_extract_dir):
                shutil.rmtree(temp_extract_dir)
            os.makedirs(temp_extract_dir, exist_ok=True)

            with tarfile.open(snapshot_path, "r:gz") as tar:
                tar.extractall(path=temp_extract_dir)

            temp_metadata_path = os.path.join(temp_extract_dir, "metadata.json")
            if not os.path.exists(temp_metadata_path):
                logger.error("Snapshot missing metadata.json!")
                shutil.rmtree(temp_extract_dir)
                return False

            with open(temp_metadata_path, "r") as f:
                data = json.load(f)

            # wipe whatever we currently have before restoring
            for filename in list(self.files_metadata.keys()):
                filepath = os.path.join(self.storage_dir, filename)
                if os.path.exists(filepath):
                    os.remove(filepath)
            self.files_metadata = {}

            # move the extracted files into the live storage dir
            for member_name in os.listdir(temp_extract_dir):
                src = os.path.join(temp_extract_dir, member_name)
                dst = os.path.join(self.storage_dir, member_name)
                if os.path.exists(dst):
                    os.remove(dst)
                os.replace(src, dst)

            shutil.rmtree(temp_extract_dir)

            # reload metadata from the restored file
            self._load_metadata_from_disk()
            logger.info("Successfully recovered state from snapshot.")
            return True
        except Exception as e:
            logger.error(f"Error loading snapshot: {e}")
            return False

    def preprocess_request(self, request: bytes) -> Tuple[bool, bytes, bytes]:
        # runs on the leader before anything is sequenced. it decides whether a
        # request is a write (needs to go through SMR) or a read (answer now),
        # and gets a chance to rewrite the payload before it's broadcast.
        # returns (is_write, immediate_response, proposed_payload).
        if not request:
            return False, b"", b""

        opcode = request[0]

        # writes -> these have to be sequenced and replicated
        if opcode in [protocol.OP_START, protocol.OP_CHUNK, protocol.OP_COMMIT, protocol.OP_DELETE_FILE]:
            # delete: bail early if the file isn't even here (don't waste a seq)
            if opcode == protocol.OP_DELETE_FILE:
                filename = protocol.unpack_app_delete(request[1:])
                if not self.has_file(filename):
                    import struct
                    return False, struct.pack("!B", 0x01), b""

            # commit: resolve the final name HERE, on the leader, then broadcast
            # the resolved name so every follower applies the exact same string
            elif opcode == protocol.OP_COMMIT:
                session_uuid, filename = protocol.unpack_app_commit(request[1:])
                resolved_filename = self.resolve_collision(filename)
                repacked_payload = bytes([protocol.OP_COMMIT]) + protocol.pack_app_commit(session_uuid, resolved_filename)
                import struct
                return True, struct.pack("!B", 0x00), repacked_payload

            # start / chunk go through untouched
            import struct
            return True, struct.pack("!B", 0x00), request

        # reads -> answered straight from the leader, no sequencing
        elif opcode == protocol.OP_READ_REQUEST:
            filename = protocol.unpack_app_read_request(request[1:])
            status, content = self.read_file(filename)
            response = protocol.pack_app_read_response(status, content)
            return False, response, b""

        elif opcode == protocol.OP_LIST_REQUEST:
            json_str = self.list_files()
            response = protocol.pack_app_list_response(json_str)
            return False, response, b""

        # anything else -> ignore
        return False, b"", b""

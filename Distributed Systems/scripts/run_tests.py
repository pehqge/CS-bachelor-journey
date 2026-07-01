import subprocess
import time
import os
import shutil
import signal
import sys
import socket
import struct
import hashlib

# paths relative to this file so the suite runs from anywhere
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
TEST_ENV = os.path.join(PROJECT_ROOT, "test-env")

# we hand the client every address and let it find the leader itself (it follows
# the WRONG_LEADER redirect and skips dead nodes), so no test ever has to know
# which node is the leader at any given moment.
ALL_NODES = "127.0.0.1:5050,127.0.0.1:5051,127.0.0.1:5052"

def run_client(commands_input: str, target: str = ALL_NODES, timeout: int = 15):
    # pipe a few CLI commands into client.py and hand back what it printed
    p = subprocess.Popen(
        [sys.executable, os.path.join(SRC_DIR, "client.py"), "--nodes", target],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=PROJECT_ROOT
    )
    stdout, stderr = p.communicate(input=commands_input.encode('utf-8'), timeout=timeout)
    return stdout.decode('utf-8'), stderr.decode('utf-8')

def kill_node(node_id):
    # SIGKILL a node using the pid we stashed when it started
    pid_file = os.path.join(TEST_ENV, "pids", f"{node_id}.pid")
    if os.path.exists(pid_file):
        with open(pid_file, "r") as f:
            pid = int(f.read().strip())
        try:
            os.kill(pid, signal.SIGKILL)
            print(f"[INFO] Terminated {node_id} (PID: {pid})")
        except OSError:
            pass
        try:
            os.remove(pid_file)
        except OSError:
            pass

def promote(host, port):
    # flip a live follower to leader in place -- same thing src/promote.py does,
    # just send the admin opcode and read the ack back. no restart, no kill.
    OP_PROMOTE = 0x0B
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3.0)
    try:
        s.connect((host, port))
        s.sendall(bytes([OP_PROMOTE]))
        try:
            s.recv(64)
        except socket.timeout:
            pass
        print(f"[INFO] Sent PROMOTE to {host}:{port}")
    finally:
        s.close()

def start_node(node_id, role, port, leader_port=None, snapshot_threshold=5, epoch=1):
    # spawn a server.py in the background and remember its pid
    cmd = [
        sys.executable,
        os.path.join(SRC_DIR, "server.py"),
        "--role", role,
        "--port", str(port),
        "--node-id", node_id,
        "--snapshot-threshold", str(snapshot_threshold),
        # full cluster list -> a follower can find the new leader on its own
        # after a leader change, without anyone restarting or repointing it
        "--peers", ALL_NODES
    ]
    if role == "leader":
        cmd.extend(["--epoch", str(epoch)])
    if leader_port:
        cmd.extend(["--leader-host", "127.0.0.1", "--leader-port", str(leader_port)])

    os.makedirs(os.path.join(TEST_ENV, "logs"), exist_ok=True)
    log_file = open(os.path.join(TEST_ENV, "logs", f"{node_id}.log"), "w")
    proc = subprocess.Popen(cmd, stdout=log_file, stderr=log_file, cwd=PROJECT_ROOT)

    os.makedirs(os.path.join(TEST_ENV, "pids"), exist_ok=True)
    with open(os.path.join(TEST_ENV, "pids", f"{node_id}.pid"), "w") as f:
        f.write(str(proc.pid))

    print(f"[INFO] Started {node_id} ({role}) on port {port} (PID: {proc.pid})")
    return proc

def cleanup():
    # kill everything and wipe test-env so every run starts from a clean slate
    print("[INFO] Cleaning up replica processes...")
    for node in ["node_1", "node_2", "node_3"]:
        kill_node(node)
    # belt and suspenders: sweep up any server we lost track of
    subprocess.run(["pkill", "-9", "-f", "src/server.py"], stderr=subprocess.DEVNULL)
    if os.path.exists(TEST_ENV):
        try:
            shutil.rmtree(TEST_ENV)
        except Exception:
            pass
    print("[INFO] Cleanup complete.")

# ---------------------------------------------------------------------------
# Replica state verification ("estado das réplicas ao final")
# ---------------------------------------------------------------------------

def replica_signature(node_dir):
    # hash every committed file in a node's sandbox -> {name: sha}. we skip the
    # .part / metadata.json / snapshot_* noise so the diff only compares the
    # files a user would actually see.
    if not os.path.isdir(node_dir):
        return None
    sig = {}
    for fname in sorted(os.listdir(node_dir)):
        if fname.startswith(".") or fname == "metadata.json" or fname.startswith("snapshot_"):
            continue
        fpath = os.path.join(node_dir, fname)
        if os.path.isfile(fpath):
            with open(fpath, "rb") as f:
                sig[fname] = hashlib.sha256(f.read()).hexdigest()[:12]
    return sig

def verify_replicas(node_names, label="REPLICA STATE DIFF"):
    # print each replica's signature and check they all line up
    print(f"\n--- {label} ---")
    sigs = []
    for n in node_names:
        sig = replica_signature(os.path.join(TEST_ENV, n))
        sigs.append(sig)
        if sig is None:
            print(f"  {n:<12}: (missing dir)")
        elif not sig:
            print(f"  {n:<12}: (empty)")
        else:
            print(f"  {n:<12}: {sig}")
    identical = all(s is not None for s in sigs) and all(s == sigs[0] for s in sigs)
    print(f"  => {'IDENTICAL across replicas' if identical else 'DIVERGENT'}")
    return identical

def main():
    cleanup()
    os.makedirs(os.path.join(TEST_ENV, "logs"), exist_ok=True)
    os.makedirs(os.path.join(TEST_ENV, "pids"), exist_ok=True)

    print("\n=== STARTING AUTOMATED DISTRIBUTED FS REPLICATION TESTS ===")

    # tiny snapshot threshold (5) so compaction fires after just a couple uploads
    start_node("node_1", "leader", 5050, snapshot_threshold=5)
    start_node("node_2", "follower", 5051, leader_port=5050, snapshot_threshold=5)
    start_node("node_3", "follower", 5052, leader_port=5050, snapshot_threshold=5)

    # let the cluster come up and sync before we poke it
    time.sleep(3.0)

    success = True

    # the file we'll upload around in the tests
    test_file_path = os.path.join(PROJECT_ROOT, "test_file.txt")
    with open(test_file_path, "w") as f:
        f.write("Hello Distributed World!")

    try:
        # TEST 1: Synchronous Replication
        print("\n--- TEST 1: Synchronous Replication ---")
        run_client("upload test_file.txt file1.txt\nexit\n")
        time.sleep(1.0)

        # it should land on all three nodes
        for node in ["node-1-fs", "node-2-fs", "node-3-fs"]:
            path = os.path.join(TEST_ENV, node, "file1.txt")
            if not os.path.exists(path):
                print(f"[FAIL] file1.txt not replicated to {node}")
                success = False
            else:
                print(f"[PASS] file1.txt successfully replicated to {node}")

        print("\n--- TEST 2: Fault Tolerance (Node Drop) ---")
        kill_node("node_3")
        time.sleep(1.0)

        # upload with node_3 dead -- should still go through on the two survivors
        run_client("upload test_file.txt file2.txt\nexit\n")
        time.sleep(1.0)

        # node 1 and 2 should have it, node 3 should not
        for node in ["node-1-fs", "node-2-fs"]:
            path = os.path.join(TEST_ENV, node, "file2.txt")
            if not os.path.exists(path):
                print(f"[FAIL] file2.txt not replicated to active {node}")
                success = False
            else:
                print(f"[PASS] file2.txt successfully replicated to active {node}")

        node_3_path = os.path.join(TEST_ENV, "node-3-fs", "file2.txt")
        if os.path.exists(node_3_path):
            print("[FAIL] file2.txt unexpectedly replicated to dead node-3")
            success = False
        else:
            print("[PASS] file2.txt was not written to dead node-3")

        print("\n--- TEST 3: Catch-up Recovery ---")
        # bring node_3 back -- it should pull the file2 it missed while down
        start_node("node_3", "follower", 5052, leader_port=5050, snapshot_threshold=5)
        time.sleep(3.0)  # handshake + catch-up

        if not os.path.exists(node_3_path):
            print("[FAIL] node-3 failed to catch up and replicate file2.txt")
            success = False
        else:
            print("[PASS] node-3 caught up successfully and received file2.txt")

        print("\n--- TEST 4: Snapshot Recovery ---")
        # each upload is 3 SMR ops (START, CHUNK, COMMIT), so two uploads put us
        # at seq 6 -- past the threshold of 5, meaning a snapshot already ran at
        # seq 5. now nuke node-2 entirely and make it rebuild from that snapshot.
        print("[INFO] Wiping node-2 state directory...")
        node_2_dir = os.path.join(TEST_ENV, "node-2-fs")
        if os.path.exists(node_2_dir):
            shutil.rmtree(node_2_dir)
        os.makedirs(node_2_dir, exist_ok=True)

        # sanity check that the wipe actually happened
        for i in [1, 2]:
            if os.path.exists(os.path.join(node_2_dir, f"file{i}.txt")):
                print("[FAIL] Wiping node-2 state failed internally in test script")
                success = False

        # restart it from nothing -> forces a catch-up that falls back to snapshot
        kill_node("node_2")
        time.sleep(1.0)
        start_node("node_2", "follower", 5051, leader_port=5050, snapshot_threshold=5)
        time.sleep(4.0)  # ask for catch-up, pull the snapshot, restore

        # both files should be back
        recovered_all = True
        for i in [1, 2]:
            path = os.path.join(node_2_dir, f"file{i}.txt")
            if not os.path.exists(path):
                print(f"[FAIL] node-2 failed to recover file{i}.txt via snapshot")
                recovered_all = False
                success = False
        if recovered_all:
            print("[PASS] node-2 successfully loaded leader snapshot and recovered all files")

        print("\n--- TEST 5: Download / Read Path ---")
        download_path = os.path.join(PROJECT_ROOT, "downloaded_file1.txt")
        if os.path.exists(download_path):
            os.remove(download_path)
        run_client(f"download file1.txt {download_path}\nexit\n")
        time.sleep(0.5)
        if os.path.exists(download_path):
            with open(download_path, "rb") as f:
                got = f.read()
            if got == b"Hello Distributed World!":
                print("[PASS] downloaded content matches the original upload")
            else:
                print(f"[FAIL] downloaded content mismatch: {got!r}")
                success = False
            os.remove(download_path)
        else:
            print("[FAIL] download did not produce a local file")
            success = False

        print("\n--- TEST 6: Delete Replication ---")
        run_client("delete file2.txt\nexit\n")
        time.sleep(1.0)
        deleted_everywhere = True
        for node in ["node-1-fs", "node-2-fs", "node-3-fs"]:
            if os.path.exists(os.path.join(TEST_ENV, node, "file2.txt")):
                print(f"[FAIL] file2.txt still present on {node} after delete")
                deleted_everywhere = False
                success = False
        # file1.txt must still be present (delete is targeted, not a wipe)
        for node in ["node-1-fs", "node-2-fs", "node-3-fs"]:
            if not os.path.exists(os.path.join(TEST_ENV, node, "file1.txt")):
                print(f"[FAIL] file1.txt unexpectedly missing on {node} after delete")
                success = False
        if deleted_everywhere:
            print("[PASS] file2.txt removed from all 3 replicas; file1.txt preserved")

        print("\n--- TEST 7: Concurrent Collision Resolution ---")
        a_path = os.path.join(PROJECT_ROOT, "concurrent_a.bin")
        b_path = os.path.join(PROJECT_ROOT, "concurrent_b.bin")
        content_a = b"A" * 400
        content_b = b"B" * 600
        with open(a_path, "wb") as f:
            f.write(content_a)
        with open(b_path, "wb") as f:
            f.write(content_b)

        # Fire two clients uploading distinct content to the SAME remote name in parallel
        pA = subprocess.Popen(
            [sys.executable, os.path.join(SRC_DIR, "client.py"), "--nodes", "127.0.0.1:5050"],
            stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=PROJECT_ROOT)
        pB = subprocess.Popen(
            [sys.executable, os.path.join(SRC_DIR, "client.py"), "--nodes", "127.0.0.1:5050"],
            stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=PROJECT_ROOT)
        pA.communicate(b"upload concurrent_a.bin race.bin\nexit\n", timeout=15)
        pB.communicate(b"upload concurrent_b.bin race.bin\nexit\n", timeout=15)
        time.sleep(1.0)

        leader_dir = os.path.join(TEST_ENV, "node-1-fs")
        clash = sorted(f for f in os.listdir(leader_dir) if f.startswith("race") and f.endswith(".bin"))
        if clash == ["race (1).bin", "race.bin"]:
            print("[PASS] collision resolved deterministically: race.bin + 'race (1).bin'")
        else:
            print(f"[FAIL] unexpected collision result: {clash}")
            success = False
        # Both distinct contents must survive (no lost update)
        survived = set()
        for f in clash:
            with open(os.path.join(leader_dir, f), "rb") as fh:
                survived.add(fh.read())
        if survived == {content_a, content_b}:
            print("[PASS] both contents survived — no lost update")
        else:
            print(f"[FAIL] lost update: surviving sizes {[len(s) for s in survived]}")
            success = False
        # Replicated identically to all three
        if verify_replicas(["node-1-fs", "node-2-fs", "node-3-fs"], "REPLICA DIFF after concurrent upload"):
            print("[PASS] concurrent upload replicated identically to all 3 nodes")
        else:
            print("[FAIL] concurrent upload diverged across replicas")
            success = False
        os.remove(a_path)
        os.remove(b_path)

        print("\n--- TEST 8: Full Replica State Verification ---")
        if verify_replicas(["node-1-fs", "node-2-fs", "node-3-fs"], "FINAL REPLICA STATE (3 live nodes)"):
            print("[PASS] all three replicas hold identical committed state")
        else:
            print("[FAIL] replicas diverged")
            success = False

        # TEST 9: WRONG_LEADER Redirection (client contacts a follower)
        # A follower must reject a client and reply with OpCode 0x06 (WRONG_LEADER)
        # carrying the active leader's host:port, so the client can reconnect.
        print("\n--- TEST 9: WRONG_LEADER Redirection ---")
        WRONG_LEADER = 0x06
        I_AM_CLIENT = 0x08
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5.0)
            s.connect(("127.0.0.1", 5051))      # node_2 is a follower
            s.sendall(bytes([I_AM_CLIENT]))      # identity handshake (single raw byte)
            # read one length-prefixed frame (4-byte big-endian length + payload)
            raw_len = s.recv(4)
            (flen,) = struct.unpack("!I", raw_len)
            frame = b""
            while len(frame) < flen:
                frame += s.recv(flen - len(frame))
            s.close()
            epoch, seq, opcode = struct.unpack("!IIB", frame[:9])
            if opcode != WRONG_LEADER:
                print(f"[FAIL] follower did not signal WRONG_LEADER (got opcode {hex(opcode)})")
                success = False
            else:
                (addr_len,) = struct.unpack("!H", frame[9:11])
                addr = frame[11:11 + addr_len].decode("utf-8")
                if addr == "127.0.0.1:5050":
                    print(f"[PASS] follower replied WRONG_LEADER with the correct leader address ({addr})")
                else:
                    print(f"[FAIL] WRONG_LEADER carried wrong leader address: {addr}")
                    success = False
        except Exception as e:
            print(f"[FAIL] WRONG_LEADER protocol test errored: {e}")
            success = False

        # end-to-end: pointing the CLI at a follower must still reach the leader
        _, redirect_err = run_client("list\nexit\n", target="127.0.0.1:5051")
        if "Redirected to Leader at 127.0.0.1:5050" in redirect_err:
            print("[PASS] CLI transparently redirected from follower to leader")
        else:
            print("[FAIL] CLI did not redirect from follower to leader")
            success = False

        # TEST 10: Leader Failure + In-Place Promotion (runtime flip)
        # The leader is killed. ONE surviving follower (node_2) is promoted in
        # place via the OP_PROMOTE admin command -- no restart, epoch bumped to
        # fence the ghost leader. node_3 is NOT killed or repointed: it
        # rediscovers the new leader on its own through its static peer list.
        print("\n--- TEST 10: Leader Failure + In-Place Promotion (runtime flip) ---")
        kill_node("node_1")  # primary dies
        time.sleep(3.0)      # followers detect death and enter leader discovery

        promote("127.0.0.1", 5051)  # flip node_2 -> leader in place (epoch+1)
        # node_3 stays alive; give it time to rediscover node_2 and catch up.
        time.sleep(5.0)

        # Writes must resume after promotion. The client gets the full node list
        # and discovers the new leader transparently (skips dead 5050 -> finds 5051).
        run_client("upload test_file.txt after_promo.txt\nexit\n")
        time.sleep(1.0)
        promoted_ok = True
        for node in ["node-2-fs", "node-3-fs"]:
            if not os.path.exists(os.path.join(TEST_ENV, node, "after_promo.txt")):
                print(f"[FAIL] write after promotion not replicated to {node}")
                promoted_ok = False
                success = False
        if promoted_ok:
            # node_3 receiving the write proves it self-rediscovered the new
            # leader without being killed or restarted.
            print("[PASS] in-place promotion: new leader accepts writes, follower self-rediscovered (no restart)")
        if not verify_replicas(["node-2-fs", "node-3-fs"], "POST-PROMOTION DIFF (surviving nodes)"):
            print("[FAIL] surviving replicas diverged after promotion")
            success = False
        else:
            print("[PASS] surviving replicas consistent after promotion")

    except Exception as e:
        print(f"[ERROR] Test execution failed with exception: {e}")
        success = False
    finally:
        # drop the local scratch file and tear the cluster down
        if os.path.exists(test_file_path):
            os.remove(test_file_path)
        cleanup()

    print("\n================ TEST SUMMARY ================")
    if success:
        print("ALL REPLICATION AND RECOVERY TESTS PASSED!")
        sys.exit(0)
    else:
        print("SOME REPLICATION TESTS FAILED. CHECK LOGS IN test-env/logs/")
        sys.exit(1)

if __name__ == "__main__":
    main()

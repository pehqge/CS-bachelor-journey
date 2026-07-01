# Distributed filesystem (SMR)

> INE5418 — Computação Distribuída · UFSC · 2026/1 · Trabalho 2
> Grupo 17 — Gustavo Rodrigues Alves D'Angelo, Pedro Henrique Gimenez, Tom Pereira Hunt

A strongly consistent distributed filesystem built on State Machine Replication
(SMR), in plain Python. Upload / download / list / delete, replicated across a
3-node cluster.

## Layout

```text
distributed-fs/
├── src/                  # source
│   ├── app_protocol.py   # application wire protocol
│   ├── filesystem_app.py # the filesystem state machine
│   ├── server.py         # replica node entry point
│   ├── client.py         # TCP CLI client
│   └── replication/      # the reusable SMR building block
│       ├── __init__.py   # exposes ReplicationNode, AppListener
│       ├── replication.py# SMR engine: consensus loop + recovery
│       ├── communicator.py# length-prefixed TCP framing
│       └── protocol.py   # SMR wire protocol
├── docs/                 # architecture + protocol notes
│   ├── docs.md           # how it's built and why
│   └── protocol.md       # the binary wire protocol
├── scripts/              # cluster automation
│   ├── start_nodes.sh    # bring up a local 3-node cluster
│   └── cleanup.sh        # stop nodes and wipe test-env
└── test-env/             # runtime state (generated)
    ├── node-1-fs/        # node 1's isolated filesystem
    ├── node-2-fs/        # node 2's isolated filesystem
    ├── node-3-fs/        # node 3's isolated filesystem
    ├── logs/             # per-node logs
    └── pids/             # running process PIDs
```

## Running it

Start a 3-node cluster from the project root:

```bash
./scripts/start_nodes.sh
```

Then run the client. You pass it the whole node list and it finds the leader on
its own (it gets redirected if it hits a follower, and skips dead nodes), so you
never have to know which node is the leader:

```bash
python3 src/client.py --nodes 127.0.0.1:5050,127.0.0.1:5051,127.0.0.1:5052
```

Commands: `upload <local> <remote>`, `download <remote> <local>`, `list`,
`delete <remote>`, `exit`.

Stop everything and clean up:

```bash
./scripts/cleanup.sh
```

## Demos

The [demo/](demo/) directory holds five recorded-demo scripts, one per scenario.
Each one brings up its own cluster, walks through a single situation, prints the
state of all three replicas at the end, and tears the cluster back down, so you
can run them on their own and in any order. They pause on `[ENTER]` between
steps; set `NOPAUSE=1` to run straight through.

```bash
./demo/01_normal.sh          # upload / list / download / delete, replicated to all 3 nodes
./demo/02_concorrencia.sh    # two clients upload the same name; leader hands out a deterministic (1) suffix
./demo/03_falha_follower.sh  # kill a follower (writes still go through), then it catches up on return
./demo/04_falha_lider.sh     # kill the leader, promote a follower at runtime, writes resume
./demo/05_snapshot.sh        # wipe a node and rebuild it from a snapshot
```

A recorded walkthrough of the demos is on YouTube: https://youtu.be/oFuAaPZYFC0

## Tests

```bash
./scripts/run_tests.sh
```

The suite brings up a leader + two followers and checks the full cycle:

1. Synchronous replication: an upload lands identically on all three nodes.
2. Fault tolerance: kill a follower, writes still go through (Drop Rule).
3. Catch-up: a restarted follower reconnects and pulls the entries it missed.
4. Snapshot recovery: a wiped node requests and loads a snapshot, restoring state.
5. Download: a downloaded file matches the original byte for byte.
6. Delete replication: a delete propagates to all three replicas.
7. Concurrent collisions: two clients uploading the same name both survive (no
   lost update) and the leader hands out a deterministic `(1)` suffix everywhere.
8. Replica diff: the committed contents of all three nodes are hashed and
   compared to confirm they're identical.
9. WRONG_LEADER redirect: a client that contacts a follower gets opcode `0x06`
   with the leader's `host:port` and reconnects transparently.
10. Leader failure: kill the leader, flip one surviving follower to leader at
    runtime (no restart) with the `OP_PROMOTE` command and a higher epoch; the
    other follower finds the new leader on its own via its peer list, and writes
    resume.

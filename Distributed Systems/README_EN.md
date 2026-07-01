[<kbd><img title="Português" alt="Português" src="https://flagicons.lipis.dev/flags/4x3/br.svg" width="22"></kbd> Versão em português](README.md)

# INE5418 - Distributed Systems

Group 17: Gustavo Rodrigues Alves D'Angelo, Pedro Henrique Gimenez and Tom Pereira Hunt.

These are the two course projects, each in its own folder. Trabalho 1 is a distributed URL shortener with caching and a circuit breaker. Trabalho 2 is a distributed filesystem built on State Machine Replication (SMR).

| Folder | What it holds |
|---|---|
| [Trabalho 1/](Trabalho%201) | Distributed URL shortener (client, interceptor and REST server). |
| [Trabalho 2/](Trabalho%202) | Distributed filesystem on SMR, replicated across 3 nodes. |

Original repository: [gustavovonn/distributed-fs](https://github.com/gustavovonn/distributed-fs)

## Trabalho 1 - Distributed URL shortener

Three parts talking over two protocols: clients speak TCP (one JSON message per line) to an interceptor, and the interceptor speaks HTTP REST to the server. The interceptor is transparent (the server does not know it exists) and adds two patterns: Cache-Aside (LRU + TTL) and Circuit Breaker.

Full documentation and run instructions live in the [Trabalho 1 README](Trabalho%201/README.md).

| Path | Description |
|---|---|
| [README.md](Trabalho%201/README.md) | Full project documentation. |
| [relatorio.pdf](Trabalho%201/relatorio.pdf) | Project report. |
| [config.txt](Trabalho%201/config.txt) | Shared config (host, ports, cache, circuit breaker). |
| [server/server.py](Trabalho%201/server/server.py) | REST server (standard-library `http.server`). |
| [interceptor/interceptor.py](Trabalho%201/interceptor/interceptor.py) | TCP server: request routing and dispatch. |
| [interceptor/cache.py](Trabalho%201/interceptor/cache.py) | Thread-safe LRU cache with TTL. |
| [interceptor/circuit_breaker.py](Trabalho%201/interceptor/circuit_breaker.py) | Circuit breaker (CLOSED / OPEN / HALF_OPEN). |
| [interceptor/protocol.py](Trabalho%201/interceptor/protocol.py) | JSON-per-line protocol. |
| [clients/python/url_client.py](Trabalho%201/clients/python/url_client.py) | Python client library. |
| [clients/javascript/url_client.js](Trabalho%201/clients/javascript/url_client.js) | Node.js client library. |
| [examples/](Trabalho%201/examples) | Demos: basic usage, cache and circuit breaker. |

## Trabalho 2 - Distributed filesystem (SMR)

A strongly consistent filesystem in plain Python, built on State Machine Replication. Upload, download, list and delete files, replicated across a 3-node cluster, staying consistent through faults. The client gets the full node list and finds the leader on its own, so you never need to know which node is the leader.

### Code

| Path | Description |
|---|---|
| [src/server.py](Trabalho%202/src/server.py) | Replica node entry point. |
| [src/client.py](Trabalho%202/src/client.py) | TCP command-line client. |
| [src/filesystem_app.py](Trabalho%202/src/filesystem_app.py) | The filesystem state machine. |
| [src/app_protocol.py](Trabalho%202/src/app_protocol.py) | Application protocol. |
| [src/promote.py](Trabalho%202/src/promote.py) | Promotes a follower to leader at runtime. |
| [src/replication/replication.py](Trabalho%202/src/replication/replication.py) | SMR engine: consensus loop and recovery. |
| [src/replication/communicator.py](Trabalho%202/src/replication/communicator.py) | Length-prefixed TCP framing. |
| [src/replication/protocol.py](Trabalho%202/src/replication/protocol.py) | SMR wire protocol. |

### Docs, scripts and demos

| Path | Description |
|---|---|
| [docs/protocol.md](Trabalho%202/docs/protocol.md) | The binary wire protocol in three layers (framing, replication, application). |
| [docs/T2 - Building Blocks.pdf](Trabalho%202/docs/T2%20-%20Building%20Blocks.pdf) | Assignment brief. |
| [scripts/start_nodes.sh](Trabalho%202/scripts/start_nodes.sh) | Brings up a local 3-node cluster. |
| [scripts/run_tests.sh](Trabalho%202/scripts/run_tests.sh) | Runs the test suite. |
| [scripts/run_tests.py](Trabalho%202/scripts/run_tests.py) | Test suite (10 scenarios). |
| [scripts/cleanup.sh](Trabalho%202/scripts/cleanup.sh) | Stops the nodes and wipes the test environment. |
| [slides/apresentacao.pdf](Trabalho%202/slides/apresentacao.pdf) | Presentation slides. |
| [video_apresentacao.md](Trabalho%202/video_apresentacao.md) | Link to the demo video. |

### Demos

Each script brings up its own cluster, walks through one scenario and tears it all down, so you can run them in any order. They pause on `[ENTER]` between steps; set `NOPAUSE=1` to run straight through.

| Script | Scenario |
|---|---|
| [01_normal.sh](Trabalho%202/demo/01_normal.sh) | upload, list, download and delete replicated to all 3 nodes. |
| [02_concorrencia.sh](Trabalho%202/demo/02_concorrencia.sh) | two clients upload the same name; the leader hands out a deterministic `(1)` suffix. |
| [03_falha_follower.sh](Trabalho%202/demo/03_falha_follower.sh) | kill a follower; writes still go through; it catches up on return. |
| [04_falha_lider.sh](Trabalho%202/demo/04_falha_lider.sh) | kill the leader, promote a follower at runtime, writes resume. |
| [05_snapshot.sh](Trabalho%202/demo/05_snapshot.sh) | wipe a node and rebuild it from a snapshot. |

### Running it

From `Trabalho 2/`, bring up the cluster and run the client:

```bash
./scripts/start_nodes.sh
python3 src/client.py --nodes 127.0.0.1:5050,127.0.0.1:5051,127.0.0.1:5052
```

Client commands: `upload <local> <remote>`, `download <remote> <local>`, `list`, `delete <remote>`, `exit`. To stop everything and clean up: `./scripts/cleanup.sh`.

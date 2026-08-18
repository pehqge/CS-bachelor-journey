[<kbd><img title="Português" alt="Português" src="https://flagicons.lipis.dev/flags/4x3/br.svg" width="22"></kbd> Versão em português](README.md)

# INE5418 - Distributed Systems

**Group 17:** Gustavo Rodrigues Alves D'Angelo, Pedro Henrique Gimenez and Tom Pereira Hunt

The course's two projects, each in its own folder. [Trabalho 1](Trabalho%201) is a distributed URL shortener with caching and a circuit breaker. [Trabalho 2](Trabalho%202) is a distributed filesystem built on State Machine Replication (SMR), replicated across 3 nodes. The original repository for Trabalho 2 is [gustavovonn/distributed-fs](https://github.com/gustavovonn/distributed-fs).

Study site for the course exam, open to anyone: **[distribuida.pehqge.com](https://distribuida.pehqge.com)**. It covers the syllabus in 7 modules, with interactive labs, open-ended questions graded by an LLM and mock exams assembled from past papers. In Portuguese.

## Trabalho 1 - Distributed URL shortener

Three components and two protocols: clients speak TCP (one JSON message per line) to an interceptor, and the interceptor speaks HTTP REST to the server. The interceptor is transparent, the server does not know it exists, and it adds Cache-Aside (LRU + TTL) and Circuit Breaker. Full documentation is in the [Trabalho 1 README](Trabalho%201/README.md).

| Path | Description |
|---|---|
| [relatorio.pdf](Trabalho%201/relatorio.pdf) | Project report. In Portuguese. |
| [server/server.py](Trabalho%201/server/server.py) | REST server, on top of the standard-library `http.server`. |
| [interceptor/interceptor.py](Trabalho%201/interceptor/interceptor.py) | TCP server: request routing and dispatch. |
| [interceptor/cache.py](Trabalho%201/interceptor/cache.py) | Thread-safe LRU cache with TTL. |
| [interceptor/circuit_breaker.py](Trabalho%201/interceptor/circuit_breaker.py) | Circuit breaker (CLOSED / OPEN / HALF_OPEN). |
| [interceptor/protocol.py](Trabalho%201/interceptor/protocol.py) | JSON-per-line protocol. |
| [clients/](Trabalho%201/clients) | Client libraries in Python and Node.js. |
| [examples/](Trabalho%201/examples) | Demos for basic usage, caching and the circuit breaker. |
| [config.txt](Trabalho%201/config.txt) | Shared config: host, ports, cache and circuit breaker. |

## Trabalho 2 - Distributed filesystem (SMR)

A strongly consistent filesystem in plain Python. Upload, download, list and delete, replicated across a 3-node cluster and consistent through faults. The client gets the node list and finds the leader on its own.

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

| Docs and scripts | Description |
|---|---|
| [docs/protocol.md](Trabalho%202/docs/protocol.md) | The binary wire protocol in three layers: framing, replication and application. |
| [docs/T2 - Building Blocks.pdf](Trabalho%202/docs/T2%20-%20Building%20Blocks.pdf) | Assignment brief. |
| [slides/apresentacao.pdf](Trabalho%202/slides/apresentacao.pdf) | Presentation slides. In Portuguese. |
| [scripts/start_nodes.sh](Trabalho%202/scripts/start_nodes.sh) | Brings up a local 3-node cluster. |
| [scripts/run_tests.sh](Trabalho%202/scripts/run_tests.sh) | Runs the test suite, 10 scenarios. |
| [scripts/cleanup.sh](Trabalho%202/scripts/cleanup.sh) | Stops the nodes and wipes the test environment. |

### Demos

Each script brings up its own cluster, walks through one scenario and tears it all down, so they run in any order. They pause on `[ENTER]` between steps; `NOPAUSE=1` runs straight through.

| Script | Scenario |
|---|---|
| [01_normal.sh](Trabalho%202/demo/01_normal.sh) | Upload, list, download and delete replicated to all 3 nodes. |
| [02_concorrencia.sh](Trabalho%202/demo/02_concorrencia.sh) | Two clients upload the same name; the leader hands out a deterministic `(1)` suffix. |
| [03_falha_follower.sh](Trabalho%202/demo/03_falha_follower.sh) | Kill a follower; writes keep going and it catches up on return. |
| [04_falha_lider.sh](Trabalho%202/demo/04_falha_lider.sh) | Kill the leader, promote a follower at runtime, writes resume. |
| [05_snapshot.sh](Trabalho%202/demo/05_snapshot.sh) | Wipe a node and rebuild it from a snapshot. |

### Running it

From `Trabalho 2/`:

```bash
./scripts/start_nodes.sh
python3 src/client.py --nodes 127.0.0.1:5050,127.0.0.1:5051,127.0.0.1:5052
```

Client commands: `upload <local> <remote>`, `download <remote> <local>`, `list`, `delete <remote>` and `exit`. To stop everything: `./scripts/cleanup.sh`.

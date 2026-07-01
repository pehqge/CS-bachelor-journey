[<kbd><img title="English" alt="English" src="https://flagicons.lipis.dev/flags/4x3/us.svg" width="22"></kbd> English version](README_EN.md)

# INE5418 - Computação Distribuída

Grupo 17: Gustavo Rodrigues Alves D'Angelo, Pedro Henrique Gimenez e Tom Pereira Hunt.

São os dois trabalhos da disciplina, cada um na sua pasta. O Trabalho 1 é um encurtador de URLs distribuído com cache e circuit breaker. O Trabalho 2 é um sistema de arquivos distribuído sobre Replicação de Máquina de Estados (SMR).

| Pasta | O que tem |
|---|---|
| [Trabalho 1/](Trabalho%201) | Encurtador de URLs distribuído (cliente, interceptador e servidor REST). |
| [Trabalho 2/](Trabalho%202) | Sistema de arquivos distribuído sobre SMR, replicado em 3 nós. |

Repositório original: [gustavovonn/distributed-fs](https://github.com/gustavovonn/distributed-fs)

## Trabalho 1 - Encurtador de URLs distribuído

Três componentes que conversam por dois protocolos: os clientes falam TCP (JSON por linha) com um interceptador, e o interceptador fala HTTP REST com o servidor. O interceptador é transparente (o servidor não sabe que ele existe) e adiciona dois padrões: Cache-Aside (LRU + TTL) e Circuit Breaker.

A documentação completa e as instruções de execução estão no [README do Trabalho 1](Trabalho%201/README.md).

| Caminho | Descrição |
|---|---|
| [README.md](Trabalho%201/README.md) | Documentação completa do trabalho. |
| [relatorio.pdf](Trabalho%201/relatorio.pdf) | Relatório do trabalho. |
| [config.txt](Trabalho%201/config.txt) | Configuração compartilhada (host, portas, cache, circuit breaker). |
| [server/server.py](Trabalho%201/server/server.py) | Servidor REST (biblioteca padrão `http.server`). |
| [interceptor/interceptor.py](Trabalho%201/interceptor/interceptor.py) | Servidor TCP: roteamento e dispatch das requisições. |
| [interceptor/cache.py](Trabalho%201/interceptor/cache.py) | Cache LRU com TTL, thread-safe. |
| [interceptor/circuit_breaker.py](Trabalho%201/interceptor/circuit_breaker.py) | Circuit breaker (CLOSED / OPEN / HALF_OPEN). |
| [interceptor/protocol.py](Trabalho%201/interceptor/protocol.py) | Protocolo JSON por linha. |
| [clients/python/url_client.py](Trabalho%201/clients/python/url_client.py) | Biblioteca cliente em Python. |
| [clients/javascript/url_client.js](Trabalho%201/clients/javascript/url_client.js) | Biblioteca cliente em Node.js. |
| [examples/](Trabalho%201/examples) | Demos: uso básico, cache e circuit breaker. |

## Trabalho 2 - Sistema de arquivos distribuído (SMR)

Um sistema de arquivos fortemente consistente, em Python puro, sobre Replicação de Máquina de Estados. Faz upload, download, listagem e remoção de arquivos, replicados num cluster de 3 nós, mantendo consistência mesmo com falhas. O cliente recebe a lista completa de nós e descobre o líder sozinho, então nunca é preciso saber qual nó é o líder.

### Código

| Caminho | Descrição |
|---|---|
| [src/server.py](Trabalho%202/src/server.py) | Ponto de entrada de um nó réplica. |
| [src/client.py](Trabalho%202/src/client.py) | Cliente TCP de linha de comando. |
| [src/filesystem_app.py](Trabalho%202/src/filesystem_app.py) | A máquina de estados do sistema de arquivos. |
| [src/app_protocol.py](Trabalho%202/src/app_protocol.py) | Protocolo de aplicação. |
| [src/promote.py](Trabalho%202/src/promote.py) | Promove um follower a líder em tempo de execução. |
| [src/replication/replication.py](Trabalho%202/src/replication/replication.py) | Motor de SMR: laço de consenso e recuperação. |
| [src/replication/communicator.py](Trabalho%202/src/replication/communicator.py) | Framing TCP com prefixo de tamanho. |
| [src/replication/protocol.py](Trabalho%202/src/replication/protocol.py) | Protocolo de rede do SMR. |

### Documentação, scripts e demos

| Caminho | Descrição |
|---|---|
| [docs/protocol.md](Trabalho%202/docs/protocol.md) | O protocolo binário em três camadas (framing, replicação, aplicação). |
| [docs/T2 - Building Blocks.pdf](Trabalho%202/docs/T2%20-%20Building%20Blocks.pdf) | Enunciado do trabalho. |
| [scripts/start_nodes.sh](Trabalho%202/scripts/start_nodes.sh) | Sobe um cluster local de 3 nós. |
| [scripts/run_tests.sh](Trabalho%202/scripts/run_tests.sh) | Roda a suíte de testes. |
| [scripts/run_tests.py](Trabalho%202/scripts/run_tests.py) | Suíte de testes (10 cenários). |
| [scripts/cleanup.sh](Trabalho%202/scripts/cleanup.sh) | Para os nós e limpa o ambiente de teste. |
| [slides/apresentacao.pdf](Trabalho%202/slides/apresentacao.pdf) | Slides da apresentação. |
| [video_apresentacao.md](Trabalho%202/video_apresentacao.md) | Link do vídeo com as demos. |

### Demos

Cada script sobe o próprio cluster, mostra um cenário e derruba tudo no final, então dá para rodar em qualquer ordem. Eles pausam em `[ENTER]` entre passos; use `NOPAUSE=1` para rodar direto.

| Script | Cenário |
|---|---|
| [01_normal.sh](Trabalho%202/demo/01_normal.sh) | upload, list, download e delete replicados nos 3 nós. |
| [02_concorrencia.sh](Trabalho%202/demo/02_concorrencia.sh) | dois clientes sobem o mesmo nome; o líder gera um sufixo `(1)` determinístico. |
| [03_falha_follower.sh](Trabalho%202/demo/03_falha_follower.sh) | mata um follower; as escritas continuam; ele se atualiza ao voltar. |
| [04_falha_lider.sh](Trabalho%202/demo/04_falha_lider.sh) | mata o líder, promove um follower em runtime e as escritas voltam. |
| [05_snapshot.sh](Trabalho%202/demo/05_snapshot.sh) | apaga um nó e o reconstrói a partir de um snapshot. |

### Como rodar

A partir de `Trabalho 2/`, suba o cluster e rode o cliente:

```bash
./scripts/start_nodes.sh
python3 src/client.py --nodes 127.0.0.1:5050,127.0.0.1:5051,127.0.0.1:5052
```

Comandos do cliente: `upload <local> <remoto>`, `download <remoto> <local>`, `list`, `delete <remoto>`, `exit`. Para parar tudo e limpar: `./scripts/cleanup.sh`.

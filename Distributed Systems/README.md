[<kbd><img title="English" alt="English" src="https://flagicons.lipis.dev/flags/4x3/us.svg" width="22"></kbd> English version](README_EN.md)

# INE5418 - Computação Distribuída

**Grupo 17:** Gustavo Rodrigues Alves D'Angelo, Pedro Henrique Gimenez e Tom Pereira Hunt

Os dois trabalhos da disciplina, cada um na sua pasta. O [Trabalho 1](Trabalho%201) é um encurtador de URLs distribuído com cache e circuit breaker. O [Trabalho 2](Trabalho%202) é um sistema de arquivos distribuído sobre Replicação de Máquina de Estados (SMR), replicado em 3 nós. O repositório original do Trabalho 2 é o [gustavovonn/distributed-fs](https://github.com/gustavovonn/distributed-fs).

Site de estudo para a prova da disciplina, aberto a quem quiser usar: **[distribuida.pehqge.com](https://distribuida.pehqge.com)**. Cobre a ementa em 7 módulos, com laboratórios interativos, questões discursivas corrigidas por IA e simulados montados a partir das provas antigas.

## Trabalho 1 - Encurtador de URLs distribuído

Três componentes e dois protocolos: os clientes falam TCP (JSON por linha) com um interceptador, e o interceptador fala HTTP REST com o servidor. O interceptador é transparente, o servidor não sabe que ele existe, e acrescenta Cache-Aside (LRU + TTL) e Circuit Breaker. A documentação completa está no [README do Trabalho 1](Trabalho%201/README.md).

| Caminho | Descrição |
|---|---|
| [relatorio.pdf](Trabalho%201/relatorio.pdf) | Relatório do trabalho. |
| [server/server.py](Trabalho%201/server/server.py) | Servidor REST, sobre a biblioteca padrão `http.server`. |
| [interceptor/interceptor.py](Trabalho%201/interceptor/interceptor.py) | Servidor TCP: roteamento e dispatch das requisições. |
| [interceptor/cache.py](Trabalho%201/interceptor/cache.py) | Cache LRU com TTL, thread-safe. |
| [interceptor/circuit_breaker.py](Trabalho%201/interceptor/circuit_breaker.py) | Circuit breaker (CLOSED / OPEN / HALF_OPEN). |
| [interceptor/protocol.py](Trabalho%201/interceptor/protocol.py) | Protocolo JSON por linha. |
| [clients/](Trabalho%201/clients) | Bibliotecas cliente em Python e Node.js. |
| [examples/](Trabalho%201/examples) | Demos de uso básico, cache e circuit breaker. |
| [config.txt](Trabalho%201/config.txt) | Configuração compartilhada: host, portas, cache e circuit breaker. |

## Trabalho 2 - Sistema de arquivos distribuído (SMR)

Sistema de arquivos fortemente consistente em Python puro. Faz upload, download, listagem e remoção, replicados num cluster de 3 nós e consistentes mesmo com falhas. O cliente recebe a lista de nós e descobre o líder sozinho.

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

| Documentação e scripts | Descrição |
|---|---|
| [docs/protocol.md](Trabalho%202/docs/protocol.md) | O protocolo binário em três camadas: framing, replicação e aplicação. |
| [docs/T2 - Building Blocks.pdf](Trabalho%202/docs/T2%20-%20Building%20Blocks.pdf) | Enunciado do trabalho. |
| [slides/apresentacao.pdf](Trabalho%202/slides/apresentacao.pdf) | Slides da apresentação. |
| [scripts/start_nodes.sh](Trabalho%202/scripts/start_nodes.sh) | Sobe um cluster local de 3 nós. |
| [scripts/run_tests.sh](Trabalho%202/scripts/run_tests.sh) | Roda a suíte de testes, 10 cenários. |
| [scripts/cleanup.sh](Trabalho%202/scripts/cleanup.sh) | Para os nós e limpa o ambiente de teste. |

### Demos

Cada script sobe o próprio cluster, mostra um cenário e derruba tudo no final, então rodam em qualquer ordem. Pausam em `[ENTER]` entre passos; `NOPAUSE=1` roda direto.

| Script | Cenário |
|---|---|
| [01_normal.sh](Trabalho%202/demo/01_normal.sh) | Upload, list, download e delete replicados nos 3 nós. |
| [02_concorrencia.sh](Trabalho%202/demo/02_concorrencia.sh) | Dois clientes sobem o mesmo nome; o líder gera um sufixo `(1)` determinístico. |
| [03_falha_follower.sh](Trabalho%202/demo/03_falha_follower.sh) | Mata um follower; as escritas continuam e ele se atualiza ao voltar. |
| [04_falha_lider.sh](Trabalho%202/demo/04_falha_lider.sh) | Mata o líder, promove um follower em runtime e as escritas voltam. |
| [05_snapshot.sh](Trabalho%202/demo/05_snapshot.sh) | Apaga um nó e o reconstrói a partir de um snapshot. |

### Como rodar

A partir de `Trabalho 2/`:

```bash
./scripts/start_nodes.sh
python3 src/client.py --nodes 127.0.0.1:5050,127.0.0.1:5051,127.0.0.1:5052
```

Comandos do cliente: `upload <local> <remoto>`, `download <remoto> <local>`, `list`, `delete <remoto>` e `exit`. Para parar tudo: `./scripts/cleanup.sh`.

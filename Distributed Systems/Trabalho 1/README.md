# Encurtador de URLs Distribuído — INE5418

Implementação do Trabalho 1 da disciplina INE5418 (Computação Distribuída).
Sistema composto por **três** componentes que se comunicam por dois protocolos
distintos:

```
[ Clientes ]  --(TCP socket: JSON+\n)-->  [ Interceptador / Proxy ]  --(HTTP REST)-->  [ Servidor REST ]
   Python ┐                                  ┌─ Cache-Aside (LRU + TTL)                  Python (http.server)
   Node   ┘                                  └─ Circuit Breaker                          Armazenamento em RAM
```

O interceptador é **transparente**: o servidor REST não sabe que ele existe;
do ponto de vista do cliente, o interceptador é o servidor.

## Estrutura

```
encurtador-urls/
├── config.txt                       # Configuração compartilhada (host/porta/cache/CB)
├── requirements.txt                 # Dependências Python (apenas `requests`)
├── start_all.sh / stop_all.sh       # Scripts utilitários
├── server/
│   ├── server.py                    # API REST (http.server stdlib)
│   └── config_loader.py             # Loader simples KEY=VALUE
├── interceptor/
│   ├── interceptor.py               # TCP server + roteamento + dispatch
│   ├── cache.py                     # LRU + TTL thread-safe (OrderedDict)
│   ├── circuit_breaker.py           # CB CLOSED/OPEN/HALF_OPEN
│   └── protocol.py                  # encode/parse JSON-line + LineSocket
├── clients/
│   ├── python/url_client.py         # Biblioteca cliente Python
│   └── javascript/url_client.js     # Biblioteca cliente Node.js (heterogeneidade)
├── examples/
│   ├── example_python.py            # Demo principal (cliente Python)
│   ├── example_javascript.js        # Demo principal (cliente Node.js)
│   ├── demo_cache.py                # Demo focada em HIT/MISS/invalidação/TTL
│   └── demo_circuit_breaker.py      # Demo do segundo padrão
└── logs/                            # Logs e PIDs dos processos em background
```

## Pré-requisitos

- **Python 3.10+** (testado em 3.12). A biblioteca `requests` é necessária para
  o interceptador.
- **Node.js 18+** (apenas para o cliente JavaScript; usa só a stdlib `net`,
  então não precisa de `npm install`).

Instalação da dependência Python:

```bash
pip install -r requirements.txt
# ou, equivalente, instalando direto:
pip install --user 'requests>=2.31'
```

## Como executar

```bash
cd encurtador-urls
pip install -r requirements.txt   # uma vez
./start_all.sh                    # sobe servidor REST e interceptador em background
python3 examples/example_python.py
node      examples/example_javascript.js
python3 examples/demo_cache.py
python3 examples/demo_circuit_breaker.py
./stop_all.sh
```

Logs ficam em `logs/server.log` e `logs/interceptor.log`. PIDs em `logs/*.pid`.

Para rodar manualmente em terminais separados:

```bash
# Terminal 1
python3 server/server.py
# Terminal 2
python3 interceptor/interceptor.py
# Terminal 3
python3 examples/example_python.py
```

## Configuração

Edite `config.txt`. As principais chaves:

| Chave                       | Descrição                                                  |
|-----------------------------|------------------------------------------------------------|
| `SERVER_HOST` / `SERVER_PORT`             | Endereço do servidor REST                    |
| `INTERCEPTOR_HOST` / `INTERCEPTOR_PORT`   | Endereço TCP do interceptador |
| `CACHE_MAX_SIZE`            | Tamanho máximo do cache LRU                                |
| `CACHE_TTL_SECONDS`         | TTL em segundos (0 = desabilitado, só LRU)                 |
| `CB_FAILURE_THRESHOLD`      | Falhas consecutivas para abrir o circuito                  |
| `CB_RESET_TIMEOUT_SECONDS`  | Tempo em OPEN antes de tentar HALF_OPEN                    |
| `CB_REQUEST_TIMEOUT`        | Timeout (s) das chamadas HTTP do interceptador             |

## Protocolo cliente ↔ interceptador

**Formato:** uma mensagem JSON por linha (`\n` como delimitador).

Requisições aceitas:
```jsonc
{"action": "encurta", "url": "https://..."}
{"action": "resolve", "codigo": "abc123"}
{"action": "remove",  "codigo": "abc123"}
{"action": "list"}
{"action": "stats"}    // diagnóstico: cache + circuit breaker
{"action": "ping"}
```

Respostas:
```jsonc
{"status": "ok", "codigo": "abc123", "url_curta": "http://..."}
{"status": "ok", "url_original": "https://...", "source": "cache"|"server"}
{"status": "ok", "removido": true, "cache_invalidated": true}
{"status": "ok", "urls": [...]}
{"status": "error", "code": 404, "message": "..."}
```

## API REST do servidor (uso interno do interceptador)

Endpoints do enunciado:

| Método | Caminho         | Corpo / Resposta                                                                |
|--------|-----------------|---------------------------------------------------------------------------------|
| POST   | `/urls`         | Req: `{"url":"..."}` &nbsp; Res: `{"codigo":"...","url_curta":"..."}`           |
| GET    | `/urls/{codigo}`| Res: `{"url_original":"..."}` (incrementa `acessos`)                            |
| DELETE | `/urls/{codigo}`| Res: `{"removido": true}`                                                       |
| GET    | `/urls`         | Res: `[{"codigo":"...","url_original":"...","acessos":N}, ...]`                 |

Endpoints utilitários (apenas para demos, **fora** da especificação do enunciado):

| Método | Caminho           | Descrição                                                          |
|--------|-------------------|--------------------------------------------------------------------|
| POST   | `/_debug/fail`    | Força o servidor a responder 503; usado pela demo do CB            |
| POST   | `/_debug/recover` | Volta ao modo normal                                               |

## Como validar manualmente

1. **Cache HIT/MISS:** olhe o stdout do interceptador. Cada `resolve` imprime
   `cache HIT` ou `cache MISS`. O campo `acessos` em `GET /urls` cresce só
   quando há ida ao servidor (cache miss).
2. **Invalidação:** após `remove`, um `resolve` do mesmo código deve produzir
   404 e a stats mostra `invalidations` incrementado.
3. **Circuit Breaker:** rode `examples/demo_circuit_breaker.py`. Veja `CB.state`
   transitar `CLOSED → OPEN → HALF_OPEN → CLOSED`. As tentativas em OPEN
   retornam em <1ms (fail fast).
4. **Heterogeneidade:** `examples/example_javascript.js` consome o mesmo
   interceptador via Node.js, implementando o protocolo JSON por linha do zero.
5. **Diagnóstico ao vivo:** envie `{"action":"stats"}` por qualquer cliente
   ou execute `python3 -c "from clients.python.url_client import *; ..."`.

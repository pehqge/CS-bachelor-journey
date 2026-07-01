# ========================= interceptor.py =========================
# Proxy TCP que fica no meio do caminho cliente <-> servidor REST.
#
# Cada cliente abre um socket TCP no interceptador e envia mensagens JSON
# delimitadas por '\n' (ver protocol.py). O interceptador então traduz
# isso em chamadas HTTP no servidor REST.
#
# As duas grandes responsabilidades:
#   1) Cache-Aside no resolve()  -> evita ida ao servidor quando o código
#      já foi visto recentemente.
#   2) Circuit Breaker nas chamadas HTTP -> protege o cliente quando o
#      servidor REST cai (fail-fast em vez de ficar esperando timeout).
# ====================================================================

import json
import os
import signal
import socket
import sys
import threading

import requests

# entrypoint direto (python3 interceptor/interceptor.py): precisa botar
# este diretório e o do server/ no sys.path antes dos imports locais
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "server")))

from cache import LRUCache
from circuit_breaker import CircuitBreaker, CircuitOpenError
from protocol import LineSocket, make_error, make_ok
from config_loader import load_config, get_int, get_float, get_str

# utilitário para logs
def _log(msg: str) -> None:
    sys.stderr.write(f"[interceptor] {msg}\n")
    sys.stderr.flush()


# ====================================================================
# classe principal
# ====================================================================

class Interceptor:
    def __init__(self, cfg: dict):
        # ---------- configs ----------
        self.cfg = cfg
        self.host = get_str(cfg, "INTERCEPTOR_HOST", "127.0.0.1")
        self.port = get_int(cfg, "INTERCEPTOR_PORT", 6000)
        self.server_base = (
            f"http://{get_str(cfg, 'SERVER_HOST', '127.0.0.1')}:"
            f"{get_int(cfg, 'SERVER_PORT', 5000)}"
        )
        self.req_timeout = get_float(cfg, "CB_REQUEST_TIMEOUT", 2.0)

        # ---------- componentes ----------
        self.cache = LRUCache(
            max_size=get_int(cfg, "CACHE_MAX_SIZE", 64),
            ttl_seconds=get_float(cfg, "CACHE_TTL_SECONDS", 60.0),
        )
        self.cb = CircuitBreaker(
            failure_threshold=get_int(cfg, "CB_FAILURE_THRESHOLD", 3),
            reset_timeout=get_float(cfg, "CB_RESET_TIMEOUT_SECONDS", 8.0),
        )

        # ---------- TCP SERVER ----------
        self._stop_event = threading.Event()
        self._sock = None    # listener socket; setado em serve_forever()

    # ----------------------------------------------------------------
    # ponte com o servidor REST (toda chamada HTTP passa por aqui)
    # ----------------------------------------------------------------

    def _http_call(self, method: str, path: str, **kwargs) -> requests.Response:

        url = self.server_base + path  # formatação da URL completa
        kwargs.setdefault("timeout", self.req_timeout)

        def do() -> requests.Response:
            resp = requests.request(method, url, **kwargs)

            # códigos 5xx são de falha no Circuit Breaker (servidor inoperante).
            # códigos 4xx são problema do Client (não entrando na contagem de falhas).
            if 500 <= resp.status_code < 600:
                raise requests.HTTPError(f"{resp.status_code} {resp.reason}", response=resp)

            return resp

        return self.cb.call(do)

    # ----------------------------------------------------------------
    # handlers das ações do protocolo
    # ----------------------------------------------------------------

    def handle_encurta(self, req: dict) -> dict:
        url = req.get("url")

        # sanitização da URL
        if not isinstance(url, str) or not url:
            return make_error(400, "campo 'url' obrigatório")

        # CHAMADA HTTP AO SERVIDOR
        try:
            resp = self._http_call("POST", "/urls", json={"url": url})

        except CircuitOpenError as e:
            return make_error(503, f"circuit breaker: {e}")

        except requests.RequestException as e:
            return make_error(503, f"erro de comunicação com servidor: {e}")

        # ERRO
        if resp.status_code != 201:
            return make_error(resp.status_code, _resp_message(resp))

        # SUCESSO
        data = resp.json()

        return make_ok(codigo=data["codigo"], url_curta=data["url_curta"])
    
        # ** registro em Cache apenas em resolve() (além de ser após a primeira chamada)

    def handle_resolve(self, req: dict) -> dict:
        codigo = req.get("codigo")

        # sanitização do campo código
        if not isinstance(codigo, str) or not codigo:
            return make_error(400, "campo 'codigo' obrigatório")

        # ---- VERIFICANDO NA CACHE ----
        cached = self.cache.get(codigo)

        # encontrou
        if cached is not None:
            _log(f"cache HIT  codigo={codigo}")
            return make_ok(url_original=cached, source="cache")

        # não encontrou
        _log(f"cache MISS codigo={codigo}")

        # ---- BUSCANDO NO SERVIDOR ----
        try:
            resp = self._http_call("GET", f"/urls/{codigo}")

        except CircuitOpenError as e:
            return make_error(503, f"circuit breaker: {e}")
        
        except requests.RequestException as e:
            return make_error(503, f"erro de comunicação com servidor: {e}")
        
        if resp.status_code == 404:
            return make_error(404, "código não encontrado")
        
        if resp.status_code != 200:
            return make_error(resp.status_code, _resp_message(resp))

        # verificação extra: resposta do servidor tem que ter o campo url_original
        url_original = resp.json().get("url_original")
        if not isinstance(url_original, str) or not url_original:
            return make_error(500, "resposta inválida do servidor REST")

        # registra na Cache pra proxima chamada ser HIT
        self.cache.put(codigo, url_original)
        return make_ok(url_original=url_original, source="server")

    def handle_remove(self, req: dict) -> dict:
        codigo = req.get("codigo")

        # sanitização do campo código
        if not isinstance(codigo, str) or not codigo:
            return make_error(400, "campo 'codigo' obrigatório")

        # ---- CHAMADA HTTP AO SERVIDOR ----
        try:
            resp = self._http_call("DELETE", f"/urls/{codigo}")

        except CircuitOpenError as e:
            return make_error(503, f"circuit breaker: {e}")
        
        except requests.RequestException as e:
            return make_error(503, f"erro de comunicação com servidor: {e}")

        # invalida o cache local mesmo se o servidor respondeu com erro 404
        # (o cache poderia estar com um valor velho de um servidor antigo)
        invalidated = self.cache.invalidate(codigo)

        # SUCESSO NA DELEÇÃO
        if resp.status_code == 200:
            _log(f"DELETE codigo={codigo} cache_invalidated={invalidated}")
            return make_ok(removido=True, cache_invalidated=invalidated)
        
        # ERRO NA DELEÇÃO
        if resp.status_code == 404:
            return make_error(404, "código não encontrado")

        return make_error(resp.status_code, _resp_message(resp))

    def handle_list(self, req: dict) -> dict:
        # chamada HTTP ao servidor para pegar a lista de URLs encurtadas
        try:
            resp = self._http_call("GET", "/urls")

        except CircuitOpenError as e:
            return make_error(503, f"circuit breaker: {e}")
        
        except requests.RequestException as e:
            return make_error(503, f"erro de comunicação com servidor: {e}")
        
        # ERRO
        if resp.status_code != 200:
            return make_error(resp.status_code, _resp_message(resp))
        
        # SUCESSO
        return make_ok(urls=resp.json())

    def handle_stats(self, req: dict) -> dict:
        """ retorna estatísticas do Cache e do Circuit Breaker para ajudar a monitorar o sistema e 
        debugar problemas de desempenho ou indisponibilidade do servidor REST."""

        return make_ok(
            cache=self.cache.stats.as_dict(),
            cache_size=len(self.cache),
            cache_max=self.cache.max_size,
            cache_ttl=self.cache.ttl,
            circuit=self.cb.stats(),
        )

    def handle_ping(self, req: dict) -> dict:
        return make_ok(pong=True)

    # ----------------------------------------------------------------
    # client loop
    # ----------------------------------------------------------------

    def serve_client(self, conn: socket.socket, addr) -> None:
        _log(f"cliente conectado {addr}")
        ls = LineSocket(conn)
        try:
            while not self._stop_event.is_set():
                # ---- recebe a proxima mensagem ----
                try:
                    req = ls.recv()
    
                except json.JSONDecodeError as e:
                    ls.send(make_error(400, f"JSON inválido: {e}"))
                    continue

                except ConnectionError:
                    break

                if req is None:
                    break    # peer fechou

                # ---- despacha para respectiva ação ----
                action = req.get("action")
                handler = {
                    "encurta": self.handle_encurta,
                    "resolve": self.handle_resolve,
                    "remove":  self.handle_remove,
                    "list":    self.handle_list,
                    "stats":   self.handle_stats,
                    "ping":    self.handle_ping,
                }.get(action)

                # invocamento desconhecido
                if handler is None:
                    ls.send(make_error(400, f"ação desconhecida: {action!r}"))
                    continue

                # ---- executa o handler da ação chamada ----
                try:
                    response = handler(req)
                except Exception as e:
                    _log(f"erro inesperado em {action}: {e!r}")
                    response = make_error(500, f"erro interno: {e}")
                ls.send(response)
        finally:
            ls.close()
            _log(f"cliente desconectado {addr}")

    # ----------------------------------------------------------------
    # configuração do servidor TCP
    # ----------------------------------------------------------------

    def _install_signal_handlers(self) -> None:
        def _shutdown(_signum, _frame):
            self._stop_event.set()
            if self._sock is not None:
                try:
                    self._sock.close()
                except OSError:
                    pass
        try:
            signal.signal(signal.SIGTERM, _shutdown)
            signal.signal(signal.SIGINT, _shutdown)
        except ValueError:
            # signal só funciona na main thread. em teste pode falhar (ignora)
            pass

    def serve_forever(self) -> None:
        # configura o socket TCP e entra no loop para aceitar conexões de clientes
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((self.host, self.port))
        self._sock.listen(64)
        self._install_signal_handlers()

        _log(f"escutando em {self.host}:{self.port} (REST -> {self.server_base})")

        try:
            while not self._stop_event.is_set():

                try:
                    conn, addr = self._sock.accept()

                except OSError as e:
                    # se foi sinal de parada, encerra
                    if self._stop_event.is_set():
                        break
                    _log(f"accept falhou ({e}); seguindo")
                    continue

                # uma thread por cliente - simples e suficiente para o escopo
                t = threading.Thread(
                    target=self.serve_client, args=(conn, addr), daemon=True
                )

                t.start()
                
        except KeyboardInterrupt:
            _log("encerrando")

        finally:
            if self._sock:
                try:
                    self._sock.close()
                except OSError:
                    pass


# ====================================================================
# utilitários
# ====================================================================

def _resp_message(resp: requests.Response) -> str:
    # tenta extrair {"erro": "..."} do corpo; usa o HTTP status de fallback
    try:
        body = resp.json()
        if isinstance(body, dict) and "erro" in body:
            return str(body["erro"])
    except Exception:
        pass
    return f"HTTP {resp.status_code}"


# ====================================================================
# entrypoint
# ====================================================================

def main():
    cfg = load_config()
    Interceptor(cfg).serve_forever()


if __name__ == "__main__":
    main()

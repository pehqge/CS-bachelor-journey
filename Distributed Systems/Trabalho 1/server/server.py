# ========================== server.py ==========================
# Servidor REST do encurtador. Armazenamento em memória (dict global
# protegido por lock). Comandos:
#   POST   /urls            -> encurtador {"url": ...}
#   GET    /urls            -> lista todos os encurtados
#   GET    /urls/<codigo>   -> resolve uma URL encurtada dado seu código
#   DELETE /urls/<codigo>   -> remove um registro dado o código
#
# Endpoints de debug (apenas para demo do circuit breaker):
#   POST /_debug/fail       -> todo request passa a responder 503
#   POST /_debug/recover    -> volta ao normal
# ================================================================

import json
import os
import random
import string
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit, unquote

# entrypoint direto (python3 server/server.py) - precisa do sys.path manual
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config_loader import load_config, get_int, get_str


# ----------- estado global -----------
# storage: codigo -> {"url_original": str, "acessos": int}
# (lock obrigatório pois ThreadingHTTPServer atende cada cliente numa thread)
_storage_lock = threading.Lock()
_storage: dict[str, dict] = {}

# flag de debug para forçar 503 em todos os endpoints (usada na demo do circuit breaker)
_fail_mode_lock = threading.Lock()
_fail_mode = False


# ----------- configuracao -----------
_cfg = load_config()
SHORT_CODE_LENGTH = get_int(_cfg, "SHORT_CODE_LENGTH", 6)
PUBLIC_BASE_URL = get_str(_cfg, "PUBLIC_BASE_URL", "http://127.0.0.1:5000")
SERVER_HOST = get_str(_cfg, "SERVER_HOST", "127.0.0.1")
SERVER_PORT = get_int(_cfg, "SERVER_PORT", 5000)

MAX_URL_LEN = 2048         # tamanho máximo aceito para a URL original
MAX_BODY_BYTES = 65536     # tamanho máximo da body de um request


# ================================================================
# helpers
# ================================================================

def _gen_codigo() -> str:
    # tenta gerar código único. dispara erro se não conseguir
    alphabet = string.ascii_letters + string.digits
    for _ in range(16):
        codigo = "".join(random.choice(alphabet) for _ in range(SHORT_CODE_LENGTH))
        with _storage_lock:
            if codigo not in _storage:
                return codigo
    raise RuntimeError("Não é possível gerar mais códigos únicos. Para isso, aumente SHORT_CODE_LENGTH ou limpe o armazenamento.")


def _extract_codigo(raw_path: str) -> str:
    # extrai o código da URL pura
    path = urlsplit(raw_path).path
    return unquote(path[len("/urls/"):]).rstrip("/")


def _resp_msg_404() -> dict:
    return {"erro": "rota não encontrada"}


# ================================================================
# handler HTTP
# ================================================================

class URLHandler(BaseHTTPRequestHandler):
    server_version = "EncurtadorREST/1.0"

    # ---------- I/O basico ----------

    def _send_json(self, status: int, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self):
        length = int(self.headers.get("Content-Length", "0") or 0)

        # Verificando o tamanho da body

        # tamanho excede o limite
        if length > MAX_BODY_BYTES:
            self._send_json(413, {"erro": f"payload acima de {MAX_BODY_BYTES} bytes"})
            return None
        
        # body vazia
        if length == 0:
            return {}
        raw = self.rfile.read(length)

        try:
            return json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            # se nao for json valido, devolve dict vazio. o handler vai reclamar do campo faltando
            return {}

    def _check_fail_mode(self) -> bool:
        with _fail_mode_lock:
            return _fail_mode

    def log_message(self, fmt: str, *args) -> None:
        # log padronizado (BaseHTTPRequestHandler escreve no stderr por padrao)
        sys.stderr.write("[server] %s - %s\n" % (self.address_string(), fmt % args))

    # ---------- POST ----------

    def do_POST(self):
        global _fail_mode

        # endpoints de debug precisam passar ANTES do fail_mode
        # (caso contrario o /_debug/recover trava quando o fail_mode esta ativo)

        # FAIL DEBUG MODE
        if self.path == "/_debug/fail":
            with _fail_mode_lock:
                _fail_mode = True
            self._send_json(200, {"fail_mode": True})
            return
        
        # RECOVER DEBUG MODE
        if self.path == "/_debug/recover":
            with _fail_mode_lock:
                _fail_mode = False
            self._send_json(200, {"fail_mode": False})
            return

        if self._check_fail_mode():
            self._send_json(503, {"erro": "servidor em modo de falha (debug)"})
            return

        # CRIAR URL ENCURTADA
        if self.path == "/urls":
            body = self._read_json_body()

            # dupla validação do body size
            if body is None:
                return   # _read_json_body ja respondeu erro 413

            url = body.get("url")

            # validações

            # URL ausente
            if not url or not isinstance(url, str):
                self._send_json(400, {"erro": "campo 'url' obrigatório"})
                return
            
            # URL muito longa
            if len(url) > MAX_URL_LEN:
                self._send_json(400, {"erro": f"url maior que {MAX_URL_LEN} caracteres"})
                return

            # caso positivo: tenta gerar encurtamento, armazenar e responder
            try:
                codigo = _gen_codigo()
            except RuntimeError as e:
                self._send_json(503, {"erro": str(e)})
                return
            
            # persistência no armazenamento do servidor
            with _storage_lock:
                _storage[codigo] = {"url_original": url, "acessos": 0}
            
            # response de sucesso (201 Created)
            self._send_json(201, {
                "codigo": codigo,
                "url_curta": f"{PUBLIC_BASE_URL}/r/{codigo}",
            })
            return

        self._send_json(404, _resp_msg_404())

    # ---------- GET ----------

    def do_GET(self):
        if self._check_fail_mode():
            self._send_json(503, {"erro": "servidor em modo de falha (debug)"})
            return

        path = urlsplit(self.path).path

        # CONSULTA TODOS ENCURTAMENTOS (com proteção do lock)
        if path == "/urls":
            with _storage_lock:
                items = [
                    {"codigo": k, "url_original": v["url_original"], "acessos": v["acessos"]}
                    for k, v in _storage.items()
                ]
            
            # response de sucesso com a lista de URLs encurtadas (pode ser grande, mas é só para demo mesmo)
            self._send_json(200, items)
            return

        # CONSULTA URL ORIGINAL DADO UM ENCURTAMENTO
        if path.startswith("/urls/"):
            codigo = _extract_codigo(self.path)
        
            # usuário não forneceu código, responde erro
            if not codigo:
                self._send_json(400, {"erro": "código vazio"})
                return
    
            # pega a url dentro do lock, mas a resposta TCP vai fora dele
            # (segura o lock só pelo tempo mínimo necessário)
            with _storage_lock:
                entry = _storage.get(codigo)
                if entry is None:
                    url_original = None
                else:
                    entry["acessos"] += 1
                    url_original = entry["url_original"]
            
            # caso não encontre a URL do encurtamento
            if url_original is None:
                self._send_json(404, {"erro": "código não encontrado"})
            else:
                # caso positivo: responde a URL original
                self._send_json(200, {"url_original": url_original})
            return

        self._send_json(404, _resp_msg_404())

    # ---------- DELETE ----------

    def do_DELETE(self):
        if self._check_fail_mode():
            self._send_json(503, {"erro": "servidor em modo de falha (debug)"})
            return

        path = urlsplit(self.path).path

        # REMOVER ENCURTAMENTO DADO O CÓDIGO
        if path.startswith("/urls/"):
            codigo = _extract_codigo(self.path)

            # remove do armazenamento do servidor protegendo o acesso com lock
            with _storage_lock:
                existed = _storage.pop(codigo, None) is not None

            if existed:
                # caso de sucesso, responde confirmação de remoção
                self._send_json(200, {"removido": True})
            else:
                # caso onde o código não correspondia a nenhum encurtamento
                self._send_json(404, {"erro": "código não encontrado", "removido": False})
            return

        self._send_json(404, _resp_msg_404())


# ================================================================
# entrypoint
# ================================================================

def main():
    server = ThreadingHTTPServer((SERVER_HOST, SERVER_PORT), URLHandler)
    sys.stderr.write(f"[server] Servidor REST em http://{SERVER_HOST}:{SERVER_PORT}\n")
    sys.stderr.flush()
    try:
        server.serve_forever()  # listener loop
    except KeyboardInterrupt:
        sys.stderr.write("[server] encerrando\n")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()

# ========================== url_client.py ==========================
# Cliente Python para o interceptador.
#
# O enunciado em C usa funcoes do tipo:
#   int encurta(const char *url_original, char *codigo, char *url_curta);
# (rc no retorno, ponteiros de saida para os campos extras).
#
# Como o Python nao tem ponteiros de saida, a gente
# devolve uma tupla (rc, ...campos...). Convencao do rc:
#   rc  =  0  -> sucesso
#   rc  >  0  -> repassa o status do interceptador (404, 503, ...)
#   rc  <  0  -> erro local (perdeu conexao, json invalido, etc)
# ====================================================================

import json
import socket


class URLClientError(Exception):
    """erro generico do cliente (problema de I/O ou protocolo)."""


class URLShortenerClient:
    def __init__(self,
                 host: str = "127.0.0.1",
                 port: int = 6000,
                 timeout: float = 10.0):
        self.host = host
        self.port = port
        self.timeout = timeout
        self._sock = None     # preenchido em connect()
        self._buf = b""       # buffer de bytes ja recebidos mas nao consumidos

    # ---------- ciclo de vida ----------

    # inicia a conexão do socket tcp
    def connect(self) -> None:
        if self._sock is not None:
            return    # ja conectado, nada a fazer
        s = socket.create_connection((self.host, self.port), timeout=self.timeout)
        s.settimeout(self.timeout)
        self._sock = s
        self._buf = b""

    # finaliza a conexão do socket tcp
    def close(self) -> None:
        if self._sock is not None:
            try:
                self._sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            self._sock.close()
            self._sock = None

    # __enter__ e __exit__ permitem usar 'with URLShortenerClient() as cli:'
    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()

    # ---------- I/O baixo nivel ----------

    # converte a mensagem, que era um dict gerado pelo encurta(), 
    # em string JSON, usando quebras de linha como delimitador,
    # finalmente codificando em utf-8, para enviar bytes
    def _send(self, msg: dict) -> None:
        if self._sock is None:
            self.connect()
        # ensure_ascii=False pra nao escapar acentos
        self._sock.sendall((json.dumps(msg, ensure_ascii=False) + "\n").encode("utf-8"))

    # oposto de _send: recebe a mensagem em bytes, e vai acumulando até encontrar
    # quebra de linha (\n). Depois disso decodifica o JSON e retorna um dict, que é 
    # o formato usado para gerar a mensagem
    def _recv(self) -> dict:
        if self._sock is None:
            raise URLClientError("não conectado")
        # acumula bytes ate aparecer um '\n' (1 mensagem completa)
        while b"\n" not in self._buf:
            chunk = self._sock.recv(4096)
            if not chunk:
                raise URLClientError("conexão fechada pelo interceptador")
            self._buf += chunk
        line, _, rest = self._buf.partition(b"\n")
        self._buf = rest
        return json.loads(line.decode("utf-8"))

    # chama _send e _request, fechando a conexão caso encontre erros
    def _request(self, msg: dict) -> dict:
        # uma chamada = um send + um recv
        try:
            self._send(msg)
            return self._recv()
        except (socket.error, OSError) as e:
            # socket morto: marca como nao conectado pra forcar reconexao na proxima
            try:
                if self._sock is not None:
                    self._sock.close()
            except OSError:
                pass
            self._sock = None
            self._buf = b""
            raise URLClientError(f"erro de I/O: {e}") from e
        except json.JSONDecodeError as e:
            raise URLClientError(f"resposta malformada: {e}") from e

    # ---------- API publica (espelho da assinatura C do enunciado) ----------

    # recebe URL original, retorna URL curto, rc e codigo 
    def encurta(self, url_original: str):
        """rc=0 em sucesso; codigo/url_curta voltam None se houve erro."""
        try:
            resp = self._request({"action": "encurta", "url": url_original})

        except URLClientError:
            return (-1, None, None)
        
        if resp.get("status") == "ok":
            return (0, resp.get("codigo"), resp.get("url_curta"))
        
        return (int(resp.get("code", -2)), None, None)

    # recebe codigo e retorna URL original
    def resolve(self, codigo_curto: str):
        """rc=0 em sucesso; url None se houve erro."""
        try:
            resp = self._request({"action": "resolve", "codigo": codigo_curto})

        except URLClientError:
            return (-1, None)
        
        if resp.get("status") == "ok":
            return (0, resp.get("url_original"))
        
        return (int(resp.get("code", -2)), None)

    # recebe o código, cria mensagem para o servidor para apagar url
    def remove_url(self, codigo_curto: str) -> int:
        try:
            resp = self._request({"action": "remove", "codigo": codigo_curto})
        except URLClientError:
            return -1
        return 0 if resp.get("status") == "ok" else int(resp.get("code", -2))


    def list_urls(self):
        try:
            resp = self._request({"action": "list"})
        except URLClientError:
            return (-1, [])
        if resp.get("status") == "ok":
            return (0, resp.get("urls", []))
        return (int(resp.get("code", -2)), [])

    def stats(self) -> dict:
        try:
            resp = self._request({"action": "stats"})
        except URLClientError as e:
            return {"status": "error", "message": str(e)}
        return resp

    def ping(self) -> bool:
        try:
            resp = self._request({"action": "ping"})
            return resp.get("status") == "ok"
        except URLClientError:
            return False


# --------------------------------------------------------------------
# Usamos wrappers para abrir e fechar a conexão a cada chamada.
# Usam internamente o "with URLShortenerClient() as c:" para chamar automaticamente
# o __enter__ e __exit__
# Para varias chamadas seguidas, vale a pena usar a classe direto e
# economizar o handshake TCP.
# --------------------------------------------------------------------

def encurta(url_original: str, host: str = "127.0.0.1", port: int = 6000):
    with URLShortenerClient(host, port) as c:
        return c.encurta(url_original)


def resolve(codigo_curto: str, host: str = "127.0.0.1", port: int = 6000):
    with URLShortenerClient(host, port) as c:
        return c.resolve(codigo_curto)


def remove_url(codigo_curto: str, host: str = "127.0.0.1", port: int = 6000) -> int:
    with URLShortenerClient(host, port) as c:
        return c.remove_url(codigo_curto)

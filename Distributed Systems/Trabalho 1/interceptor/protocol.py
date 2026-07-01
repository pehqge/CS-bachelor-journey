# ========================= protocol.py =========================
# protocolo cliente <-> interceptador
#
# mensagens são definidas em JSON, uma por linha (delimitador '\n'). 
# usar JSON puro em TCP daria problema porque sockets não tem indicadores
# de fronteira de mensagem - dois json grudados viram uma stream que não dá pra parsear
# de forma legal. o '\n' resolve isso de forma trivial.
#
# Invocações/ações suportadas:
#   encurta, resolve, remove, list, stats, ping
#
# formato de resposta:
#   ok    -> {"status": "ok", ...campos extras}
#   erro  -> {"status": "error", "code": int, "message": str}
# ================================================================

import json
import socket


def encode(msg: dict) -> bytes:
    # ensure_ascii=False para suportar acentos
    return (json.dumps(msg, ensure_ascii=False) + "\n").encode("utf-8")


def parse(raw_line: str) -> dict:
    return json.loads(raw_line)


class LineSocket:
    """envia/recebe mensagens delimitadas por '\\n' em um socket TCP."""

    def __init__(self, sock: socket.socket):
        self._sock = sock
        self._buf = b""    # buffer de bytes ainda nao consumidos

    def send(self, msg: dict) -> None:
        self._sock.sendall(encode(msg))

    def recv(self):
        """próxima mensagem ou None se a conexão foi fechada pelo peer."""
        # acumula bytes até aparecer um '\n'
        while b"\n" not in self._buf:

            chunk = self._sock.recv(4096)  # recebe bytes

            if not chunk:
                # peer fechou; bytes pendentes sem '\n' são lixo, descarta
                self._buf = b""
                return None

            self._buf += chunk

        line, _, rest = self._buf.partition(b"\n")
        self._buf = rest   # o que sobrou fica para o próximo recv

        return parse(line.decode("utf-8"))

    def close(self) -> None:
        # shutdown avisa o peer; close libera o fd
        try:
            self._sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass

        self._sock.close()


# ------------------------------------------------------------
# helpers para formatar respostas
# ------------------------------------------------------------

def make_error(code: int, message: str) -> dict:
    return {"status": "error", "code": code, "message": message}


def make_ok(**payload) -> dict:
    out = {"status": "ok"}
    out.update(payload)
    return out

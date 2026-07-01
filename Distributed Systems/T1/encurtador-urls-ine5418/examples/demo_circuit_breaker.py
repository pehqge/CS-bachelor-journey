# =================== demo_circuit_breaker.py ===================
# Demo do Circuit Breaker:
#   1) Força o servidor a entrar em modo de falha (POST /_debug/fail)
#   2) Dispara chamadas e observa o circuito ir pra OPEN
#   3) Espera o reset_timeout
#   4) Confirma a transição HALF_OPEN -> CLOSED com uma chamada de teste
# ================================================================

import os
import sys
import time

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "clients", "python"))
sys.path.insert(0, os.path.join(HERE, "..", "server"))

from url_client import URLShortenerClient
from config_loader import load_config, get_int, get_str

# print formatado de seção, pra organizar a saída da demo
def section(t: str) -> None:
    print(f"\n== {t} ==")


def main():
    # lê configs pra saber onde o servidor e o interceptador estao rodando
    cfg = load_config()
    server_url = f"http://{get_str(cfg, 'SERVER_HOST', '127.0.0.1')}:{get_int(cfg, 'SERVER_PORT', 5000)}"
    inter_host = get_str(cfg, "INTERCEPTOR_HOST", "127.0.0.1")
    inter_port = get_int(cfg, "INTERCEPTOR_PORT", 6000)
    threshold = get_int(cfg, "CB_FAILURE_THRESHOLD", 3)
    reset = get_int(cfg, "CB_RESET_TIMEOUT_SECONDS", 8)

    with URLShortenerClient(inter_host, inter_port) as cli:

        section("estado inicial")
        s = cli.stats()
        print(f"  circuit: {s['circuit']}")

        section("servidor saudável -> encurta normalmente")
        rc, codigo, curta = cli.encurta("https://example.com/healthy")

        print(f"  rc={rc} codigo={codigo}")
        assert rc == 0

        try:
            section("forçando fail_mode no servidor")
            r = requests.post(server_url + "/_debug/fail")
            print(f"  POST /_debug/fail -> {r.status_code} {r.text}")

            section(f"{threshold + 2} requisições -> circuito deve abrir após {threshold} falhas")

            for i in range(threshold + 2):
                rc, _, _ = cli.encurta(f"https://example.com/fail-{i}")
                s = cli.stats()
                print(f"  tentativa #{i+1}: rc={rc}  CB.state={s['circuit']['state']}  fails={s['circuit']['failure_count']} short_circuits={s['circuit']['short_circuits']}")
            
            s = cli.stats()
            assert s["circuit"]["state"] == "OPEN", "circuito deveria estar OPEN"

            section("chamada com circuito OPEN (fail-fast esperado)")
            t0 = time.monotonic()
            rc, _, _ = cli.encurta("https://example.com/should-fail-fast")
            dt = (time.monotonic() - t0) * 1000
            print(f"  rc={rc}  tempo={dt:.1f}ms")

        finally:
            # restaura o servidor ao normal, mesmo se algo acima quebrou.
            # evita que a próxima execução da demo comece quebrada.
            try:
                requests.post(server_url + "/_debug/recover", timeout=2)
            except Exception as e:
                print(f"  aviso: falha ao recuperar servidor: {e}")

        section(f"aguardando {reset + 1}s para HALF_OPEN")
        time.sleep(reset + 1)

        section("próxima chamada: HALF_OPEN -> sucesso -> CLOSED")

        rc, codigo, curta = cli.encurta("https://example.com/recovered")
        s = cli.stats()

        print(f"  rc={rc} codigo={codigo}")
        print(f"  CB.state={s['circuit']['state']}  successes={s['circuit']['successes']}")
        assert rc == 0
        assert s["circuit"]["state"] == "CLOSED"

        print("\nok.")


if __name__ == "__main__":
    main()

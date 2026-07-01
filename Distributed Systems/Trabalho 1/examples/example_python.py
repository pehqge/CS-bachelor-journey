# =================== example_python.py ===================
# Exemplo simples de uso do url_client:
# encurta -> resolve (com cache) -> lista -> remove -> stats
# =========================================================

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "clients", "python"))

from url_client import URLShortenerClient


def section(t: str) -> None:
    print(f"\n== {t} ==")


def main():
    # é possível sobrescrever host/porta por variáveis de ambiente, úteis para
    # uso em VMs e conteineres
    host = os.environ.get("INTERCEPTOR_HOST", "127.0.0.1")
    port = int(os.environ.get("INTERCEPTOR_PORT", "6000"))

    with URLShortenerClient(host, port) as cli:

        section("encurta 3 URLs")
        codigos = []
        for url in [
            "https://en.wikipedia.org/wiki/Distributed_computing",
            "https://docs.python.org/3/library/socket.html",
            "https://martinfowler.com/bliki/CircuitBreaker.html",
        ]:
            rc, codigo, curta = cli.encurta(url)
            print(f"  encurta({url!r}) -> rc={rc} codigo={codigo} curta={curta}")
            assert rc == 0
            codigos.append(codigo)

        section("resolve 3x do mesmo código (1a MISS, demais HIT)")

        for i in range(3):
            rc, original = cli.resolve(codigos[0])
            print(f"  resolve({codigos[0]}) tentativa {i+1} -> rc={rc} url={original}")
            assert rc == 0

        section("listagem")
        rc, lista = cli.list_urls()

        for item in lista:
            print(f"  - {item}")

        section("remove primeiro")
        rc = cli.remove_url(codigos[0])

        print(f"  remove({codigos[0]}) -> rc={rc}")
        assert rc == 0

        section("resolve do que foi removido (deve dar 404)")

        rc, _ = cli.resolve(codigos[0])

        print(f"  resolve({codigos[0]}) -> rc={rc} (esperado 404)")
        assert rc == 404

        section("stats")
        s = cli.stats()
        print(f"  cache:   {s.get('cache')}  size={s.get('cache_size')}/{s.get('cache_max')} ttl={s.get('cache_ttl')}s")
        print(f"  circuit: {s.get('circuit')}")


if __name__ == "__main__":
    main()

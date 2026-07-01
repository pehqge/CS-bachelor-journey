# ======================= demo_cache.py =======================
# Demo focada no cache: HIT, MISS, invalidação e TTL.
#
# O teste de TTL roda contra um LRUCache LOCAL (instanciado aqui mesmo),
# para não depender do TTL configurado no interceptador - assim a demo
# fica reproduzível mesmo se o CACHE_TTL_SECONDS estiver grande.
# =============================================================

import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "clients", "python"))
sys.path.insert(0, os.path.join(HERE, "..", "interceptor"))
sys.path.insert(0, os.path.join(HERE, "..", "server"))

from url_client import URLShortenerClient
from cache import LRUCache

# print formatado de seção, pra organizar a saída da demo
def section(t: str) -> None:
    print(f"\n== {t} ==")

# helper para evidenciar mudança entre as snapshots das chaves
def delta(a: dict, b: dict) -> dict:
    """a - b, chave por chave (pra ver o quanto MUDOU desde o snapshot inicial)."""
    return {k: a[k] - b.get(k, 0) for k in a}


def main():
    with URLShortenerClient() as cli:
        # snapshot do cache antes de comecar, para calcular delta no fim
        initial = cli.stats()["cache"]

        section("encurta 3 URLs")
        codigos = []

        for i in range(3):
            rc, c, _ = cli.encurta(f"https://example.com/p/{i}")
            assert rc == 0, rc
            codigos.append(c)

        print(f"  códigos: {codigos}")

        section("resolve 2x cada — 1a=MISS, 2a=HIT")

        for c in codigos:
            cli.resolve(c)
            cli.resolve(c)

        s = cli.stats()
        d = delta(s["cache"], initial)

        print(f"  delta desde início: {d}  (cache size atual={s['cache_size']})")
        assert d["hits"] == 3 and d["misses"] == 3, d

        section("listagem: acessos=1 por código (1 MISS = 1 ida ao server)")
        rc, lst = cli.list_urls()
        ours = [it for it in lst if it["codigo"] in codigos]

        for it in ours:
            print(f"  - {it}")

        for it in ours:
            assert it["acessos"] == 1, it

        section("remove o primeiro -> cache invalidado se ainda estiver lá")

        # garante que o codigo ESTÁ na Cache antes de remover (pode ter sido
        # removido se CACHE_MAX_SIZE < número de códigos da demo)
        cli.resolve(codigos[0])
        before_inv = cli.stats()["cache"]["invalidations"]
        cli.remove_url(codigos[0])
        s = cli.stats()
        d = delta(s["cache"], initial)

        print(f"  delta: {d}  (cache size={s['cache_size']})")
        assert s["cache"]["invalidations"] > before_inv

        section("resolve do removido -> 404 (e mais um miss)")
        rc, _ = cli.resolve(codigos[0])

        print(f"  rc={rc} (esperado 404)")
        assert rc == 404

    # ----------------------------------------------------------------
    # teste de TTL: feito num cache local, sem depender do Proxy.
    # ----------------------------------------------------------------
    section("TTL local em um LRUCache em memória (ttl=0.5s)")
    local = LRUCache(max_size=8, ttl_seconds=0.5)
    local.put("x", "https://exemplo.org")

    assert local.get("x") == "https://exemplo.org"

    time.sleep(0.7)   # garante que passou do TTL

    miss = local.get("x")

    print(f"  após 0.7s: get('x')={miss!r}  stats={local.stats.as_dict()}")
    assert miss is None
    assert local.stats.expirations >= 1

    print("\nstats do cache local:", local.stats.as_dict())


if __name__ == "__main__":
    main()

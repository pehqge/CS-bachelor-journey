# =========================== cache.py ===========================
# Cache thread-safe LRU com TTL opcional.
# OrderedDict conta com .move_to_end() e .popitem(last=False) O(1).
# =================================================================

import threading
import time
from collections import OrderedDict
from dataclasses import dataclass


@dataclass
class CacheStats:
    # contadores para acompanhar o comportamento do cache nos demos
    hits: int = 0
    misses: int = 0
    evictions: int = 0       # removido por enchimento da Cache
    expirations: int = 0     # removido por TTL
    invalidations: int = 0   # removido explicitamente por DELETE

    def as_dict(self) -> dict:
        return {
            "hits": self.hits,
            "misses": self.misses,
            "evictions": self.evictions,
            "expirations": self.expirations,
            "invalidations": self.invalidations,
        }


class LRUCache:
    def __init__(self, max_size: int, ttl_seconds: float = 0):

        # sanitização
        if not isinstance(max_size, int) or max_size <= 0:
            raise ValueError("max_size deve ser inteiro > 0")

        self._max = max_size

        # ttl=0 (ou negativo) configura Cache sem TTL
        self._ttl = float(ttl_seconds) if ttl_seconds and ttl_seconds > 0 else 0.0

        # entrada = (valor, timestamp_de_insercao)
        self._data: "OrderedDict[str, tuple[object, float]]" = OrderedDict()

        # RLock porque get() pode rebater em pop em caso de TTL expirado
        self._lock = threading.RLock()
        self.stats = CacheStats()

    # ---------- propriedades (read-only) ----------

    @property
    def max_size(self) -> int:
        return self._max

    @property
    def ttl(self) -> float:
        return self._ttl

    def __len__(self) -> int:
        with self._lock:
            return len(self._data)

    # ---------- operaçõees principais ----------

    def get(self, key: str):
        """retorna o valor associado a chave (renovando o TTL) ou None se não tiver / expirou."""
        
        # lock de proteção a Cache
        with self._lock:
            entry = self._data.get(key)

            # CACHE MISS
            if entry is None:
                self.stats.misses += 1
                return None

            # CACHE HIT (mas pode ser que tenha expirado)
            value, ts = entry

            # se passou do TTL, conta como expiracao + miss e some
            if self._ttl and (time.monotonic() - ts) > self._ttl:
                self._data.pop(key, None)
                self.stats.expirations += 1
                self.stats.misses += 1
                return None
            
            self._data.move_to_end(key)   # renova a chave na Cache -> mais recente

            self.stats.hits += 1

            return value

    def put(self, key: str, value) -> None:
        # protege a Cache com lock
        with self._lock:

            # caso já existia a chave, apenas atualiza o valor e renova a chave na Cache
            if key in self._data:
                self._data.move_to_end(key)

            # adiciona na cache
            self._data[key] = (value, time.monotonic())

            # limpa o dados excedentes na Cache retirando os registros mais antigos
            while len(self._data) > self._max:
                self._data.popitem(last=False)
                self.stats.evictions += 1

    def invalidate(self, key: str) -> bool:
        """remove a chave manualmente (usado no DELETE). devolve se existia."""
        with self._lock:
            existed = self._data.pop(key, None) is not None

            if existed:
                self.stats.invalidations += 1

            return existed

    def clear(self) -> None:
        with self._lock:
            self._data.clear()

    # ---------- utilitario p/ debugar ----------

    def snapshot(self) -> list:
        """lista [(key, value, age_seconds)] em ordem LRU (mais antigo primeiro)."""
        with self._lock:
            now = time.monotonic()
            return [(k, v, now - ts) for k, (v, ts) in self._data.items()]

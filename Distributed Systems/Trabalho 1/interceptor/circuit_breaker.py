# ===================== circuit_breaker.py =====================
# Circuit Breaker clássico de 3 estados:
#
#   CLOSED      -> tudo funciona; conta falhas consecutivas
#   OPEN        -> rejeita chamadas instantaneamente (fail-fast)
#   HALF_OPEN   -> deixa UMA chamada de teste passar; se tiver sucesso,
#                  volta pra CLOSED, senão volta pra OPEN
#
# Transições:
#   CLOSED    --(N falhas seguidas)-->  OPEN
#   OPEN      --(reset_timeout passou)->  HALF_OPEN
#   HALF_OPEN --(sucesso)-->  CLOSED
#   HALF_OPEN --(falha)-->    OPEN  (e zera o relógio)
# ================================================================

import threading
import time
from collections import deque
from enum import Enum


class CircuitState(str, Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


class CircuitOpenError(Exception):
    """CIRCUITO ABERTO: chamada rejeitada sem ir até o servidor."""


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, reset_timeout: float = 10.0):
        # threshold minimo de 1 falha; valores negativos viram 1
        self._threshold = max(1, int(failure_threshold))
        self._reset_timeout = float(reset_timeout)

        # estado atual
        self._state = CircuitState.CLOSED
        self._fail_count = 0       # falhas consecutivas no CLOSED
        self._opened_at = 0.0      # quando virou OPEN (monotonic)
        self._half_open_in_flight = False   # se já tem uma chamada de teste em execução no HALF_OPEN

        self._lock = threading.RLock()

        # contadores totais (para métricas no /stats)
        self._total_calls = 0
        self._total_short_circuits = 0
        self._total_failures = 0
        self._total_successes = 0

        # histórico curto das últimas transições (para DEBUG)
        self._state_changes: deque = deque(maxlen=100)

    # ---------- getter de estado e estatísticas ----------

    @property
    def state(self) -> CircuitState:
        with self._lock:
            # verifica se já passou o tempo de resetar (transitar para HALF_OPEN e testar)
            self._maybe_transition_to_half_open_locked()
            return self._state

    def stats(self) -> dict:
        with self._lock:
            recent = [(ts, s.value) for ts, s in list(self._state_changes)[-10:]]
            return {
                "state": self._state.value,
                "failure_count": self._fail_count,
                "threshold": self._threshold,
                "reset_timeout": self._reset_timeout,
                "total_calls": self._total_calls,
                "successes": self._total_successes,
                "failures": self._total_failures,
                "short_circuits": self._total_short_circuits,
                "recent_state_changes": recent,
            }

    # ---------- chamada principal ----------

    def call(self, fn, *args, **kwargs):
        """intermediador de uma chamada de função: se o circuito permitir, 
        executa; se não, levanta CircuitOpenError."""

        with self._lock:
            self._total_calls += 1
            # verifica primeiramente se já passou o tempo de resetar (transitar para HALF_OPEN e testar)
            self._maybe_transition_to_half_open_locked()

            # CIRCUITO ABERTO: rejeita instantaneamente sem ir até o servidor
            if self._state is CircuitState.OPEN:
                self._total_short_circuits += 1
                raise CircuitOpenError("Circuito aberto - servidor REST indisponível")

            # HALF-OPEN: apenas 1 chamada de cada vez vira "chamada de teste";
            # outras chamadas concorrentes são bloqueadas
            if self._state is CircuitState.HALF_OPEN and self._half_open_in_flight:
                self._total_short_circuits += 1
                raise CircuitOpenError("Circuito em half-open com chamada de teste em andamento")
            if self._state is CircuitState.HALF_OPEN:
                self._half_open_in_flight = True

        # chamada da função externa fora do lock (para não bloquear o circuito inteiro durante a chamada)
        try:
            result = fn(*args, **kwargs)
        except Exception as exc:
            self._on_failure()
            raise exc
        else:
            self._on_success()
            return result

    # ---------- transições ----------

    def _maybe_transition_to_half_open_locked(self):
        # deve ser chamado dentro do lock
        if self._state is CircuitState.OPEN:
            now = time.monotonic()

            # verifica tempo de reseta para transitar ao HALF_OPEN
            if (now - self._opened_at) >= self._reset_timeout:
                self._state = CircuitState.HALF_OPEN
                self._half_open_in_flight = False
                self._state_changes.append((now, self._state))

    def _on_success(self):
        with self._lock:
            self._total_successes += 1

            # HALF-OPEN: chamada de teste teve sucesso -> fecha o circuito (servidor voltou)
            if self._state is CircuitState.HALF_OPEN:
                self._state = CircuitState.CLOSED
                self._fail_count = 0
                self._half_open_in_flight = False
                self._state_changes.append((time.monotonic(), self._state))

            # CLOSED: sucesso que quebra a sequência de falhas
            elif self._state is CircuitState.CLOSED:
                # sequencia de falhas foi quebrada
                self._fail_count = 0

    def _on_failure(self):
        with self._lock:
            self._total_failures += 1

            # HALF-OPEN: chamada de teste teve falha -> reabre o circuito (servidor ainda indisponível)
            if self._state is CircuitState.HALF_OPEN:
                self._state = CircuitState.OPEN
                self._opened_at = time.monotonic()
                self._half_open_in_flight = False
                self._state_changes.append((self._opened_at, self._state))
                return

            self._fail_count += 1

            # threshold permite algumas falhas antes de abrir o circuito
            if self._fail_count >= self._threshold:
                self._state = CircuitState.OPEN
                self._opened_at = time.monotonic()
                self._state_changes.append((self._opened_at, self._state))

    # ---------- utilitários ----------

    def reset(self):
        with self._lock:
            self._state = CircuitState.CLOSED
            self._fail_count = 0
            self._opened_at = 0.0
            self._half_open_in_flight = False

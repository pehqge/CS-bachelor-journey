#!/usr/bin/env bash
# Shared helpers for the DFS recorded demo.
# Sourced by every scenario script. Not meant to be run directly.
#
# Env toggles:
#   NOPAUSE=1   -> skip the interactive "[ENTER]" pauses (run straight through)

set -uo pipefail

DEMO_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT="$( dirname "$DEMO_DIR" )"
SRC="$ROOT/src"
TEST_ENV="$ROOT/test-env"
PY="python3"
# Lista completa do cluster. O cliente recebe TODOS os endereços e descobre o
# líder sozinho (redireciona em WRONG_LEADER, pula nós mortos) -> a replicação é
# TRANSPARENTE: o usuário nunca precisa saber qual nó é o líder.
ALLNODES="127.0.0.1:5050,127.0.0.1:5051,127.0.0.1:5052"

# ---------- presentation helpers ----------
banner() { printf '\n\033[1;36m========================= %s =========================\033[0m\n' "$*"; }
step()   { printf '\n\033[1;33m>>> %s\033[0m\n' "$*"; }
note()   { printf '    \033[0;90m%s\033[0m\n' "$*"; }
pause()  { [ "${NOPAUSE:-0}" = "1" ] && return 0; printf '\n\033[0;35m[ENTER para continuar]\033[0m '; read -r _ || true; }

_hash() { shasum -a 256 "$1" 2>/dev/null | cut -c1-12 || sha256sum "$1" | cut -c1-12; }
_size() { wc -c < "$1" | tr -d ' '; }

# ---------- cluster control ----------
# cluster_up [leader_epoch=1] [snapshot_threshold=1000]
cluster_up() {
  local epoch="${1:-1}" thr="${2:-1000}"
  "$ROOT/scripts/cleanup.sh" >/dev/null 2>&1
  mkdir -p "$TEST_ENV/pids" "$TEST_ENV/logs"
  # --peers dá a todo nó a lista completa do cluster: followers redescobrem o
  # líder sozinhos após uma troca de líder, sem reinício nem reapontamento manual.
  $PY "$SRC/server.py" --role leader   --host 127.0.0.1 --port 5050 --node-id node_1 --epoch "$epoch" --snapshot-threshold "$thr" --peers "$ALLNODES" > "$TEST_ENV/logs/node_1.log" 2>&1 &
  echo $! > "$TEST_ENV/pids/node_1.pid"; disown 2>/dev/null || true; sleep 1
  $PY "$SRC/server.py" --role follower --host 127.0.0.1 --port 5051 --node-id node_2 --leader-host 127.0.0.1 --leader-port 5050 --snapshot-threshold "$thr" --peers "$ALLNODES" > "$TEST_ENV/logs/node_2.log" 2>&1 &
  echo $! > "$TEST_ENV/pids/node_2.pid"; disown 2>/dev/null || true
  $PY "$SRC/server.py" --role follower --host 127.0.0.1 --port 5052 --node-id node_3 --leader-host 127.0.0.1 --leader-port 5050 --snapshot-threshold "$thr" --peers "$ALLNODES" > "$TEST_ENV/logs/node_3.log" 2>&1 &
  echo $! > "$TEST_ENV/pids/node_3.pid"; disown 2>/dev/null || true
  sleep 2
  note "Cluster no ar  ->  node_1=LEADER:5050   node_2=follower:5051   node_3=follower:5052  (epoch=$epoch)"
}

cluster_down() { "$ROOT/scripts/cleanup.sh" >/dev/null 2>&1; note "Cluster encerrado e test-env removido."; }

# kill_node node_1|node_2|node_3
kill_node() {
  local pf="$TEST_ENV/pids/$1.pid"
  if [ -f "$pf" ]; then kill -9 "$(cat "$pf")" 2>/dev/null || true; rm -f "$pf"; fi
  note "Processo $1 morto com SIGKILL (queda abrupta: nenhum TCP FIN enviado)."
}

# start_follower node port [leader_port]
start_follower() {
  $PY "$SRC/server.py" --role follower --host 127.0.0.1 --port "$2" --node-id "$1" --leader-host 127.0.0.1 --leader-port "${3:-5050}" --snapshot-threshold 1000 --peers "$ALLNODES" > "$TEST_ENV/logs/$1.log" 2>&1 &
  echo $! > "$TEST_ENV/pids/$1.pid"; disown 2>/dev/null || true; sleep 2
  note "$1 (re)iniciado como follower na porta $2; descobre o líder atual via peer-list."
}

# promote_leader port  — flip de líder EM RUNTIME (sem matar/reiniciar o nó).
# O nó incrementa o próprio epoch (epoch+1) ao ser promovido; os demais followers
# redescobrem o novo líder sozinhos pela peer-list (não são tocados).
promote_leader() {
  $PY "$SRC/promote.py" 127.0.0.1 "$1" >/dev/null 2>&1
  sleep 2
  note "Promoção EM RUNTIME enviada a :$1 (flip follower->leader, epoch+1; sem reinício)."
  note "Os outros followers redescobrem o novo líder sozinhos — nenhum nó vivo é morto."
}

# show the last N log lines of a node (observable output requirement)
show_log() {  # show_log node_1 [N]
  local n="${1}" k="${2:-12}"
  printf '\n\033[1mlog de %s (últimas %s linhas):\033[0m\n' "$n" "$k"
  tail -n "$k" "$TEST_ENV/logs/$n.log" | sed 's/^/    /'
}

# ---------- client driver ----------
# dfs [host:port,...]
# Sem argumento usa a lista completa -> cliente acha o líder de forma transparente.
dfs() { $PY "$SRC/client.py" --nodes "${1:-$ALLNODES}"; }

# ---------- replica state verification (estado das réplicas ao final) ----------
# show_replicas [node-1-fs node-2-fs ...]   (default: all three)
show_replicas() {
  banner "ESTADO DAS RÉPLICAS"
  local nodes=("$@"); [ $# -eq 0 ] && nodes=(node-1-fs node-2-fs node-3-fs)
  local sig0="" first=1 allmatch=1
  for n in "${nodes[@]}"; do
    local d="$TEST_ENV/$n"
    printf '\n\033[1m%s\033[0m\n' "$n"
    if [ ! -d "$d" ]; then echo "  (sem diretório — nó morto/zerado)"; allmatch=0; continue; fi
    local seq; seq=$($PY -c "import json;print(json.load(open('$d/metadata.json')).get('last_applied_sequence_id','?'))" 2>/dev/null || echo '?')
    printf '  seq aplicada: %s\n' "$seq"
    local sig=""
    while IFS= read -r f; do
      [ -z "$f" ] && continue
      local b; b=$(basename "$f")
      printf '  %-28s %10s bytes  sha:%s\n' "$b" "$(_size "$f")" "$(_hash "$f")"
      sig="$sig$b:$(_hash "$f") "
    done < <(find "$d" -maxdepth 1 -type f ! -name '.*' ! -name 'metadata.json' ! -name 'snapshot_*' 2>/dev/null | sort)
    [ -z "$sig" ] && sig="(vazio)"
    if [ "$first" = "1" ]; then sig0="$sig"; first=0; else [ "$sig" != "$sig0" ] && allmatch=0; fi
  done
  echo
  if [ "$allmatch" = "1" ]; then
    printf '\033[1;32m✓ CONTEÚDO IDÊNTICO entre as réplicas comparadas — replicação consistente\033[0m\n'
  else
    printf '\033[1;31m✗ DIVERGÊNCIA detectada entre as réplicas comparadas\033[0m\n'
  fi
}

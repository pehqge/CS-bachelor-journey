#!/usr/bin/env bash
# CENÁRIO 5 — Snapshot + recuperação de nó zerado (log compaction).
# Demonstração de captura de estado global (metadata.json + .tar.gz) e restauração
# de um nó do zero via SNAPSHOT_TRANSMIT.
# threshold baixo (5) para disparar o snapshot rapidamente na demo.
source "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/_common.sh"

banner "CENÁRIO 5 — SNAPSHOT & RECUPERAÇÃO (threshold=5)"
cluster_up 1 5
pause

step "Sobe 2 arquivos. Cada upload = START+CHUNK+COMMIT (3 ops) -> 6 ops > 5 dispara snapshot"
printf 'arquivo um\n' > /tmp/dfs_s1.txt
printf 'arquivo dois\n' > /tmp/dfs_s2.txt
dfs <<'EOF'
upload /tmp/dfs_s1.txt s1.txt
upload /tmp/dfs_s2.txt s2.txt
exit
EOF
sleep 1
note "Procure no log a linha 'Triggering snapshot' e o snapshot_*.tar.gz gerado:"
show_log node_1 10
ls -1 "$TEST_ENV/node-1-fs/" | sed 's/^/      /'
pause

step "Zera completamente o node_2 (apaga o diretório) e reinicia"
kill_node node_2
rm -rf "$TEST_ENV/node-2-fs"
start_follower node_2 5051 5050
sleep 3
note "node_2 pede catch-up; como a seq pedida é antiga demais, recebe o SNAPSHOT_TRANSMIT:"
show_log node_2 14
pause

step "node_2 reconstruiu todo o estado a partir do snapshot -> réplicas idênticas"
show_replicas
pause

cluster_down

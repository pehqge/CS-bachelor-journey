#!/usr/bin/env bash
# CENÁRIO 3 — Falha de follower: Drop Rule (disponibilidade) + catch-up na volta.
# Demonstração de falha de follower, drop rule (disponibilidade) e catch-up na volta.
# Mostra: líder não trava esperando ACK de nó morto (Synchronous Blocking Trap),
# e o nó reintegra-se via CATCHUP_REQUEST ao voltar.
#
# Escopo: SÓ falha de follower. A recuperação aqui é por CATCH-UP (streaming do
# log), porque o cluster sobe com snapshot-threshold=1000 (cluster_up default) e
# o nó fica fora pouco tempo, então o líder ainda tem as ops perdidas no log.
# O caso de snapshot (nó fora tempo demais / log compactado) é o Cenário 5.
source "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/_common.sh"

banner "CENÁRIO 3 — FALHA DE FOLLOWER (Drop Rule + Catch-up)"
cluster_up
pause

step "Estado inicial: sobe file1 com os 3 nós vivos"
printf 'conteudo 1\n' > /tmp/dfs_f1.txt
printf 'conteudo 2\n' > /tmp/dfs_f2.txt
dfs <<'EOF'
upload /tmp/dfs_f1.txt file1.txt
exit
EOF
pause

step "Mata o follower node_3 e sobe file2 com apenas 2 nós vivos"
kill_node node_3
sleep 1
dfs <<'EOF'
upload /tmp/dfs_f2.txt file2.txt
exit
EOF
note "Upload teve SUCESSO mesmo com node_3 morto: o líder aplicou a Drop Rule"
note "(evicta o nó que estourou o timeout de ACK e segue com o cluster restante)."
show_log node_1 14
pause

step "node_3 ainda NÃO tem file2 (estava morto) — note a divergência esperada"
show_replicas
pause

step "Reinicia node_3 -> envia CATCHUP_REQUEST e recebe SÓ as operações que faltaram (catch-up por log)"
start_follower node_3 5052 5050
sleep 2
note "Líder ainda tinha as ops perdidas no log e fez STREAMING delas (não foi snapshot)."
note "Prova no log do líder: 'Streaming missed SMR operations to follower' (sem 'Transmitting snapshot')."
show_log node_1 8
show_log node_3 8
pause

step "Após o catch-up, as 3 réplicas voltam a ser idênticas"
show_replicas
pause

cluster_down

#!/usr/bin/env bash
# CENÁRIO 4 — Falha de LÍDER + promoção EM RUNTIME (sem eleição automática).
# Demonstração de falha do líder e promoção em runtime (sem eleição automática).
# Mostra: queda do líder, promoção de um follower em runtime (epoch+1), e
# prevenção de split-brain por epoch crescente.
source "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/_common.sh"

banner "CENÁRIO 4 — FALHA DE LÍDER (flip em runtime + redescoberta, anti split-brain)"
cluster_up 1
pause

step "Sobe um arquivo com o líder original (epoch=1) e confirma replicação"
printf 'antes da queda do lider\n' > /tmp/dfs_pre.txt
dfs <<'EOF'
upload /tmp/dfs_pre.txt antes.txt
exit
EOF
pause

step "Mata APENAS o LÍDER (node_1). Os followers detectam a queda e entram em descoberta."
kill_node node_1
sleep 3
note "Sem líder, escritas ficam paradas (replicação não tem eleição embutida — by design)."
note "node_2 e node_3 seguem VIVOS, varrendo a peer-list à procura de um novo líder."
show_log node_2 8
pause

step "Promoção EM RUNTIME: node_2 (:5051) vira LEADER no lugar — epoch+1, sem reinício"
promote_leader 5051
note "node_3 NÃO é morto nem reapontado: ele acha o node_2 sozinho pela peer-list"
note "(epoch maior derrota qualquer líder fantasma de epoch antigo)."
sleep 5
show_log node_3 8
pause

step "Cluster reconstituído: cliente usa a lista completa e DESCOBRE o novo líder sozinho"
note "O usuário NÃO informa que o líder mudou de :5050 para :5051 — a replicação é"
note "transparente: o cliente pula o nó morto e é redirecionado ao líder atual."
printf 'depois da promocao\n' > /tmp/dfs_pos.txt
dfs <<'EOF'
upload /tmp/dfs_pos.txt depois.txt
list
exit
EOF
pause

step "Réplicas vivas (node_2 novo líder + node_3) consistentes. node_1 segue morto."
show_replicas node-2-fs node-3-fs
note "node-1-fs ficou com estado obsoleto (epoch 1). Se voltasse, seus broadcasts"
note "de epoch antigo seriam REJEITADOS pelos followers -> proteção contra split-brain."
pause

cluster_down

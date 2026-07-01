#!/usr/bin/env bash
# CENÁRIO 1 — Execução normal: upload, list, download, delete + replicação nos 3 nós.
# Demonstração de um cenário normal de execução e do estado das réplicas.
source "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/_common.sh"

banner "CENÁRIO 1 — EXECUÇÃO NORMAL"
cluster_up
pause

step "Cliente faz upload de um arquivo para o LEADER (replicação síncrona para os followers)"
printf 'Trabalho de Computacao Distribuida - INE5418 - replicacao SMR.\n' > /tmp/dfs_doc.txt
dfs <<'EOF'
upload /tmp/dfs_doc.txt documento.txt
list
exit
EOF
pause

step "Verificando que o arquivo foi replicado IDENTICAMENTE nos 3 nós"
show_replicas
pause

step "Cliente baixa o arquivo do LEADER (leitura centralizada = consistência forte)"
rm -f /tmp/dfs_back.txt
dfs <<'EOF'
download documento.txt /tmp/dfs_back.txt
exit
EOF
note "Conteúdo recuperado:"; sed 's/^/      /' /tmp/dfs_back.txt
pause

step "Cliente deleta o arquivo (DELETE_FILE é replicado: some dos 3 nós)"
dfs <<'EOF'
delete documento.txt
list
exit
EOF
show_replicas
pause

cluster_down

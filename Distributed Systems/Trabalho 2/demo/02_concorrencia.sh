#!/usr/bin/env bash
# CENÁRIO 2 — Concorrência: dois clientes sobem o MESMO nome ao mesmo tempo.
# Demonstração de cenário de concorrência com colisões de nomes de arquivos.
# Mostra: sessões por UUID + sufixo "(1)" calculado DETERMINISTICAMENTE pelo líder
# (sequenciador). Followers aplicam a string exata -> determinismo SMR, sem lost-update.
source "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/_common.sh"

banner "CENÁRIO 2 — CONCORRÊNCIA (colisão de nome)"
cluster_up
pause

step "Dois clientes sobem conteúdos DIFERENTES com o MESMO nome 'relatorio.pdf' em paralelo"
python3 -c "open('/tmp/dfs_A.bin','wb').write(b'AAAA'*100)"   # 400 bytes (cliente 1)
python3 -c "open('/tmp/dfs_B.bin','wb').write(b'BBBBBB'*100)" # 600 bytes (cliente 2)
note "cliente 1 -> 400 bytes  |  cliente 2 -> 600 bytes  |  mesmo destino: relatorio.pdf"

( dfs <<'EOF'
upload /tmp/dfs_A.bin relatorio.pdf
exit
EOF
) &
( dfs <<'EOF'
upload /tmp/dfs_B.bin relatorio.pdf
exit
EOF
) &
wait
sleep 1
pause

step "Listagem: o líder resolveu a colisão -> relatorio.pdf + relatorio (1).pdf"
dfs <<'EOF'
list
exit
EOF
pause

step "Ambos os conteúdos sobreviveram (sem lost-update) e estão iguais nos 3 nós"
show_replicas
note "O líder calcula o sufixo dentro do lock do sequenciador; os followers só aplicam"
note "a string já resolvida. Por isso as 3 réplicas convergem para o mesmo estado."
pause

cluster_down

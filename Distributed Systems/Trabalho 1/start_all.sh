#!/usr/bin/env bash
# Sobe server + interceptor em background. Use stop_all.sh para parar.

set -euo pipefail
cd "$(dirname "$0")"

mkdir -p logs

# limpa restos antes de subir
if [[ -f logs/server.pid ]]; then
  kill "$(cat logs/server.pid)" 2>/dev/null || true
  rm -f logs/server.pid
fi
if [[ -f logs/interceptor.pid ]]; then
  kill "$(cat logs/interceptor.pid)" 2>/dev/null || true
  rm -f logs/interceptor.pid
fi

wait_port() {
  local host="$1" port="$2"
  for _ in $(seq 1 40); do
    if python3 -c "import socket,sys; s=socket.socket(); s.settimeout(0.2); sys.exit(0 if s.connect_ex(('${host}', ${port}))==0 else 1)" 2>/dev/null; then
      return 0
    fi
    sleep 0.1
  done
  return 1
}

echo "Iniciando servidor REST..."
python3 server/server.py > logs/server.log 2>&1 &
echo $! > logs/server.pid
if ! wait_port 127.0.0.1 5000; then
  echo "ERRO: servidor REST não respondeu na porta 5000 a tempo" >&2
  exit 1
fi

echo "Iniciando interceptador..."
python3 interceptor/interceptor.py > logs/interceptor.log 2>&1 &
echo $! > logs/interceptor.pid
if ! wait_port 127.0.0.1 6000; then
  echo "ERRO: interceptador não respondeu na porta 6000 a tempo" >&2
  exit 1
fi

echo "OK."
echo "  server      PID=$(cat logs/server.pid)      log=logs/server.log"
echo "  interceptor PID=$(cat logs/interceptor.pid) log=logs/interceptor.log"

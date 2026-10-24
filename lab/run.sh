#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export COMPOSE_PROJECT_NAME="${COMPOSE_PROJECT_NAME:-cve-2026-109618}"
export PYTHONUNBUFFERED=1
chmod +x poc.py

LABEL="CVE-2026-109618"
WITNESS="CVE-2026-109618-OOM-WITNESS"
VULN_URL="http://127.0.0.1:18220/"
PATCHED_URL="http://127.0.0.1:18221/"

down() {
  echo "== docker compose down -v =="
  docker compose -p "${COMPOSE_PROJECT_NAME}" down -v --remove-orphans || true
}

fail_setup() {
  local reason="$1"
  echo "FAIL ${LABEL} ${reason} ${WITNESS}" | tee poc-last-run.txt
  docker compose -p "${COMPOSE_PROJECT_NAME}" logs --no-color --tail=80 vuln patched || true
  down
  exit 1
}

echo "== docker compose down (clean) =="
down

echo "== docker pull php:8.4.26-apache php:8.4.27-apache =="
docker pull php:8.4.26-apache || fail_setup "vuln-image-pull-failed"
docker pull php:8.4.27-apache || fail_setup "patched-image-pull-failed"

echo "== docker compose up --build =="
up_ok=0
for attempt in $(seq 1 8); do
  if docker compose -p "${COMPOSE_PROJECT_NAME}" up --build -d; then
    up_ok=1
    break
  fi
  echo "IOC compose-up-retry attempt=${attempt}"
  sleep 20
  down
done
if [[ "${up_ok}" != 1 ]]; then
  fail_setup "compose-up-failed"
fi

echo "== wait loopback Apache 127.0.0.1:18220 (vuln) and 18221 (patched) =="
ready=0
for i in $(seq 1 90); do
  vuln_code="$(curl -sS -o /tmp/cve-2026-109618-vuln-ready.txt -w '%{http_code}' --max-time 5 "${VULN_URL}" || true)"
  patched_code="$(curl -sS -o /tmp/cve-2026-109618-patched-ready.txt -w '%{http_code}' --max-time 5 "${PATCHED_URL}" || true)"
  if [[ "${vuln_code}" == "200" ]] && [[ "${patched_code}" == "200" ]] \
    && grep -q 'CVE-2026-109618-ALIVE' /tmp/cve-2026-109618-vuln-ready.txt \
    && grep -q 'CVE-2026-109618-ALIVE' /tmp/cve-2026-109618-patched-ready.txt; then
    ready=1
    echo "IOC http-ready attempt=${i} vuln=${vuln_code} patched=${patched_code}"
    break
  fi
  echo "IOC http-wait attempt=${i} vuln=${vuln_code} patched=${patched_code}"
  sleep 2
done
if [[ "${ready}" != 1 ]]; then
  echo "== compose logs (not ready) =="
  docker compose -p "${COMPOSE_PROJECT_NAME}" logs --no-color --tail=80 vuln patched || true
  fail_setup "apache-not-ready"
fi

echo "== poc.py =="
set +e
python3 ./poc.py | tee poc-last-run.txt
rc=${PIPESTATUS[0]}
set -e

if ! tail -n1 poc-last-run.txt 2>/dev/null | grep -qE '^(SUCCESS|FAIL) '; then
  echo "FAIL ${LABEL} poc-exit=${rc} ${WITNESS}" >> poc-last-run.txt
  rc=1
fi

down
exit "${rc}"

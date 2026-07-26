#!/usr/bin/env bash
# Remap non-test host ports in the stand compose so CI does not collide with
# unrelated local stacks (e.g. another app on :3001).
# Kept for api_auto: gateway :8003, postgres :5432, kafka :9092/:9093.

set -euo pipefail

COMPOSE_FILE="${1:?compose file path required}"

if [[ ! -f "${COMPOSE_FILE}" ]]; then
  echo "Compose file not found: ${COMPOSE_FILE}" >&2
  exit 1
fi

# BusyBox/GNU sed compatible in-place edit via temp file.
tmp="$(mktemp)"
sed \
  -e 's/"3000:9000"/"13000:9000"/g' \
  -e 's/"3001:9001"/"13001:9001"/g' \
  -e 's/"3002:3000"/"13002:3000"/g' \
  -e 's/"5050:80"/"15050:80"/g' \
  -e 's/"8080:8080"/"18080:8080"/g' \
  -e 's/"8081:8080"/"18081:8080"/g' \
  -e 's/"9090:9090"/"19090:9090"/g' \
  "${COMPOSE_FILE}" > "${tmp}"
mv "${tmp}" "${COMPOSE_FILE}"

echo "Patched host ports in ${COMPOSE_FILE}"

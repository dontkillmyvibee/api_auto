#!/usr/bin/env bash
# Tear down the bank stand started by ci/stand/up.sh.

set -euo pipefail

STAND_HOST_PATH="${STAND_HOST_PATH:?STAND_HOST_PATH is required}"

if [[ ! -d "${STAND_HOST_PATH}" ]]; then
  echo "Stand path ${STAND_HOST_PATH} does not exist — nothing to tear down."
  exit 0
fi

cd "${STAND_HOST_PATH}"

if [[ -f docker-compose.kafka-host.yaml ]]; then
  docker compose -f docker-compose.yaml -f docker-compose.kafka-host.yaml down --remove-orphans
else
  docker compose -f docker-compose.yaml down --remove-orphans
fi

echo "Stand torn down."

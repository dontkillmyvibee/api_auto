#!/usr/bin/env bash
# Clone/update the bank stand and bring it up via the host Docker daemon (docker.sock).
# STAND_HOST_PATH must be the same absolute path on the Mac host and inside the job
# container (bind-mounted in GitLab runner config.toml).

set -euo pipefail

STAND_REPO="${STAND_REPO:-https://github.com/Nikita-Filonov/performance-qa-engineer-course.git}"
STAND_HOST_PATH="${STAND_HOST_PATH:?STAND_HOST_PATH is required}"
STAND_REF="${STAND_REF:-main}"
COMPOSE_KAFKA_OVERRIDE="${COMPOSE_KAFKA_OVERRIDE:-docker-compose.kafka-host.yaml}"
GATEWAY_URL="${GATEWAY_URL:-http://host.docker.internal:8003}"
WAIT_ATTEMPTS="${WAIT_ATTEMPTS:-90}"
WAIT_SLEEP_SEC="${WAIT_SLEEP_SEC:-5}"

mkdir -p "$(dirname "${STAND_HOST_PATH}")"

if [[ -d "${STAND_HOST_PATH}/.git" ]]; then
  echo "Updating stand at ${STAND_HOST_PATH}..."
  git -C "${STAND_HOST_PATH}" fetch --depth 1 origin "${STAND_REF}"
  git -C "${STAND_HOST_PATH}" checkout -f "FETCH_HEAD"
else
  echo "Cloning stand into ${STAND_HOST_PATH}..."
  git clone --depth 1 --branch "${STAND_REF}" "${STAND_REPO}" "${STAND_HOST_PATH}" \
    || git clone --depth 1 "${STAND_REPO}" "${STAND_HOST_PATH}"
fi

if [[ -f "${COMPOSE_KAFKA_OVERRIDE}" ]]; then
  cp "${COMPOSE_KAFKA_OVERRIDE}" "${STAND_HOST_PATH}/docker-compose.kafka-host.yaml"
fi

cd "${STAND_HOST_PATH}"

echo "Building base-service image..."
docker build -f Dockerfile.base -t base-service .

echo "Starting stand (docker compose)..."
docker compose \
  -f docker-compose.yaml \
  -f docker-compose.kafka-host.yaml \
  up -d --build --remove-orphans

echo "Waiting for gateway ${GATEWAY_URL}..."
for i in $(seq 1 "${WAIT_ATTEMPTS}"); do
  code="$(curl -s -o /dev/null -w "%{http_code}" "${GATEWAY_URL}/" || true)"
  if [[ "${code}" != "000" ]]; then
    echo "Gateway responded with HTTP ${code} (attempt ${i}/${WAIT_ATTEMPTS})"
    docker compose -f docker-compose.yaml -f docker-compose.kafka-host.yaml ps
    exit 0
  fi
  sleep "${WAIT_SLEEP_SEC}"
done

echo "Gateway did not become ready in time"
docker compose -f docker-compose.yaml -f docker-compose.kafka-host.yaml ps
docker compose -f docker-compose.yaml -f docker-compose.kafka-host.yaml logs --tail=80 || true
exit 1

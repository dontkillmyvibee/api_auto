#!/usr/bin/env bash
# Register an isolated project runner (Docker executor) for api-auto.
#
# Prerequisites:
#   1. docker compose -f ci/docker-compose.runner.yml up -d
#   2. GitLab → Project → Settings → CI/CD → Runners
#      → Create project runner → copy authentication token (glrt-...)
#   3. Disable shared runners on the project (optional but recommended).
#
# Usage:
#   export GITLAB_RUNNER_TOKEN='glrt-...'
#   ./ci/register-runner.sh

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
COMPOSE_FILE="${ROOT_DIR}/ci/docker-compose.runner.yml"
TOKEN="${GITLAB_RUNNER_TOKEN:-}"

if [[ -z "${TOKEN}" ]]; then
  echo "Set GITLAB_RUNNER_TOKEN to the project runner authentication token (glrt-...)." >&2
  exit 1
fi

docker compose -f "${COMPOSE_FILE}" run --rm --no-deps gitlab-runner register \
  --non-interactive \
  --url "https://gitlab.com/" \
  --token "${TOKEN}" \
  --name "api-auto-local-docker" \
  --executor "docker" \
  --docker-image "ghcr.io/astral-sh/uv:python3.13-bookworm-slim" \
  --docker-privileged=false \
  --docker-volumes "/cache" \
  --docker-extra-hosts "host.docker.internal:host-gateway" \
  --tag-list "api-auto" \
  --run-untagged=false \
  --locked=true

echo "Runner registered. Restarting:"
docker compose -f "${COMPOSE_FILE}" restart gitlab-runner
echo "Done. Check GitLab → Settings → CI/CD → Runners — status should be online."

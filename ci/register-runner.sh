#!/usr/bin/env bash
# Register an isolated project runner (Docker executor) for api-auto.
#
# New GitLab registration tokens (glrt-...) configure tags / locked / run-untagged
# in the GitLab UI when creating the runner — do NOT pass them to `register`.
#
# Prerequisites:
#   1. docker compose -f ci/docker-compose.runner.yml up -d
#   2. GitLab → Project → Settings → CI/CD → Runners → Create project runner
#      - Tags: api-auto
#      - Run untagged jobs: off
#      - Copy authentication token (glrt-...)
#   3. Disable shared runners on the project (recommended).
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
  --docker-volumes "/cache,/var/run/docker.sock:/var/run/docker.sock,/Users/anatolijkoleda/ci-stand:/Users/anatolijkoleda/ci-stand" \
  --docker-extra-hosts "host.docker.internal:host-gateway"

echo "Runner registered. Applying Mac stand mounts and restarting..."
bash "${ROOT_DIR}/ci/setup-mac-runner.sh"
echo "Done. Check GitLab → Settings → CI/CD → Runners — status should be online."

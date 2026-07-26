#!/usr/bin/env bash
# One-time Mac setup for the GitLab Docker runner + bank stand workspace.
#
# - Creates STAND host directory (bind-mounted into CI jobs)
# - Ensures runner config.toml has docker.sock + stand path volumes
# - Restarts the runner container

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
COMPOSE_FILE="${ROOT_DIR}/ci/docker-compose.runner.yml"
CONFIG_TOML="${ROOT_DIR}/ci/runner/config/config.toml"
STAND_ROOT="${STAND_ROOT:-/Users/anatolijkoleda/ci-stand}"
STAND_MOUNT="${STAND_ROOT}:${STAND_ROOT}"
SOCK_MOUNT="/var/run/docker.sock:/var/run/docker.sock"

mkdir -p "${STAND_ROOT}"

if [[ ! -f "${CONFIG_TOML}" ]]; then
  echo "Missing ${CONFIG_TOML}. Register the runner first (./ci/register-runner.sh)." >&2
  exit 1
fi

python3 - <<'PY' "${CONFIG_TOML}" "${SOCK_MOUNT}" "${STAND_MOUNT}"
import pathlib
import sys

config_path = pathlib.Path(sys.argv[1])
needed = [sys.argv[2], sys.argv[3], "/cache"]
text = config_path.read_text()
# Replace volumes = [...] under [runners.docker]
import re

def repl(match: re.Match[str]) -> str:
    items = []
    for item in needed:
        items.append(f'"{item}"')
    return "volumes = [" + ", ".join(items) + "]"

new_text, n = re.subn(r"volumes\s*=\s*\[[^\]]*\]", repl, text, count=1)
if n != 1:
    raise SystemExit("Could not patch volumes in config.toml")
config_path.write_text(new_text)
print("Patched runner volumes:", ", ".join(needed))
PY

docker compose -f "${COMPOSE_FILE}" up -d
docker compose -f "${COMPOSE_FILE}" restart gitlab-runner

echo "Mac runner ready."
echo "  stand workspace: ${STAND_ROOT}"
echo "  verify: docker compose -f ci/docker-compose.runner.yml logs --tail=20"

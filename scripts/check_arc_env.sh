#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)

if ! command -v uv >/dev/null 2>&1 && [ -x "$HOME/.local/bin/uv" ]; then
  export PATH="$HOME/.local/bin:$PATH"
fi

say() {
  printf '%s\n' "$1"
}

fail() {
  printf 'ERROR: %s\n' "$1" >&2
  exit 1
}

if ! command -v uv >/dev/null 2>&1; then
  fail "uv is required. Install it from https://docs.astral.sh/uv/getting-started/installation/"
fi

cd "$ROOT_DIR"

VENV_PYTHON="$ROOT_DIR/.venv/bin/python"
VENV_STARTER="$ROOT_DIR/.venv/bin/arc-starter"

if [ ! -x "$VENV_PYTHON" ] || [ ! -x "$VENV_STARTER" ]; then
  fail "Project environment is not synced yet. Run 'uv sync --locked --dev' first."
fi

say "==> Checking the existing project environment"

say "==> Checking the pinned Python version"
PYTHON_VERSION=$($VENV_PYTHON -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
if [ "$PYTHON_VERSION" != "3.12" ]; then
  fail "Expected Python 3.12 from the project environment, found $PYTHON_VERSION"
fi

say "==> Running import smoke check"
$VENV_PYTHON -c 'import arc_agi, rl_arc_agi_3; print("Imports OK")'

say "==> Running the golden-path local starter smoke check"
$VENV_STARTER --mode offline --max-steps 1

REMOTE_STATUS=$($VENV_PYTHON -c 'from rl_arc_agi_3.config import load_runtime_config; config = load_runtime_config(game="hack1", requested_mode="auto", render_mode="terminal", max_steps=1); print(config.api_key_status)')
say "==> Remote readiness: ARC_API_KEY is $REMOTE_STATUS"
say "Local setup is ready. Remote scorecards remain optional until you export ARC_API_KEY."
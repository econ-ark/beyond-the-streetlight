#!/usr/bin/env bash
# Quick check: only the main pipeline, from the raw data to the regression and
# the two figures shown in the slides, verified against the committed outputs
# (about 10 seconds after the environment is installed). ./reproduce.sh runs
# everything.

# The REMARK tooling runs this with $SHELL, which may not be bash.
[ -n "${BASH_VERSION:-}" ] || exec bash "$0" "$@"
set -euo pipefail
cd "$(dirname "$0")"

command -v uv >/dev/null || {
    echo "reproduce_min.sh needs uv: https://docs.astral.sh/uv/getting-started/installation/" >&2
    exit 1
}

uv sync --frozen
uv run python code/main/reproduce.py "$@"

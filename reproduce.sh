#!/usr/bin/env bash
# Reproduce every result and figure, and the slides, from the raw data
# (about 30 seconds after the environment is installed).
#
#   ./reproduce.sh                  # everything, checked against the committed outputs
#   ./reproduce.sh --refresh-fred   # use current FRED data (needs FRED_API_KEY)
#
# Needs uv (https://docs.astral.sh/uv/), which installs the environment pinned in
# uv.lock. README.md describes the Docker and conda/Binder alternatives.

# The REMARK tooling runs this with $SHELL, which may not be bash.
[ -n "${BASH_VERSION:-}" ] || exec bash "$0" "$@"
set -euo pipefail
cd "$(dirname "$0")"

command -v uv >/dev/null || {
    echo "reproduce.sh needs uv: https://docs.astral.sh/uv/getting-started/installation/" >&2
    exit 1
}

uv sync --frozen

# Main and supplementary analyses; fails if any output does not reproduce
uv run python code/main/reproduce.py --all "$@"

# Slides: render the notebook with reveal.js; GitHub Pages serves index.html
uv run jupyter nbconvert --to slides RS100_Discussion_Slides.ipynb --log-level WARN
cp RS100_Discussion_Slides.slides.html index.html

echo "Reproduction complete."

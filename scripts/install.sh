#!/bin/sh
set -eu
repo=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
python3 "$repo/scripts/validate.py"
codex plugin marketplace add "$repo" --json
codex plugin add pstack@pstack-local --json

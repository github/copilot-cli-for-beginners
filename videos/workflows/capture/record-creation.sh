#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
SKILL_ROOT="${CLI_TO_VIDEO_SKILL:-$HOME/Desktop/test/ignite-2026/.github/skills/cli-to-video}"
EXAMPLE="$SKILL_ROOT/examples/dynamic-workflows"
SOURCE_APP="$(cd ../.. && pwd)/samples/book-app-project"
OUTPUT="$PWD/creation"
mkdir -p "$OUTPUT/capture/tapes"
cp capture/tapes/console-settings.tape "$OUTPUT/capture/tapes/settings.tape"
cp capture/tapes/workflow-create.tape "$OUTPUT/capture/tapes/workflow-create.tape"
CAPTURE_PYTHON="${CAPTURE_PYTHON:-python3.14}" \
PREFLIGHT='python -m pytest -q -p no:cacheprovider tests/' \
FIXTURE_INSTRUCTIONS="$EXAMPLE/fixture-instructions.md" \
AFTER_TAPE="$EXAMPLE/hooks/after-tape.sh" \
  bash "$SKILL_ROOT/scripts/record.sh" "$SOURCE_APP" "$OUTPUT" workflow-create

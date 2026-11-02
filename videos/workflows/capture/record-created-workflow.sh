#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
OUTPUT="$PWD/creation"
SKILL_ROOT="${CLI_TO_VIDEO_SKILL:-$HOME/Desktop/test/ignite-2026/.github/skills/cli-to-video}"
EXAMPLE="$SKILL_ROOT/examples/dynamic-workflows"
SOURCE_APP="$(cd ../.. && pwd)/samples/book-app-project"
export CAPTURE_HOME
CAPTURE_HOME="$(cat "$OUTPUT/capture-home.txt")"
export DEMO_APP="$CAPTURE_HOME/demo-app"
EXTENSION="$DEMO_APP/.github/extensions/book-release-check/extension.mjs"
test -f "$EXTENSION"
PYTHON_EXECUTABLE="$("$CAPTURE_HOME/bin/python3" -c 'import sys; print(sys.executable)')"
if [ ! -e "$CAPTURE_HOME/bin/python" ]; then
  ln -s "$PYTHON_EXECUTABLE" "$CAPTURE_HOME/bin/python"
fi
export PATH="$CAPTURE_HOME/bin:$PATH"
HOME="$CAPTURE_HOME" python -m pytest -q -p no:cacheprovider "$DEMO_APP/tests/"
node --check "$EXTENSION"
shasum -a 256 "$EXTENSION" > "$OUTPUT/assets/workflow-before-run.sha256"
export COPILOT_GITHUB_TOKEN
COPILOT_GITHUB_TOKEN="$(gh auth token)"
export COPILOT_AUTO_UPDATE=false
unset COPILOT_CUSTOM_INSTRUCTIONS_DIRS COPILOT_SUPERVISED COPILOT_LOADER_PID
cp capture/tapes/workflow-created-run.tape "$OUTPUT/capture/tapes/"
cp capture/tapes/console-report.tape "$OUTPUT/capture/tapes/report.tape"
cp capture/tapes/workflow-created-report.tape "$OUTPUT/capture/tapes/"
cd "$OUTPUT/capture"
vhs tapes/workflow-created-run.tape
test -s "$DEMO_APP/release-report.md"
vhs tapes/report.tape
vhs tapes/workflow-created-report.tape
cp "$DEMO_APP/release-report.md" "$OUTPUT/assets/release-report.md"
cp "$EXTENSION" "$OUTPUT/assets/generated-extension.mjs"
shasum -a 256 "$EXTENSION" > "$OUTPUT/assets/workflow-after-run.sha256"
cmp "$OUTPUT/assets/workflow-before-run.sha256" "$OUTPUT/assets/workflow-after-run.sha256"
node "$EXAMPLE/hooks/record-origin.mjs" "$OUTPUT" "$SOURCE_APP"

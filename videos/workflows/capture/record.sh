#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

for tool in vhs ttyd ffmpeg ffprobe copilot gh; do
  command -v "$tool" >/dev/null || { echo "Missing required tool: $tool" >&2; exit 1; }
done
CAPTURE_PYTHON="${CAPTURE_PYTHON:-python3}"
PYTHON_EXECUTABLE="$("$CAPTURE_PYTHON" -c 'import sys; assert sys.version_info >= (3, 10), "Use Python 3.10+ via CAPTURE_PYTHON"; print(sys.executable)')"

export CAPTURE_HOME
CAPTURE_HOME="$(mktemp -d /private/tmp/ghcp-workflows.XXXXXX)"
bash setup-env.sh "$CAPTURE_HOME"
mkdir -p "$CAPTURE_HOME/bin"
ln -s "$PYTHON_EXECUTABLE" "$CAPTURE_HOME/bin/python3"
export PATH="$CAPTURE_HOME/bin:$PATH"
HOME="$CAPTURE_HOME" python3 -m pytest --version
mkdir -p "$CAPTURE_HOME/book-app/.github/extensions/book-release-check" ../assets ../renders
cp book-release-check/extension.mjs "$CAPTURE_HOME/book-app/.github/extensions/book-release-check/"
printf '%s\n' "$CAPTURE_HOME" > ../capture-home.txt
export COPILOT_GITHUB_TOKEN
COPILOT_GITHUB_TOKEN="$(gh auth token)"
export COPILOT_AUTO_UPDATE=false

TAPE="${1:-workflow-demo}"
vhs validate "tapes/$TAPE.tape"
echo "Warming up authentication and first-run notices..."
vhs tapes/preflight.tape >/dev/null
echo "Recording $TAPE..."
vhs "tapes/$TAPE.tape"
if [ "$TAPE" = workflow-demo ]; then
  test -s "$CAPTURE_HOME/book-app/release-report.md"
  cp "$CAPTURE_HOME/book-app/release-report.md" ../assets/release-report.md
  vhs tapes/report.tape
fi

#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
CAPTURE_HOME="${1:?Pass a newly created temporary HOME directory}"
APP="$CAPTURE_HOME/book-app"

mkdir -p "$APP/.github/extensions" "$CAPTURE_HOME/.copilot"
rsync -a --exclude '__pycache__' --exclude '.pytest_cache' --exclude '*.pyc' \
  "$PROJECT_ROOT/samples/book-app-project/" "$APP/"

cat > "$CAPTURE_HOME/.copilot/settings.json" <<JSON
{
  "showTipsOnStartup": false,
  "streamerMode": true,
  "banner": "never",
  "experimental": true,
  "ide": { "autoConnect": false },
  "updateTerminalTitle": false
}
JSON
printf '{"trustedFolders":["%s"]}\n' "$APP" > "$CAPTURE_HOME/.copilot/config.json"

cat > "$APP/.github/copilot-instructions.md" <<'MD'
# Book app recording

This is an isolated copy of the course's Python book collection app.
Keep responses short and beginner-friendly. Do not change application code.
When explicitly asked to run a dynamic workflow, use the registered workflow.
Do not recreate it or substitute normal subagents.
MD

cat > "$APP/.gitignore" <<'EOF'
__pycache__/
.pytest_cache/
*.pyc
release-report.md
EOF
git -C "$APP" init -q -b main

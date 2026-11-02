#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
node production/build.mjs
node production/verify.mjs

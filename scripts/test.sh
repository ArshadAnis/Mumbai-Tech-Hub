#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

pushd backend >/dev/null
poetry install --no-interaction --no-ansi
pytest
popd >/dev/null

if command -v flutter >/dev/null; then
  pushd mobile >/dev/null
  flutter pub get
  flutter test
  popd >/dev/null
else
  echo "Flutter not installed; skipping mobile tests" >&2
fi

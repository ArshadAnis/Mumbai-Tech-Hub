#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
export COMPOSE_PROJECT_NAME=moneytrader
cd ops

docker compose up --build

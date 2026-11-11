#!/usr/bin/env bash
set -euo pipefail
BASE_URL="${1:?Usage: ./scripts/smoke-test.sh https://SERVICE_URL}"
BASE_URL="${BASE_URL%/}"
echo "[1/4] Health endpoint"
curl --fail --silent --show-error "${BASE_URL}/healthz"
echo
echo "[2/4] Build metadata"
curl --fail --silent --show-error "${BASE_URL}/api/v1/info"
echo
echo "[3/4] Resource collection"
curl --fail --silent --show-error "${BASE_URL}/api/v1/resources"
echo
echo "[4/4] POST echo"
curl --fail --silent --show-error -X POST "${BASE_URL}/api/v1/echo" \
  -H "Content-Type: application/json" \
  -d '{"message":"smoke test","correlation_id":"shell-001"}'
echo

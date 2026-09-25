#!/usr/bin/env bash
# Reference run for the Module 20 capstone kit.
#
#   ./run_reference.sh
#
# Starts the sandbox (port 8765 or $PORT), then:
#   1. runs the round-0 variants  -> expect 2 failures (F-1 TEST_DEFECT, F-2 PRODUCT_DEFECT)
#   2. runs the reference suite   -> expect 11 passed, 1 xfailed (strict, DEF-5561)
#   3. runs the G1/G2 sequence gate
#   4. runs package_check.py      -> expect all required rows PASS
#   5. prints the cost summary
set -euo pipefail
cd "$(dirname "$0")"

PY="${PYTHON:-python3}"
PORT="${PORT:-8765}"
export SANDBOX_URL="http://127.0.0.1:${PORT}"

"$PY" tools/mock_sandbox_api.py --port "$PORT" >/tmp/capstone-sandbox.log 2>&1 &
SERVER_PID=$!
trap 'kill "$SERVER_PID" 2>/dev/null || true' EXIT

for _ in $(seq 1 40); do
  if curl -sf "$SANDBOX_URL/health" >/dev/null 2>&1; then break; fi
  sleep 0.25
done

echo "=== round 0 (seeded defects; expect 2 failed) ==="
"$PY" -m pytest tests/variants/round0 -q || true

echo
echo "=== round 1 (reference suite; expect 11 passed, 1 xfailed) ==="
"$PY" -m pytest tests/test_req_2502_cancel_reason.py tests/test_req_2502_audit.py -q

echo
echo "=== G1/G2 sequence gate ==="
"$PY" tools/sequence_gate.py --run req-2502-run-01

echo
echo "=== package_check.py (CA-1…CA-10) ==="
"$PY" tools/package_check.py

echo
echo "=== cost summary ==="
"$PY" tools/cost_summary.py --run req-2502-run-01 --usd-per-mtok 6.0

echo
echo "Done. Sandbox stopped."

#!/usr/bin/env bash
# Offline kit: reset the run to its starting state for another drill pass.
# Usage: reset.sh [pipeline-root]   (default: current directory)
set -euo pipefail

KIT="$(cd "$(dirname "$0")" && pwd)"
ROOT="${1:-.}"
RUN_DIR="$ROOT/runs/req-2481-run-02"

mkdir -p "$RUN_DIR" "$ROOT/tests"
cp -r "$KIT/fixture-run/." "$RUN_DIR/"
cp "$KIT/variants/tests_round0.py" "$ROOT/tests/test_req_2481_order_cancellation.py"

rm -f "$RUN_DIR/gate_log.jsonl" "$RUN_DIR/HALT" "$RUN_DIR/TAMPER" "$RUN_DIR/decision_packet.md"
rm -rf "$RUN_DIR/findings"

(cd "$ROOT" && python3 "$KIT/hash_state.py")
echo "reset complete: $RUN_DIR"

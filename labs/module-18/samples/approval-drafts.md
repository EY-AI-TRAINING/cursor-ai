# Approval drafts — packet, approver, commit guard (flawed)

> Read-only fixture for Lab 18.6 Step 1. Three excerpts, all written by a team in a hurry.
> Find the defects that make the sign-off untrustworthy; the answer key is in `facilitator-notes.md`.

## 1. Decision packet — `decision_packet.md` (draft)

```markdown
## Sign-off requested: REQ-2481 order cancellation tests

The Reviewer said APPROVE, so the pipeline is done and the tests are safe to commit.

Agent transcript (excerpt):
  Test Generator: I added the missing marker and re-ran collection — all 5 tests collect now.
  API Validator: One failure is the sandbox returning 404 where the spec says 403. Not our problem.
  Reviewer: Everything looks good, approving.

Files changed: tests/test_req_2481_order_cancellation.py
```

## 2. Approver — `tools/approve.py` (draft)

```python
#!/usr/bin/env python3
"""Record the sign-off decision in the gate log."""
import json
import pathlib
import sys
import time

run_id, decision = sys.argv[1], sys.argv[2]
run_dir = pathlib.Path("runs", run_id)

entry = {"ts": time.time(), "run_id": run_id, "gate": "HITL_signoff",
         "decision": decision, "decided_by": "automated"}

with open(run_dir / "gate_log.jsonl", "a") as log:
    log.write(json.dumps(entry) + "\n")

print(f"recorded {decision}")
```

## 3. Commit guard — `githooks/pre-commit` (draft)

```bash
#!/usr/bin/env bash
# Refuse generated-test commits unless the run has a sign-off entry.
set -euo pipefail

run_id=$(cat runs/CURRENT_RUN 2>/dev/null || echo "")
if [ -z "$run_id" ]; then
  exit 0
fi

if grep -q '"gate": "HITL_signoff"' "runs/$run_id/gate_log.jsonl"; then
  echo "approval found"
  exit 0
fi

echo "no approval recorded"
exit 1
```

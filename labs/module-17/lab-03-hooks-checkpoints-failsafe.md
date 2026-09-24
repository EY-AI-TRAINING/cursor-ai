# Lab 17.3 — Wire the Hooks, Place the Checkpoints, Prove Fail-Safe

**Module 17 · Quality Gates, Hooks & Self-Correction Fundamentals | Xebia — Cursor AI Training**
Day 5 · Lab 3 of 3 · ~8 minutes · Individual or pairs

> **Objective:** enforce the pipeline's policy with deterministic hooks that the model cannot forget —
> secrets blocked, shell commands allow/deny/ask, edits logged, the stage gate run on `stop`. Trace every
> decision, place exactly **two** human checkpoints where risk justifies them, and run the fail-safe
> drill: break the gate config and confirm the pipeline halts with **NEEDS_HUMAN**, never PASS.

**Guide references:** Module 17, §3 (hooks), §4 (HITL placement), §6 (gate logging, fail-safe), §7 walkthrough tasks 3, 4 and 6
**Learning objectives covered:** 3 — hooks for validation, policy, logging, lifecycle; 4 — HITL checkpoints; 6 — gate logging and fail-safe behaviour.

---

## Before you start

- Labs 17.1–17.2 complete: `gates.yaml` v1.0.0, routing and bounds designed
- Open [`samples/hooks-draft.md`](samples/hooks-draft.md) (review), [`samples/hook-events.jsonl`](samples/hook-events.jsonl) (test events), [`samples/gate-log-excerpt.md`](samples/gate-log-excerpt.md) (broken trail)
- Repair into `<pipeline-root>/.cursor/hooks.json` + `.cursor/hooks/*.sh`; create `runs/req-2481-run-01/gate_log.jsonl` if missing
- Hook events, payload fields, and response keys vary by Cursor release — check the current docs. The **patterns** (allow/deny/ask, log, fail-safe) are what these labs assess; scripts are runnable from the terminal with or without Cursor's hook runtime

---

## Step 1 — Repair the hook configuration and scripts

- [ ] `.cursor/hooks.json` registers at least: `beforeReadFile` (secrets), `beforeShellExecution` (shell policy), `afterFileEdit` (log + scope), `stop` (stage gate)
- [ ] `deny-secrets.sh` — denies every secret path you can name: `.env*`, `creds/**`, `**/secrets/**`, `.aws/credentials`, `*.pem`; allows ordinary files; logs each decision
- [ ] `shell-policy.sh` — an explicit **allow-list** (e.g., `pytest`, `ruff`, `python3 -m pytest`), an explicit **deny-list** (`git push`, `rm -rf`, `curl`, `wget`), `ask` for dependency installs, and **default `ask`** for anything unknown
- [ ] Every hook script has a **fail-safe** error path: unexpected error → `deny` (for `before*` hooks) or `NEEDS_HUMAN` (for the gate), never `allow`/`PASS`
- [ ] Every hook appends one audit line to `runs/hook_log.jsonl`: `{ts, run_id, event, target, decision}`
- [ ] `after-edit-log-and-scope.sh` logs the edited path and flags (does not silently allow) writes outside `tests/**`, `runs/**`, `.cursor/**` policy files
- [ ] `run-stage-gate.sh` skeleton (complete it — bash or python3, no extra dependencies):

```bash
#!/usr/bin/env bash
set -euo pipefail
RUN_ID="${RUN_ID:-req-2481-run-01}"
GATE="${GATE:-G3_tests_collect_and_conform}"
LOG="runs/${RUN_ID}/gate_log.jsonl"
emit() { # $1 = decision, $2 = extra JSON fields (optional)
  printf '{"ts":"%s","run_id":"%s","gate":"%s","decision":"%s","decided_by":"automated"%s}\n' \
    "$(date -u +%FT%TZ)" "$RUN_ID" "$GATE" "$1" "${2:-}" >> "$LOG"
  echo "$1"
}
trap 'emit NEEDS_HUMAN ",\"error\":\"stage-gate script failed (fail-safe)\""' ERR
test -f gates.yaml || { emit NEEDS_HUMAN ',"error":"gates.yaml missing"'; exit 0; }
# TODO: evaluate the G3 checks (envelope exists, collect-only exit 0, markers present, scope clean)
# PASS/FAIL/NEEDS_HUMAN must each go through emit
```

---

## Step 2 — Trace the hook decisions before running them

For each event in `samples/hook-events.jsonl`, predict the decision and the log line:

| Event | Target | Decision (allow / deny / ask) | Why | Logged to |
|---|---|---|---|---|
| `beforeReadFile` | `tests/test_req_2481_*.py` | | | |
| `beforeReadFile` | `creds/aws-credentials.csv` | | | |
| `beforeShellExecution` | `pytest --collect-only -q tests/` | | | |
| `beforeShellExecution` | `git push origin main` | | | |
| `beforeShellExecution` | `pip install requests` | | | |
| `beforeShellExecution` | `rm -rf runs/` | | | |
| `afterFileEdit` | `tests/test_req_2481_*.py` | | | |

- [ ] All seven predicted; no default-allow anywhere
- [ ] One sentence each: what the **rule** (Module 8) says about secrets, and what the **hook** adds to it

---

## Step 3 — Run the scripts and record actual behaviour

Pipe the events into your scripts (works without Cursor hooks — the scripts read stdin):

```bash
echo '{"event":"beforeShellExecution","command":"git push origin main"}' | .cursor/hooks/shell-policy.sh
while IFS= read -r line; do echo "$line" | .cursor/hooks/shell-policy.sh; done < samples/hook-events.jsonl
cat runs/hook_log.jsonl | tail -5
```

- [ ] Runner outputs match the Step 2 predictions; mismatches fixed in the script (not in the prediction)
- [ ] `runs/hook_log.jsonl` has one line per decision with target and decision
- [ ] One sentence: why the `pip install` case is `ask` rather than `deny` — and why unknown commands are not

---

## Step 4 — Place the human checkpoints (exactly two)

- [ ] Checkpoint 1 — the **ambiguous input** path: G1 `NEEDS_HUMAN` → requirement owner; what the owner sees and what resumes afterwards
- [ ] Checkpoint 2 — the **irreversible/outward** step: commit/PR approval after G5, covering both `APPROVE` and `ESCALATE`; what the approver sees
- [ ] Name the **tempting third** checkpoint that would mostly cause approval fatigue, and why it is low-impact/reversible enough to automate + log instead
- [ ] One sentence: where the two other human paths in the design (loop exhaustion, control-plane failure) land — same checkpoint or a new one?

Decision packet — the approver must not receive a chat transcript. List the fields:

- [ ] decision needed · gate trail (G1–G5 with rounds) · coverage + open defects · diff scope · risk notes (hook findings) · cost · evidence paths

---

## Step 5 — Fail-safe drill: break the gate on purpose

```bash
mv gates.yaml gates.yaml.hidden
RUN_ID=req-2481-run-01 GATE=G3_tests_collect_and_conform .cursor/hooks/run-stage-gate.sh
tail -2 runs/req-2481-run-01/gate_log.jsonl
mv gates.yaml.hidden gates.yaml
```

- [ ] With `gates.yaml` missing, the script outputs **NEEDS_HUMAN** — not PASS, not a crash with no verdict
- [ ] `gate_log.jsonl` contains the failure with `decision: NEEDS_HUMAN` and an `error` field
- [ ] After restoring the config, a normal evaluation runs again (PASS/FAIL as appropriate)
- [ ] One sentence: which real-world failures the drill stands in for (unparsable judge output, crashed validator, unreachable runner), and what each must default to

---

## Step 6 — Make the trail auditable

Define the gate-log schema from §6 in `notes/module17/gate-log-schema.md` and repair the excerpt's worst entries:

| Field | Why it is there | Required on |
|---|---|---|
| `ts` · `run_id` · `gate` | identity | every entry |
| `gates_version` | verdict is relative to criteria revision | every entry |
| `round` | retry history | retryable gates |
| `input_ref` + hash | proves which artifact was judged | every entry |
| `checks[]` `{id, result, detail}` | which criterion failed, not just the verdict | every entry |
| `routed_to` | correction routing | on FAIL |
| `decided_by` (`automated` / `llm-judge@v` / `human:<role>`) | machine vs. human accountability | every entry |
| `reason` | mandatory for human overrides and ESCALATE | human / ESCALATE entries |
| `duration_ms` · `error` | performance and failure of the gate itself | all / on error |

- [ ] Schema written with the required-on column completed
- [ ] The crash entry (recorded as PASS) rewritten correctly as NEEDS_HUMAN + error
- [ ] The human approval entry rewritten with `decided_by: human:<role>`, `reason`, and `evidence`
- [ ] One sentence: why an unrecorded approval "might as well not have happened"

---

## Evidence

- `.cursor/hooks.json` + `.cursor/hooks/*.sh` — repaired config; fail-safe defaults; allow/deny/ask
- `runs/hook_log.jsonl` — one audit line per decision (from Step 3)
- Hook decision table with predictions and actual outputs
- Two-checkpoint justification + fatigue third + decision-packet field list
- `runs/req-2481-run-01/gate_log.jsonl` — fail-safe drill entry
- `notes/module17/gate-log-schema.md` + repaired entries

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Hook script prints nothing | No branch matched, no default | Add a default decision (`ask` for policy hooks, `NEEDS_HUMAN` for gates) — silence is not permission |
| `before*` hook errors and the action proceeds | Fail-open error path | Wrap in a trap that denies on any error; fail-safe means deny/halt, never allow |
| Secrets hook only blocks `.env` | Deny-list treated as examples | Enumerate the real secret paths from Module 14's access policy and log denials |
| Every `pytest` run needs a human | Checkpoint placed on a low-impact action | Automate + log reversible sandbox actions; keep humans for irreversible decisions |
| Gate log entries have no version or input hash | Schema defined after writing | Add both to the emitter; a verdict without criteria version and artifact revision is not auditable |
| Approval recorded as "APPROVED" | No decision fields | Record `decided_by`, `reason`, and evidence paths — an unrecorded approver is no approver |
| Drill shows a stack trace and nothing else | No fail-safe wrapper | Catch the error, emit NEEDS_HUMAN, log it, exit 0 — the pipeline must always get a verdict |

---

## Checkpoint questions

1. What does a hook enforce that a rule cannot?
2. Justify the two HITL checkpoints you placed. Why would a third checkpoint on every generated test file cause approval fatigue?
3. The gate script crashes with an exception. What verdict is recorded, and what must not happen?

<details>
<summary>Answers</summary>

1. A rule tells the model what it should do and is usually followed; a hook is deterministic code that always runs, can block an action (`allow`/`deny`/`ask`), and records it. Rules explain *why*; hooks guarantee it.
2. Checkpoint 1: ambiguous input needs owner intent (G1 NEEDS_HUMAN). Checkpoint 2: commit/PR is irreversible and outward-facing, and carries the ESCALATE decision. A third on every test-file edit is low-impact and reversible — rubber-stamping sets in, and the checkpoint stops protecting anything.
3. **NEEDS_HUMAN**: halt the stage, log the error with run/stage identity, and quarantine partial artifacts. It must never be recorded as PASS — continuing without a trustworthy verdict is failing open.

</details>

---

## Next

**Lab 17.4 (optional, take-home) — Rehearse Module 18: Dry-Run All Five Gates**, then **Module 18 — Use Case Lab 4** automates everything you just designed: gates between the generator, validator, and reviewer; the bounded correction loop; downstream reruns; hooks; and the human approval checkpoint with its trail.

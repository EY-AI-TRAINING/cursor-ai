# Lab 20.1 — Kickoff, Roles & the Parameterised Control Plane

**Xebia — Cursor AI Training | AI-Assisted Software Engineering**
Day 7 · Module 20 · Lab 20.1 of 10 · ~20 min (15-minute kickoff + 5) · Team (3–4)

> **Objective:** leave the kickoff with the capstone's identity in **one manifest**, the control
> plane parameterised so no tool hard-codes REQ-2481 any more, and every role named. A capstone
> with a hard-coded run ID silently guards the wrong tests; a capstone with a collapsed role
> approves its own output. Fix both before the first token is spent.

**Guide reference:** §0 Kickoff & Scoping
**Learning objectives covered:** 1 (unseen ticket → bundle, clarifications raised), 6 (gates/CI/readiness), 7 (optional delegation)

**Placeholder convention:** `<capstone-root>` is your repository — your Modules 18–19 pipeline, or a
copy of [`samples/capstone-kit/`](samples/capstone-kit/README.md) if you are on Path B. The ticket is
**REQ-2502**, the run `req-2502-run-01`, the branch `feat/REQ-2502-cancel-reason`.

## Before you start

| Need | Notes |
|---|---|
| Team formed (3–4) | Roles from your Lab 19.8 charter |
| `<capstone-root>` ready | Own repo, or: `cp -r labs/module-20/samples/capstone-kit /tmp/req-2502-capstone && cd /tmp/req-2502-capstone` |
| Python 3.11+ with `pytest`, `pyyaml` | For Path B: `PYTHON=/path/to/python3 ./run_reference.sh` proves the kit first |
| Flawed manifest | [`samples/capstone-yaml-draft.yaml`](samples/capstone-yaml-draft.yaml) |

---

## Steps

### Step 1 — Fill the run manifest (5 min)

Read the draft manifest and record *defect → consequence → fix* for **all six planted problems**
in `notes/capstone/kickoff-review.md`. Then write your own `capstone.yaml`.

| Check | Rule |
|---|---|
| `ticket` / `run_id` | The **new** ticket and run — never the previous module's values |
| `tests_glob` | Matches only the new tests (`tests/test_req_2502_*.py`); the old glob leaves them unguarded |
| `branch` | `feat/REQ-2502-<slug>` — the convention your Lab 19.3 checker enforces |
| `sandbox_url_var` | The **name** of the env var (`SANDBOX_URL`), never the value |
| `team` | Five roles; **quality lead ≠ pipeline engineer** (the sign-off must not be the author) |
| `scope.out` | Explicit: production code, real tracker writes, auto-merge, secrets in repo |

- [ ] All six draft defects identified with consequences
- [ ] `capstone.yaml` committed on the feature branch
- [ ] `runs/CURRENT_RUN` points at `req-2502-run-01`

### Step 2 — Parameterise the control plane before anything else

Module 18's `approve.py`, `githooks/pre-commit` and `readiness.py` contain the literal
`tests/test_req_2481_*.py` and the old run ID. Every tool must now read `capstone.yaml`.

- [ ] Replace the literals with manifest reads (`tests_glob`, `run_id`, `ticket`)
- [ ] A **second person** reviews the change (it is a control-plane edit; CODEOWNERS applies)
- [ ] Smoke test against the previous run: `req-2481-run-02` still produces the same
      `package_check` / gate results as before — parameterising changed nothing else
- [ ] Path B proof that the tools really read the manifest: in a scratch copy, set
      `tests_glob: tests/does_not_exist_*.py` and run `python3 tools/package_check.py` —
      CA-4 and CA-7 must fail with "0 test files"; restore the glob

> A control-plane change without a second reviewer is a finding, not a shortcut.

### Step 3 — Kickoff checklist

- [ ] Ticket pulled read-only and its status is in the allow-list (`Ready for Dev`)
      — Path B: `python3 tools/mock_ticket_mcp.py --fixtures tickets/ --call get_ticket --arg id=REQ-2502`
- [ ] Sandbox reachable: `curl -s -o /dev/null -w '%{http_code}' "$SANDBOX_URL/health"` → `200`
      — Path B: `python3 tools/mock_sandbox_api.py --port 8765 &`
- [ ] Scope in/out pasted into the plan template; timebox 210 minutes acknowledged
- [ ] Hooks active: an intentionally denied command (or MCP transition) appears in
      `runs/hook_log.jsonl` with `decision: deny`
- [ ] Roles recorded in `capstone.yaml` and read aloud once — no "everyone owns it"

---

## Evidence

- `notes/capstone/kickoff-review.md` — six draft defects with consequences and fixes
- `capstone.yaml` committed; `runs/CURRENT_RUN` set
- Parameterisation diff + second reviewer's note + the smoke-test output
- Kickoff checklist completed (ticket status, health 200, hook deny line, roles)

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `get_ticket` returns `NOT_FOUND` | Mock server pointed at the wrong fixtures dir | `--fixtures tickets/` from `<capstone-root>` |
| Sandbox health never returns 200 | Port already in use | `--port 8766` and `export SANDBOX_URL=http://127.0.0.1:8766` |
| Old tests get hashed by `approve.py` | `tests_glob` still hard-coded | Finish Step 2; re-run the smoke test |
| Quality lead also drives the generator | Team too small | Report owner or reviewer takes the sign-off; the generator driver never signs |

## Checkpoint questions

<details>
<summary>Why must the control plane be parameterised before any capstone work?</summary>

The old tools would hash and guard `tests/test_req_2481_*.py` — the new tests would run
**unguarded**. The sign-off would bind the wrong files, the commit guard would ignore the new
suite, and CA-2/CA-7 would be false. Parameterising is also a control-plane edit, so it needs a
second reviewer: the fix must not weaken the controls it enables.
</details>

<details>
<summary>What does "cut scope, not controls" mean when the clock runs out?</summary>

Drop the optional delegated task, test fewer edge cases, shorten the report — but never skip the
plan approval, the independent review, the hash-bound sign-off or the readiness gate. The controls
are what make the deliverable trustworthy; scope is what fits inside the timebox.
</details>

---

*Next: Lab 20.2 — Stage 1: pull REQ-2502 and build the requirement bundle (CP1).*

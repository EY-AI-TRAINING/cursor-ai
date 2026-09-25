# Lab 20.8 — Stage 7: Security, CI Re-verification and Readiness (CP5)

**Xebia — Cursor AI Training | AI-Assisted Software Engineering**
Day 7 · Module 20 · Lab 20.8 of 10 · ~20 min · Team (3–4)

> **Objective:** add the checks that **don't trust the laptop**: secret/dependency/lint scans, a
> review of what the agents tried and were denied, a clean-runner re-verification of gates and
> approvals, and a readiness decision from the **unchanged** versioned policy. Unknown criteria
> fail safe: NOT READY.

**Guide reference:** §7 Stage 7 — Security/Quality Gates, CI and Deployment Readiness
**Learning objectives covered:** 6 (security/quality gates, CI and readiness), 8 (observability as evidence)

## Before you start

| Need | Notes |
|---|---|
| Sign-off recorded (G5) | Lab 20.7 |
| Hook log + gate log | `runs/hook_log.jsonl`, `runs/req-2502-run-01/gate_log.jsonl` |
| Flawed readiness report | [`samples/readiness-report-draft.md`](samples/readiness-report-draft.md) |
| Readiness tooling | Your Module 19 `readiness.yaml` + `tools/readiness.py`, or the kit's reference report |

---

## Steps

### Step 1 — Security and quality gates

| Check | Pass condition | Evidence |
|---|---|---|
| Secrets in diff/package | 0 findings (gitleaks or GitHub secret scanning) | scan output → `security.md` |
| Dependency risk | 0 new high/critical | CI check or local audit |
| Lint generated tests | `ruff check tests/` clean | G3 `lint_clean` |
| Test hygiene | markers present; no skip/xfail without DEF-ID; write scope respected | `gate_log.jsonl` |
| Control plane untouched | no agent edits to `gates.yaml`, `readiness.yaml`, `.cursor/**`, `tools/**` | G3 + CODEOWNERS diff |
| Hook-log review | every deny/revert explained | report §10 |

```bash
# Path B: no jq required
python3 tools/summarise_hooks.py --log runs/hook_log.jsonl
```

- [ ] The three deny/revert events are each explained (injection transition, force-push, control-plane revert)
- [ ] The one `ask` (DEF-5561 creation) shows human approval
- [ ] No unapproved external writes; the injection changed no task and no ticket state

### Step 2 — CI re-verification (or a labelled simulation)

The Module 19 workflow re-runs, on a clean runner: trace-convention checks, gate replay,
`verify_approval.py`, the test suite against the sandbox, and the scans.

- [ ] Path A: open the PR, watch the run go green; attach the run link to the report
- [ ] Path B (no GitHub sandbox): execute the workflow steps locally and write **exactly which
      steps were simulated** in report §11 — a labelled simulation passes CA-8; presenting a local
      run as CI does not
- [ ] Red→green sanity check: a removed `@ac` marker fails the replay; restore and re-run

### Step 3 — Readiness over unchanged policy

- [ ] `readiness.yaml` is **unchanged from Module 19** — a new ticket does not get a new rule book
- [ ] `readiness.py` evaluates policy over: CI/gate replay, hash-bound sign-off, AC coverage,
      defect policy (DEF-5561 Sev-3 strict xfail allowed), security results
- [ ] `readiness_report.md`: **Decision: READY** (staging), with an evidence column per criterion
- [ ] Promotion remains a human environment decision — READY ≠ deployed

### Step 4 — Fail-safe drills, then attack the draft

Find all five planted problems in [`samples/readiness-report-draft.md`](samples/readiness-report-draft.md)
and record them in `notes/capstone/readiness-review.md`. Then run the drills:

| Drill | How | Expected |
|---|---|---|
| **Unknown criterion** | Make one criterion unevaluable (e.g. security evidence missing) | **NOT READY** — `on_unknown: NOT_READY`, the criterion is named |
| **Severity flip** | Change DEF-5561 to Sev-2 | **NOT READY** — "Sev-2 on the changed path" |
| **Unjustified xfail** | Remove `strict=True` (or the DEF-ID) in a scratch copy | G3 `no_unjustified_skips` FAIL; readiness NOT READY |
| **Restore** | Undo the scratch changes | READY again; the two verdicts are in the report trail |

- [ ] CP5: reviewer verdict + sign-off + CI (or labelled sim) + readiness report demonstrated

---

## Evidence

- `reports/REQ-2502/security.md` (scans + hook summary + deny explanations)
- CI run link or the labelled simulation transcript; red→green replay output
- `readiness_report.md` READY + the NOT READY drill outputs
- `notes/capstone/readiness-review.md` — five draft defects

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Readiness says READY with an unknown criterion | Fail-open policy | `on_unknown: NOT_READY`; re-run — the drill exists for a reason |
| Someone edits `readiness.yaml` "for this ticket" | Policy as per-ticket preference | Revert; policy changes go through code-owner review and a version bump |
| CI replay fails on approval hash | Tests changed after sign-off | Re-gate → re-approve → commit; the hash is the control |
| Simulation presented as CI | No sandbox, no label | Label §11 explicitly; candour passes CA-8, hidden simulation fails it |

## Checkpoint questions

<details>
<summary>Why must `readiness.yaml` stay unchanged for the capstone ticket?</summary>

Readiness is organisational policy, not per-ticket preference. If each ticket could edit the rules,
READY would mean whatever its author wanted. Policy changes go through code-owner review and a
version bump — never through a capstone PR. The capstone proves the pipeline runs against a stable
rule book.
</details>

<details>
<summary>What is the difference between a gate PASS on the laptop and CI re-verification?</summary>

The laptop PASS is a claim; the clean-runner replay with the committed `gates.yaml` is evidence.
CI re-runs trace conventions, gate replay, approval verification and the tests without trusting
local state — which is why an approval hash mismatch or a missing marker surfaces there even when
the local run was green.
</details>

---

*Next: Lab 20.9 — Stage 8 (optional): the delegated task.*

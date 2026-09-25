# Lab 20.3 — Stage 2: Explore, Plan, and Record the Human Approval (CP2)

**Xebia — Cursor AI Training | AI-Assisted Software Engineering**
Day 7 · Module 20 · Lab 20.3 of 10 · ~30 min · Team (3–4)

> **Objective:** explore the repository read-only, write an implementation plan a human can
> actually review (per-AC strategy, file list, budgets, risks), and record a **hash-bound plan
> approval before any generation**. This is the cheapest checkpoint in the workflow — a wrong
> plan caught here costs five minutes; the same mistake caught at sign-off costs the run.

**Guide reference:** §2 Stage 2 — Explore the Repository, Draft the Plan, Get Approval
**Learning objectives covered:** 2 (read-only exploration; plan approved before tests or code are generated)

## Before you start

| Need | Notes |
|---|---|
| Bundle valid (CP1) | Lab 20.2 complete |
| Flawed plan | [`samples/plan-draft.md`](samples/plan-draft.md) |
| Approver available | `human:<tech-lead>` at an interactive terminal |
| Approval tool | Your Module 18 `tools/approve.py`, extended with `--checkpoint plan` (Lab 20.1) |

---

## Steps

### Step 1 — Explore read-only (no writes except the exploration note)

- [ ] Contract: `CancelRequest`, `AuditEntry`, error codes — all present and consistent with the bundle
- [ ] Existing assets: `tests/conftest.py` fixtures; the missing `support_user`; nothing to reuse that conflicts
- [ ] Risks: DEF-5520 sibling behaviour (404 vs 403); in-memory sandbox state; the 280/281 boundary
- [ ] Write `plans/REQ-2502/exploration.md` — the explorer's write scope is enforced by the hook,
      not by a prompt; everything else is read-only

### Step 2 — Draft the plan, then attack the draft (10 min)

Find all six planted problems in [`samples/plan-draft.md`](samples/plan-draft.md) and record
*defect → consequence → fix* in `notes/capstone/plan-review.md`. Then write your plan with:

| Section | Must contain |
|---|---|
| Scope | In / out explicit — no production code, no contract edits, no REQ-2481 test edits |
| Test strategy per AC | Positive + negative/boundary, data, fixtures |
| Files created/changed | Exact list (a new fixture in `conftest.py` is a reviewed change) |
| Gates & loops | `gates.yaml` version, max rounds, token/time budget |
| Risks & mitigations | DEF-5520 sibling; prose AC-4 confirmed; boundary may expose a product defect |
| Approval requested | Named approver; conditions welcome |

- [ ] No sentence in the plan says "fix the tests" or "adjust the contract to match the API"
- [ ] The plan lists **only** files the team may change; generation is scoped by this list

### Step 3 — Record the approval (hash-bound, human-only)

```bash
python3 tools/approve.py --checkpoint plan --decision APPROVE \
  --reason "Strategy covers boundaries; conftest change limited to one fixture" \
  --condition "Do not modify REQ-2481 tests"
```

- [ ] TTY required — a non-interactive run (agent) is refused and the attempt is logged
- [ ] `plans/REQ-2502/plan_approval.json` records: `decided_by: human:<name>`, reason,
      conditions, and `approved_hashes` for `plan.md` + the bundle
- [ ] Approval timestamp is **before** the first `test-generator` entry in `run_log.jsonl`

### Step 4 — Prove the binding (the five-minute habit that saves the run)

| Drill | How | Expected |
|---|---|---|
| **Tamper after approval** | In a scratch copy, change one line of `plan.md`, re-run `package_check.py` | CA-2 FAIL: `hash_fresh=False` |
| **Regenerate** | Restore the plan; re-approve if the change was real | CA-2 PASS again |
| **Generation gate** | Try to start generation with no `plan_approval.json` | Stage refuses; no tests produced |

- [ ] Record the tamper transcript in `notes/capstone/plan-review.md`
- [ ] CP2: plan + approval + matching hash demonstrated to the facilitator

---

## Evidence

- `plans/REQ-2502/exploration.md`, `plan.md`, `plan_approval.json`
- `notes/capstone/plan-review.md` — six draft defects + the tamper drill transcript
- `package_check.py` output: CA-2 FAIL on tamper → PASS after restore

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `approve.py` refuses | No interactive TTY (ran from an agent/script) | The refusal is correct; a human runs it in a terminal |
| CA-2 `before_generation=False` | Generation started before approval | Stop; the run is invalid for CA-2 — re-run generation after approval and record why |
| Plan lists `specs/openapi.yaml` as editable | Contract treated as mutable | Remove it; the contract is a source of truth. Fix the plan, not the contract |
| Explorer writes test files | Write scope not enforced by a hook | Enforce via hook; the prompt is not a control |

## Checkpoint questions

<details>
<summary>Why is the plan approval not "extra process" on top of the sign-off?</summary>

They guard different mistakes. The plan approval catches **wrong intent** (wrong endpoint, missed
boundary, wrong scope) before any tokens are spent. The sign-off catches **wrong output** (tests
that don't prove the AC). A mistake caught at planning costs minutes; at sign-off it costs the run.
</details>

<details>
<summary>What exactly does the approval hash bind, and why does that matter later?</summary>

It binds `plan.md` and the bundle. If either changes after approval, the approval is stale — the
rerun planner marks downstream stages stale, the commit guard refuses the tests, and CA-2 fails.
The hash is what turns "we approved a plan" into "we approved **this** plan".
</details>

---

*Next: Lab 20.4 — Stage 3: the spec note whose AC set equals the bundle's (CP3).*

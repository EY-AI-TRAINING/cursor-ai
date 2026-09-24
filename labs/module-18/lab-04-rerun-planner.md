# Lab 18.4 — Rerun Only What Changed: Stale-by-Input-Hash

**Xebia — Cursor AI Training | AI-Assisted Software Engineering**
Day 6 · Module 18 · Lab 18.4 of 8 · ~10 min · Build (individual)

> **Objective:** replace "rerun from the failing stage to the end" with the rule build systems use —
> a stage is stale **iff the hash of its inputs differs from the hash it last ran with** — evaluated
> one stage at a time so cascades stop early. The planner is also where hidden dependencies (the
> Reviewer reads the original requirement) surface.

**Guide reference:** §3 Configure Downstream Reruns — Only Affected Stages Re-execute
**Learning objectives covered:** 3 (downstream reruns — only stages whose inputs changed)

## Before you start

| Need | Notes |
|---|---|
| `PIPELINE.md` v2 with the stage table | Lab 18.1; the planner's `READS` table is a **mirror** of its Reads column — keep them in sync |
| Run state with recorded input hashes | `state.json`; hashes get written after each stage run |
| Flawed draft | [`samples/rerun-plan-draft.py`](samples/rerun-plan-draft.py) |

---

## Steps

### Step 1 — Critique the position-based draft (≥5 defects)

Record *defect → consequence → fix* in `notes/module18/rerun-review.md`. Compare against the guide's
§3 `rerun_plan.py` listing — the differences are the lesson.

| Ask yourself | Why it matters |
|---|---|
| What does the draft do when the Sequence Builder is retried but writes a byte-identical `02_test_sequence.json`? | The cascade should stop; the draft may still rerun stages 3–5 |
| Which stage reads the **original** requirement? Is that dependency in the draft's `READS`? | A mid-run requirement edit makes stages 1 **and** 5 stale — a position-based rule never sees it |
| Does the draft compare content hashes or file timestamps? | A `touch` must not rerun anything; a byte change must |
| Is staleness evaluated once per fix, or after every stage? | Lazy evaluation is what lets a cascade stop early |
| Which stage's inputs include `tests/conftest.py`? | The fixture contract changes what tests mean |
| Does the draft consult each stage's `status` as well as its hash? | A stage that never ran is stale by definition |

### Step 2 — Build `tools/rerun_plan.py`

- [ ] Mirror the Reads column exactly:

| Stage | Reads (guide §3) |
|---|---|
| `requirement-validator` | `requirements/{req}.md`, `specs/openapi.yaml` |
| `sequence-builder` | `runs/{run}/01_validated_requirement.md`, `specs/openapi.yaml` |
| `test-generator` | `runs/{run}/02_test_sequence.json`, `specs/openapi.yaml`, `tests/conftest.py` |
| `api-validator` | `tests/test_{req_l}_*.py`, `specs/openapi.yaml` |
| `reviewer` | `requirements/{req}.md`, `tests/test_{req_l}_*.py`, `runs/{run}/04_api_validation_report.md` |

- [ ] Implement `stale_stages(state, …)`: a stage is stale when its **status ≠ PASS** or its current
      input hash ≠ the recorded `input_hash`. Return them in pipeline order; the orchestrator asks for
      the **first** stale stage, runs it, records new input/output hashes, and asks again.
- [ ] Log a `RERUN_PLAN` entry every time the plan changes: `trigger`, `reused` (stage → hash),
      `rerun` (ordered list). Auditors ask why stage 1 was *not* re-validated — the entry answers.

### Step 3 — Prove the three cases

Using the offline kit (or your run), record the planner's output for each:

| Case | You change | Expected |
|---|---|---|
| **Tests patched** | Round-0 tests → `tests_round1.py` | Rerun `[test-generator, api-validator, reviewer]`; stages 1–2 reused with their hashes |
| **Cascade stops** | Retry `sequence-builder` but restore the byte-identical `02_test_sequence.json` | **Nothing** reruns downstream — 02's hash is unchanged |
| **Hidden dependency** | Edit `requirements/REQ-2481.md` mid-run | Stages `requirement-validator` **and** `reviewer` are stale — even though no stage failed |

- [ ] Case 2's `RERUN_PLAN` entry shows `rerun: []` (or no entry) while the loop controller separately
      escalates the identical artifact — the two components agreeing without knowing about each other.
- [ ] Case 3: explain in one sentence why a position-based rule misses this, and what it would cost.

---

## Evidence

- `tools/rerun_plan.py` with the mirrored `READS` and lazy `stale_stages`
- Three-case output (commands + observed rerun lists)
- `RERUN_PLAN` entries in `gate_log.jsonl`
- `notes/module18/rerun-review.md` — the draft's ≥5 defects

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Everything reruns every time | Hashes never recorded after stages run | Record `input_hash`/`output_hash` when a stage completes — the planner has nothing to compare otherwise |
| Nothing ever reruns | Hash includes a path that does not exist (empty set) | Handle missing files explicitly; an unreadable input is NEEDS_HUMAN, not "unchanged" |
| Reviewer never reruns after a requirement edit | `READS` out of sync with `PIPELINE.md` | Diff the two tables — the planner's table must mirror the stage contract |
| `{req_l}` not expanded | Expansion helper missing `lower().replace("-", "_")` | Expand all three placeholders: `{req}`, `{req_l}`, `{run}` |

## Checkpoint questions

<details>
<summary>Why does "stale by input hash" stop cascades that "rerun from the failing stage" cannot?</summary>

A retried stage can produce the same output. The hash rule notices that nothing downstream's inputs
actually changed, so nothing re-executes; a position-based rule reruns stages 3–5 regardless, paying
for work whose inputs are byte-identical.
</details>

<details>
<summary>Why must staleness be re-evaluated after every stage instead of once per fix?</summary>

A stage's output becomes the input of later stages. After stage 3 runs, its output hash may change
stage 4's staleness. Evaluating lazily lets the cascade stop the moment outputs stop changing — and
surfaces exactly which stage's change caused the cascade to continue.
</details>

<details>
<summary>Why is the RERUN_PLAN entry part of the evidence, not just debug output?</summary>

It is the answer to "why wasn't stage 1 re-validated?" — reused stages with their hashes, rerun stages
in order, and the trigger. Without it, a reviewer can see verdicts but not the decisions between them.
</details>

---

*Next: Lab 18.5 — Hooks for Early Feedback, where engineering checks move to the moment of the edit and tampering is reverted and flagged before the gate ever runs.*

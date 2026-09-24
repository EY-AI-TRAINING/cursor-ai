# Lab 18.3 — Close the Correction Loop: Findings, Owner Retry, Bounds

**Xebia — Cursor AI Training | AI-Assisted Software Engineering**
Day 6 · Module 18 · Lab 18.3 of 8 · ~20 min · Build (individual)

> **Objective:** make a FAIL actionable and safe. A findings builder turns failed checks into a
> schema-valid file that names the owner, the artifact to **patch**, and what not to touch; a loop
> controller decides RETRY or ESCALATE from four independent bounds; the owning agent receives only
> the findings file and the artifact — never the transcript.

**Guide reference:** §2 Implement the Correction Loop — FAIL → Structured Feedback → Owner Retry
**Learning objectives covered:** 2 (correction loop with structured feedback, bounded by rounds/progress/drift/budget)

## Before you start

| Need | Notes |
|---|---|
| A working gate engine that emits findings | Lab 18.2 |
| Flawed drafts | [`samples/findings-round-1-draft.json`](samples/findings-round-1-draft.json) · [`samples/loop-control-draft.py`](samples/loop-control-draft.py) |
| Reference | Guide §2 — `decide()` decision core and the findings schema table |
| Run state | `state.json` from Lab 18.1 (counters, budget, history) |

---

## Steps

### Step 1 — Findings: schema, critique, real file (≥5 defects)

Critique [`samples/findings-round-1-draft.json`](samples/findings-round-1-draft.json) against the
required fields. Record *defect → consequence → fix* in `notes/module18/loop-review.md`.

| Field | Purpose |
|---|---|
| `gate`, `round`, `max_rounds`, `counter` | Tells the agent how much budget is left; appears in the log |
| `route_to` | Owning stage, **validated against the gate's `on_fail`** |
| `artifact_to_modify` | The file to **patch** — "regenerate everything" is itself a finding |
| `findings[]` | `id`, `test`, `ac_id`, `criterion`, `observed`, `expected` (**with spec citation**), `class` |
| `do_not_change` | Passing tests, markers, fixtures that must survive the patch |
| `previous_attempt_summaries` | One line per earlier round, so the agent does not retry a failed fix |

- [ ] Write `schemas/findings.schema.json` encoding these fields (required vs optional, `class` enum,
      `route_to` enum).
- [ ] Produce a real `runs/req-2481-run-02/findings/round-1.json` for the missing-marker failure: owner
      `test-generator`, artifact the test file, evidence from the gate log, and `do_not_change` naming
      the passing tests and all existing markers.

### Step 2 — Loop controller: critique the draft (≥5 defects), then build it

The draft is missing most of Module 17 §5's bounds. Before writing code, list which bounds it lacks
and what each missing bound lets through.

- [ ] Build `tools/loop_control.py` with the decision core. **Checked in order; the first stop reason wins:**

| Order | Check | ESCALATE when |
|---|---|---|
| 1 | Run-level round budget | `counters.run_total >= max_total_rounds` |
| 2 | Token / wall-clock budget | `budget_used` exceeds `max_tokens` or `max_minutes` |
| 3 | Owner counter | `used >= limit` for the shared counter |
| 4 | Hash novelty | Artifact hash identical to **any** earlier round on this owner (no change or oscillation) |
| 5 | Progress | Findings did not decrease vs. the previous round **on the same gate** |
| 6 | Invariant (goal drift) | Assertion count dropped vs. the previous round |
| — | Otherwise | `RETRY` — and only then |

- [ ] On RETRY: increment `counters[name]` **and** `counters.run_total`, append to `history`, write the
      findings file, and log a `LOOP` entry. On ESCALATE: set `status = ESCALATED`, write the `HALT`
      marker, trigger the decision packet (Lab 18.6).
- [ ] Run the draft's `decide()` against a history where the artifact hash repeats: confirm the draft
      says RETRY and yours says ESCALATE with a reason an auditor can read.

### Step 3 — Owner intake: teach the generator to receive findings

Add a **Correction mode** section to `.cursor/agents/test-generator.md` (guide §2):

- [ ] Read **only** the findings file, the `artifact_to_modify`, and the stage's declared inputs.
- [ ] Make the smallest edit that resolves each finding; do not reformat, rename, or reorder unrelated tests.
- [ ] Never delete an assertion, add `skip`/`xfail`, or loosen an expected value to make a finding
      disappear; if that seems necessary, set `status: NEEDS_HUMAN` and explain in `open_issues`.
- [ ] In the envelope: `attempt += 1`, and list each finding id as `resolved` or
      `not_resolved: <reason>`.

### Step 4 — Prove RETRY and ESCALATE

Use the [offline kit](samples/offline-kit/README.md) (or your agent run) for both histories:

| History | Sequence | Expected |
|---|---|---|
| **Converging** | round-0 tests (missing marker) → gate G3 FAIL → loop control → apply `tests_round1.py` → gate G3 | RETRY 1/2 with `findings/round-1.json`, then PASS; counter `generator = 1` |
| **No progress** | After the first FAIL and RETRY, re-apply the **same** round-0 file → gate G3 → loop control | ESCALATE: "artifact identical to an earlier round" — even though the counter has room |

- [ ] The `LOOP` entries in `gate_log.jsonl` show the counter, the reason, and the findings reference.
- [ ] ESCALATE leaves `HALT` in the run folder and `state.status = ESCALATED`; nothing downstream runs.

---

## Evidence

- `schemas/findings.schema.json`
- `runs/req-2481-run-02/findings/round-1.json` (schema-valid, owner = `test-generator`)
- `tools/loop_control.py` with the six checks in order + RETRY/ESCALATE side effects
- `LOOP` entries for the converging and no-progress histories
- Correction-mode section in `.cursor/agents/test-generator.md`
- `notes/module18/loop-review.md` — both defect tables (≥5 + ≥5)

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Loop retries forever | Counter never increments, or progress check compares across gates | Increment on RETRY; compare findings per gate (the G4 round should not be compared to a G3 round) |
| First G4 failure escalates immediately | Progress check compares to no previous round and treats missing as zero | No previous round on that gate → progress check passes; rely on counter and budget |
| Findings file accepted with `route_to: reviewer` | `route_to` not validated against the gate's `on_fail` | Validate and reject mismatches → NEEDS_HUMAN |
| Agent rewrote the whole file and new findings appeared | Intake prompt missing, or `do_not_change` absent | Restore the prompt clauses; include `do_not_change`; require the finding count to decrease |
| ESCALATE but no packet | Side effects missing | ESCALATE must write `HALT`, update state, and trigger `decision_packet.py` |

## Checkpoint questions

<details>
<summary>Why does the retry receive only the findings file and the artifact, not the transcript?</summary>

Transcripts make rounds slower and costlier and invite the agent to repeat old reasoning. A findings
file is focused, schema-valid feedback with evidence and a named owner — the smallest context that can
produce the smallest fix.
</details>

<details>
<summary>A retried stage produced a byte-identical artifact. What do the planner and the controller each do?</summary>

The rerun planner sees the output hash unchanged and marks nothing downstream stale — no reruns. The
loop controller sees the artifact hash identical to an earlier round — no progress — and escalates.
The two deterministic parts agree without knowing about each other.
</details>

<details>
<summary>Why is "findings did not decrease" a stop reason, not just a warning?</summary>

If a round cannot reduce the number of findings, further rounds are unlikely to converge — they mostly
burn budget and time. Escalating early keeps the human's attention on a run that is actually stuck
rather than one that is merely slow.
</details>

---

*Next: Lab 18.4 — Rerun Only What Changed, where the planner re-executes exactly the stages whose inputs changed and nothing else.*

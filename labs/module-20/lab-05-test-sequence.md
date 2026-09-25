# Lab 20.5 — Stage 4: The Engineering Test Sequence (G1/G2)

**Xebia — Cursor AI Training | AI-Assisted Software Engineering**
Day 7 · Module 20 · Lab 20.5 of 10 · ~20 min · Team (3–4)

> **Objective:** build the sequence that sits between the agreed criteria and the tests: one
> scenario per behaviour, every scenario mapped to AC-IDs, error criteria covered by negative or
> boundary scenarios, and the approved plan's promised boundaries actually present. G1 and G2
> decide whether generation may start.

**Guide reference:** §4 Stage 4 — Generate the Engineering Test Sequence
**Learning objectives covered:** 4 (run the requirement-to-test pipeline on the new ticket)

## Before you start

| Need | Notes |
|---|---|
| Spec note frozen (CP3) | Lab 20.4; the sequence's inputs are the bundle **and** the spec note and plan |
| Flawed sequence | [`samples/test-sequence-draft.json`](samples/test-sequence-draft.json) |
| Gate tool | Your Module 18 `gate_engine.py`, or the kit's reference `tools/sequence_gate.py` |

---

## Steps

### Step 1 — Attack the draft (5 min)

Find all six planted problems in [`samples/test-sequence-draft.json`](samples/test-sequence-draft.json)
and record *defect → consequence → fix* in `notes/capstone/sequence-review.md`. Watch for the
scenario that tests an AC nobody confirmed, and the error criterion with no negative coverage.

### Step 2 — Build the sequence

Produce `runs/req-2502-run-01/02_test_sequence.json` from the bundle + spec note + approved plan:

| Scenario | AC | Type | What it proves |
|---|---|---|---|
| SEQ-1 | AC-1 | positive | each valid reason round-trips via GET |
| SEQ-2 | AC-1 | positive | no reason still cancels; reason null |
| SEQ-3 | AC-2 | negative | unknown reason → 422 `INVALID_REASON`; status unchanged |
| SEQ-4 | AC-3 | boundary | OTHER with note length 0/1/280 |
| SEQ-5 | AC-3 | boundary | OTHER with note length 281 → 422 |
| SEQ-6 | AC-4 | positive | owner and support see the entry; newest first |
| SEQ-7 | AC-4 | negative | other customer → 403 |

- [ ] Every scenario has `id`, `ac_ids`, `title`, `type`
- [ ] Every AC has ≥1 scenario; every error AC (AC-2, AC-3) has negative **and** boundary coverage
- [ ] The boundaries from the plan (`0/1/280/281`) are all present — the plan promised them
- [ ] `open_issues` is empty, or lists only genuinely parked items — never a confirmed AC

### Step 3 — Run G1 and G2

```bash
# Path B reference:
python3 tools/sequence_gate.py --run req-2502-run-01
# Own pipeline:
python3 tools/gate_engine.py --run req-2502-run-01 --gate G1_requirement_ready
python3 tools/gate_engine.py --run req-2502-run-01 --gate G2_sequence_coverage
```

- [ ] G1 PASS: all ACs present; no llm-extracted AC left unconfirmed
- [ ] G2 PASS: unique ids; every scenario mapped; every AC covered; error criteria covered
- [ ] Run the gate on the draft first: it fails with specific findings (record the output)

### Step 4 — Freeze the sequence

- [ ] The sequence records its sources (`bundle_sha`, `spec_note`, `plan_sha`)
- [ ] Sequence budget respected: **max 1** sequence round; if it fails, fix and re-run — then
      escalate rather than loop
- [ ] Gate entries appended to `gate_log.jsonl` (`G1`, `G2` round 0)

---

## Evidence

- `notes/capstone/sequence-review.md` — six draft defects with consequences
- `02_test_sequence.json` — 7 scenarios, all mapped
- G1/G2 output: FAIL on the draft → PASS on the real sequence
- `gate_log.jsonl` G1/G2 entries

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| G2 "ACs without scenarios" | A criterion skipped | Add the scenario; never let generation guess coverage |
| G2 "error criterion with no negative/boundary scenario" | Happy-path bias | Add the negative or boundary scenario for AC-2/AC-3 |
| A scenario has no `ac_ids` | Mapping lost | Add the ids; an unmapped scenario is untraceable |
| Sequence tests an unconfirmed AC | AC-4 confirmed late or never | Confirm first (G1), then map; a confirmed AC belongs in the sequence |

## Checkpoint questions

<details>
<summary>What is the sequence's job that neither the spec note nor the tests do?</summary>

The spec note defines correctness; the tests implement it. The sequence is the **reviewable
middle**: a short, readable list of scenarios a human can check for coverage and boundaries before
anyone writes code. G2 can verify coverage mechanically because the sequence declares its
mappings — which is why every scenario carries `ac_ids`.
</details>

<details>
<summary>Why does the sequence read the plan and the spec note, not just the bundle?</summary>

The bundle says *what* must be true; the plan promised *how* it will be tested (which boundaries,
which fixtures); the spec note fixes the exact expectations. Feeding only the bundle is how you get
tests that miss the boundary the plan promised, or that duplicate fixtures the exploration found.
</details>

---

*Next: Lab 20.6 — Stage 5: generate, execute, and let the correction loop run (CP4).*

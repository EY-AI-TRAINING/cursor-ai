# Lab 17.2 — Route the Failure, Rerun Only What Changed, Bound the Loop

**Module 17 · Quality Gates, Hooks & Self-Correction Fundamentals | Xebia — Cursor AI Training**
Day 5 · Lab 2 of 3 · ~5 minutes · Individual or pairs

> **Objective:** apply the three correction-loop questions to six real failures — **who retries, what
> feedback is reused, and what reruns downstream** — then bound two correction histories where the round
> counter alone would make the wrong call. The dependency map comes from your Module 16 `PIPELINE.md`
> "Reads" column, so reruns touch only what changed.

**Guide references:** Module 17, §2 (correction-loop patterns, downstream reruns, structured findings), §5 (bounded retries), §7 walkthrough tasks 2 and 5
**Learning objectives covered:** 2 — who retries, what feedback is reused, what reruns; 5 — bounded retries and the signals of an unproductive loop.

---

## Before you start

- Lab 17.1 complete: `gates.yaml` written
- Open [`samples/failure-scenarios.md`](samples/failure-scenarios.md) (read-only) and `<pipeline-root>/PIPELINE.md`
- Add the routing and bounds sections to `notes/module17/gate-design.md`

---

## Step 1 — Route all six failures to their owner

| # | Root cause (artifact / upstream / input / environment) | Route to | Feedback they receive | Stages that rerun |
|---|---|---|---|---|
| S1 | | | | |
| S2 | | | | |
| S3 | | | | |
| S4 | | | | |
| S5 | | | | |
| S6 | | | | |

- [ ] Every row names the **stage that owns the defect**, not "the last agent" or the whole pipeline
- [ ] S2 does **not** route to the generator — say what happens to the test and who decides
- [ ] S3 first retries infrastructure once, then escalates; no artifact is blamed
- [ ] S4 routes to a human, not a producer, and says where the pipeline resumes after the answer
- [ ] S5 identifies the **upstream** owner and reruns from that stage, not from the gate
- [ ] Rerun columns list stage numbers only (e.g., `3 → 4 → 5`), never "everything"

---

## Step 2 — Draw the rerun map from the dependency column

Using `PIPELINE.md`'s Reads column, state what each change forces:

| What changed | Reruns | Kept (reused artifacts) |
|---|---|---|
| Only `tests/` (stage 3 output) | | |
| `02_test_sequence.json` (stage 2 output) | | |
| `01_validated_requirement.md` (stage 1 output) | | |

- [ ] All three rows filled from the actual Reads column
- [ ] One sentence: how an `input_ref: …#sha` hash on each envelope turns "what changed" into a mechanical decision
- [ ] One sentence: what re-running everything "to be safe" costs besides tokens (and why that risk matters more)

---

## Step 3 — Write the structured findings card

For **S1**, write the routing payload in `gate-design.md` (field set from §2):

```jsonc
{
  "gate": "G3_tests_collect_and_conform",
  "round": 1, "max_rounds": 2,
  "route_to": "<owner stage>",
  "artifact_to_modify": "<file>",
  "findings": [
    { "id": "F-1", "test": "…", "ac_id": "…", "criterion": "…", "observed": "…", "expected": "…", "class": "…" }
  ],
  "do_not_change": ["…", "…"],
  "previous_attempt_summaries": ["…"]
}
```

- [ ] `artifact_to_modify` names the existing file — the producer **patches** it, it does not regenerate
- [ ] The finding names the criterion and shows observed vs. expected (with the spec citation where relevant)
- [ ] `do_not_change` and `previous_attempt_summaries` are both present — one sentence each on the regression loop they prevent

---

## Step 4 — Bound both histories

For each run in the fixture, state the round the loop should stop at, the guard that fires, and why the remaining round budget is irrelevant:

| Run | Stop at | Guard that fires | Why |
|---|---|---|---|
| A | | | |
| B | | | |

- [ ] Run A and Run B stopped for **different** reasons — name both precisely
- [ ] One row per failure mode with its guard (use §5's table):

| Loop failure mode | Signal you would see | Guard you configure |
|---|---|---|
| Runaway | | |
| Oscillation | | |
| No progress | | |
| Goal drift | | |
| Budget blow-out | | |
| Gate gaming | | |

- [ ] One sentence: why "the gate would say PASS" is not enough to continue in Run B's situation

---

## Evidence

- `notes/module17/gate-design.md` — six-row routing table, rerun map, structured findings card, two bound verdicts + guard table

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Everything routes to the Test Generator | The gate names where it failed, not why | Classify the root cause first; the failing artifact may have been produced upstream |
| "Rerun all five stages" | Dependency map ignored | Read the PIPELINE.md Reads column: unchanged inputs mean reused artifacts |
| Findings say "fix the test" | No observed/expected | A finding needs test + criterion + observed vs. expected; otherwise the retry is a re-roll |
| Product defect sent back to the generator | Class ignored | The test matches the spec; the API is wrong. No retry — flag it and escalate |
| Loop runs to `max_rounds` automatically | Counter treated as a target, not a ceiling | Progress check: identical hash or non-decreasing findings escalates early |
| Run B continues because the gate passed | Only the gate verdict checked | Invariants (assertion count, no new `skip`/`xfail` without defect ID) catch goal drift |

---

## Checkpoint questions

1. The API Validator finds a test asserting a field that is not in the spec. Who retries, what feedback do they get, and which stages rerun?
2. A loop has rounds left but produces the same artifact hash twice. What happens, and why?
3. Why does "patch, don't regenerate" matter in a correction loop?

<details>
<summary>Answers</summary>

1. The **Test Generator** retries with structured findings (test, AC-ID, criterion, observed vs. expected, spec citation) and the existing test file to patch. Stages 3 → 4 → 5 rerun; stages 1–2 are reused unchanged.
2. **Escalate immediately.** An identical hash means no progress; further rounds would burn budget and risk oscillation. The progress check overrides the remaining round count.
3. Regenerating can silently change parts that already passed — breaking working tests and invalidating prior review. Patching the named file, with a `do_not_change` list, preserves proven work and keeps the diff reviewable.

</details>

---

## Next

**Lab 17.3 — Wire the Hooks, Place the Checkpoints, Prove Fail-Safe.** Routing and bounds are designed; now enforce them deterministically — hooks that cannot be forgotten, two human checkpoints that matter, and a broken gate that halts instead of passing.

# Lab 16.2 — Build the Requirement Validator: Fail Cheaply on the Vague AC

**Module 16 · Use Case Lab 3: Multi-Agent Requirement-to-Test Automation | Xebia — Cursor AI Training**
Day 5 · Lab 2 of 8 · ~20 minutes · Individual or pairs

> **Objective:** build the pipeline's cheapest failure point. The Requirement Validator checks REQ-2481
> for completeness, testability, consistency, and traceability — and returns **NEEDS_HUMAN** for the
> deliberately vague AC-4 instead of guessing. Then you act as the requirement owner, answer the
> clarification, and re-run to **PASS**. Two attempts, both logged.

**Guide references:** Module 16, §1 (Requirement Validator — completeness and testability)
**Learning objectives covered:** 1 — configure a Validator that checks completeness and testability; 6 — traceability starts with stable AC-IDs.

---

## Before you start

- Lab 16.1 complete: `PIPELINE.md`, handoff rule, run folder, sandbox smoke-checked
- Open [`samples/REQ-2481.md`](samples/REQ-2481.md) — note that **AC-4 is deliberately vague** and must survive to the Validator untouched
- Write your definition in `<pipeline-root>/.cursor/agents/requirement-validator.md`
- Run each stage in a **fresh chat**: pass the two input files, nothing else

---

## Step 1 — Write the agent definition

Five slots, from Module 10's anatomy. Role, inputs, tools, guardrails, output:

- [ ] **Role** — one sentence: decides whether a requirement is ready for test design; does not design tests
- [ ] **Inputs** — `requirements/REQ-2481.md` and `specs/openapi.yaml`, named with paths
- [ ] **Tools** — read-only; the only write is `runs/<run_id>/01_validated_requirement.md`
- [ ] **Guardrails ("must NOT")**, at least:
  - must not invent, rewrite, or "fix" acceptance criteria — propose a clarification question instead
  - must not design test steps (that is the Sequence Builder's job)
  - status logic: `FAIL` if any AC is UNTESTABLE; `NEEDS_HUMAN` if any is NEEDS_CLARIFICATION; otherwise `PASS`
- [ ] **Output** — `01_validated_requirement.md`: the AC table + clarification questions + handoff envelope (per the rule)

---

## Step 2 — Run attempt 1: catch AC-4

Run the Validator in a fresh chat on the two inputs.

| AC-ID | Expected classification | Your run's result | Evidence cited |
|---|---|---|---|
| AC-1 | TESTABLE | | |
| AC-2 | TESTABLE | | |
| AC-3 | TESTABLE | | |
| AC-4 | NEEDS_CLARIFICATION | | |

- [ ] AC-4 is classified **NEEDS_CLARIFICATION** with a reason (refund is not observable through the API as written) and a concrete question for the owner
- [ ] The aggregated status is **NEEDS_HUMAN** (not PASS, not FAIL) — the pipeline stops here
- [ ] No AC was reworded, renumbered, or invented; every TESTABLE row cites `openapi.yaml#<path>`
- [ ] The output ends with a handoff envelope (`status: NEEDS_HUMAN`, `ac_ids_covered: AC-1..AC-4`)
- [ ] Attempt 1 appended to `run_log.jsonl`

> If your Validator guessed a refund mechanism and returned PASS: that is the exact failure this stage
> exists to prevent. Tighten the guardrail, start a fresh chat, and re-run.

---

## Step 3 — Answer as the requirement owner

You are now the requirement owner (in a real run, this is the ticket author).

- [ ] Answer the Validator's question concretely, e.g.: *"Yes — a refund record with status PENDING appears immediately after cancellation and is queryable via `GET /refunds?order_id={id}`; the test may assert the record's status and amount."*
- [ ] Record the answer in `requirements/REQ-2481.md` as a `## Clarifications` section (Q1 + answer); note the requirement was amended by its owner — not by an agent
- [ ] Confirm the ACs still carry stable IDs (`AC-1`..`AC-4`); no renumbering

---

## Step 4 — Run attempt 2: PASS

Re-run the Validator in a fresh chat with the amended requirement.

- [ ] AC-4 is now **TESTABLE** with the clarification as evidence, and the overall status is **PASS**
- [ ] The output artifact still lists all four ACs and carries the envelope with `status: PASS`
- [ ] Attempt 2 appended to `run_log.jsonl` — both attempts are visible, not just the final one

---

## Evidence

- `.cursor/agents/requirement-validator.md` — five slots, status logic, must-nots
- `runs/req-2481-run-01/01_validated_requirement.md` — attempt 1 (`NEEDS_HUMAN`) and attempt 2 (`PASS`)
- `requirements/REQ-2481.md` — `## Clarifications` section with Q1 and the owner's answer
- `run_log.jsonl` — two validator lines: `NEEDS_HUMAN`, then `PASS`

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Status is PASS on attempt 1 | Validator filled the gap itself | Harden the "must not invent/rewrite" guardrail; the correct first output is NEEDS_HUMAN |
| AC-4 marked UNTESTABLE → FAIL | "Not observable" treated as fatal | Untestable-as-written + answerable question = NEEDS_CLARIFICATION; reserve FAIL for ACs that cannot be tested even after clarification |
| AC rewritten so it is "clearer" | Agent being helpful | Report and question only; the owner amends the requirement, and the AC-ID stays stable |
| Attempt 2 repeats the question | Amended requirement not passed, or stale artifact | Fresh chat; pass the amended `requirements/REQ-2481.md` explicitly |
| Only the final attempt in the log | Outcomes collapsed | One line per attempt — the retry history is what Module 18 automates |
| Envelope missing fields | Rule not loaded | Check `.cursor/rules/pipeline-handoff.mdc` globs and that `<pipeline-root>` is the open workspace |

---

## Checkpoint questions

1. Why should the Validator return NEEDS_HUMAN for AC-4 instead of assuming how a refund is observed?
2. Why is the Validator the cheapest place for the pipeline to fail?
3. Why does the owner amend the requirement instead of the Validator?

<details>
<summary>Answers</summary>

1. Filling the gap would be **inventing a requirement** — the tests would check the agent's guess, not the owner's intent. Surfacing the ambiguity is the Validator's job, and it costs a question instead of a full generation cycle.
2. It runs first on prose only: no tests are generated, no API calls made, no downstream tokens spent. A gap caught here stops the whole chain; the same gap caught by the Reviewer costs the whole pipeline.
3. The requirement is the source of truth and the owner is accountable for it. An agent editing acceptance criteria silently breaks traceability and the Reviewer's independent judgement (it would judge against the agent's edit, not the owner's intent).

</details>

---

## Next

**Lab 16.3 — Build the Sequence Builder: Coverage Before Code.** Stage 1 output exists and passes. Now the Builder turns validated ACs into an ordered, implementation-free test sequence — and you run the first chained handoff with files only.

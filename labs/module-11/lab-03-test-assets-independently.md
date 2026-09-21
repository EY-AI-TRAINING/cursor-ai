# Lab 11.3 — Test Each Asset Independently Against Sample Inputs

**Module 11 · Use Case Lab 1: Reusable Agents, Prompts & Skills Framework | Xebia — Cursor AI Training**
Day 3 · Lab 3 of 4 · ~20 minutes · Individual

> **Objective:** prove every asset behaves as defined — before anything is trusted or chained. Run each of the
> four agents, the subagent, and one template against the shipped sample inputs, check the output against the
> declared contract, catch the deliberate mismatch in the sample test suite, and log PASS/FAIL evidence.
> A well-written definition is not evidence; a run is.

**Guide references:** Module 11, §5 (testing each asset independently); Module 8 §7 (the "testable" quality bar)
**Learning objectives covered:** 5 — test each asset independently against sample inputs.

---

## Before you start

- Lab 11.2 complete: `shared-agent-library/` with agents, templates, subagent, and `AGENTS.md`
- Create `shared-agent-library/testing/pass-fail-matrix.md`
- Sample inputs ship in [`samples/`](samples/) — **read-only**:

| Sample | Used by |
|---|---|
| [`raw-requirement-add-rate-limiting.md`](samples/raw-requirement-add-rate-limiting.md) | Requirement Analysis agent |
| [`analyzed-requirement-rate-limit.md`](samples/analyzed-requirement-rate-limit.md) | Test Generation agent · Documentation agent |
| [`rate-limit-contract.md`](samples/rate-limit-contract.md) | Validation agent |
| [`generated-tests-rate-limit.md`](samples/generated-tests-rate-limit.md) | Validation agent · Documentation agent |
| [`validation-report-rate-limit.md`](samples/validation-report-rate-limit.md) | Documentation agent |
| [`rate-limiter-api.ts`](samples/rate-limiter-api.ts) | Focused subagent (isolation test) |

---

## Step 1 — Set up the run mechanics

An asset is "run" by invoking it in a **fresh chat** with exactly what the definition declares — no extra context:

1. Open a new Agent chat.
2. `@`-mention (or attach) the agent definition and its template, then paste/attach the sample input.
3. Instruct: *"Act as this agent. Inputs are attached. Return only the declared output."*
4. Save the transcript (or its key output) under `shared-agent-library/testing/transcripts/` with a name like `requirement-analysis-run1.md`.
5. Note the model and any settings — evidence must be reproducible.

- [ ] Mechanics tried once end-to-end on the Requirement Analysis agent
- [ ] Transcript saved; model/settings noted

---

## Step 2 — Run the matrix

Run every row. Record **actual** behaviour, not what you expected.

| Asset | Sample input | What you're checking (guide §5) |
|---|---|---|
| Requirement Analysis agent | `raw-requirement-add-rate-limiting.md` | Flags the missing pieces (limits, scope, error behaviour, measurable NFRs) **without inventing criteria** |
| Test Generation agent | `analyzed-requirement-rate-limit.md` | Every AC maps to exactly one generated test; `ac_coverage` complete |
| Validation agent | `generated-tests-rate-limit.md` + `rate-limit-contract.md` | Catches the deliberate mismatch and reports it — **does not** edit the contract |
| Documentation agent | `analyzed-requirement-rate-limit.md` + tests + validation report | Output cites the specific requirement/test IDs, not generic summary |
| Focused subagent | `rate-limiter-api.ts` only | Correct summary using **only** its isolated context |
| Prompt template (pick one) | Its own declared `{inputs}` | Output matches the declared expected-output shape |

- [ ] All six rows run; transcript saved for each
- [ ] In `pass-fail-matrix.md`, each row records: asset · input · expected check · actual · **PASS/FAIL** · evidence link

---

## Step 3 — Contract conformance check

For each run, check the output against the schema you declared in Lab 11.1 — mechanically:

- [ ] Every required output field is present
- [ ] Field types/shapes match (list vs. string, IDs present, etc.)
- [ ] Missing or malformed field → **FAIL**, even if the prose "looks right" (deck: a call missing a required field is rejected)
- [ ] Any FAIL is logged with the exact field that broke the contract

---

## Step 4 — Subagent isolation test

The subagent must work with **no** visibility into the other agents' context:

- [ ] Fresh chat, only `rate-limiter-api.ts` + the subagent definition (no requirement, no tests, no parent discussion)
- [ ] Output matches the declared OUT schema
- [ ] If it needed extra context to produce a correct result, it fails the isolation test — record that and reconsider the delegation (move it back into the parent)

---

## Step 5 — Fix and re-run

For every FAIL (including the deliberately mismatched sample — decide whose artifact is at fault):

1. Diagnose: is it the **definition** (role/inputs/guardrails), the **template** (contract), or the **input**?
2. Revise the asset; bump its version (`0.1.0-draft` → `0.2.0`); record what changed and why.
3. Re-run the affected row; update the matrix.

- [ ] At least one revision recorded with a version bump (the sample's mismatch guarantees one FAIL — the Validation agent should catch it; if it didn't, that's a definition fix)
- [ ] Re-run transcripts saved; matrix updated with final status
- [ ] Expected end state: **all rows PASS** on the re-run (or a documented, justified exception)

---

## Step 6 — Optional cross-check against your own spec

- [ ] Run the Requirement Analysis agent once on a raw ticket for your `<feature>` (or a deliberately weak AC from Module 9) and compare its gap list to what your Module 9 testability pass found
- [ ] Note any gap your manual pass missed — or any invention the agent added (that's a guardrail failure)

---

## Evidence

- `shared-agent-library/testing/pass-fail-matrix.md` — six rows with actual vs. expected, PASS/FAIL, evidence links
- `shared-agent-library/testing/transcripts/` — one saved transcript per run (plus re-runs)
- Revision log: version bumps + what changed (Step 5)
- Isolation-test note for the subagent (Step 4)

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Validation agent "fixes" the test | Guardrail not enforced in the run | Re-run with the definition attached; if it still edits, tighten the guardrail wording to an explicit prohibition and re-test |
| Agent output is good but missing a declared field | Contract violation, easy to wave through | FAIL it; the field exists so a downstream consumer can rely on it (deck: Call C) |
| Every run "passes" suspiciously | Expected-vs-actual not recorded | Record actual output verbatim in the matrix; check field-by-field, not by impression |
| Subagent asks for more context | Wrong candidate or leaky IN list | Narrow the task or fold it into the parent — isolation is the point |
| Re-runs drift between runs | Model nondeterminism | Grade contract conformance and behaviour, not exact wording; keep the transcript that proves the check |
| No runner available | Environment | Use the offline fallback in the facilitator notes: a peer executes the definition manually and records the output shape |

---

## Checkpoint questions

1. Why does each asset get tested independently rather than in one end-to-end chain run?
2. What does "tested" mean for a prompt template?
3. What's the correct outcome when the Validation agent catches the sample's mismatched test?

<details>
<summary>Answers</summary>

1. Isolating each asset's failure before chaining is what makes Module 16's pipeline debuggable: if five assets pass independently, a pipeline failure is orchestration; if you never tested them alone, you can't tell which layer broke.
2. That its output matches the **declared expected-output shape** when given its own declared `{inputs}` — checkable field by field, not judged as "looks right".
3. A PASS for the Validation agent: it reported the mismatch (test expects 200; contract requires 429) without editing the contract. The mismatched test itself is sample input, not the agent's artifact — the fix belongs to the test-generation owner.

</details>

---

## Next

**Lab 11.4 — Commit and Peer Review.** With every asset tested, you commit and tag the library (`v0.1.0`), then swap libraries with another team for review against the six-check rubric — approve or request changes, then adopt at `1.0.0`.

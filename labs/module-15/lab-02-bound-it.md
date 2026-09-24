# Lab 15.2 — Bound It: Failure Policy & the Budget Card

**Module 15 · Subagents & Orchestration Patterns Overview | Xebia — Cursor AI Training**
Day 5 · Lab 2 of 3 · ~8 minutes · Individual or pairs

> **Objective:** give the pipeline an explicit failure policy. Classify what can go wrong at each stage, diagnose
> a run that mishandled almost everything (it retried a deterministic failure, hung without a timeout, overran
> its correction limit, exceeded its budget, and committed anyway), then write the policy and the run + per-stage
> **budget card** that Module 16 executes under. Every loop gets a counter; every run fails safe.

**Guide references:** Module 15, §4 (failure handling, retries, timeouts, bounded execution), §7 walkthrough task 5
**Learning objectives covered:** 5 — retries, timeouts, and bounded execution budgets.

---

## Before you start

- Lab 15.1 complete: `orchestration/pipeline-map.md` and `orchestration/handoff-envelope.md` written
- Open [`samples/incident-run-log.md`](samples/incident-run-log.md)
- Create `orchestration/failure-policy.md` and `orchestration/budget-card.yaml`
- No runner needed

---

## Step 1 — Classify the failures before handling them

For each stage, name its likely failure types and the correct handling pattern (§4): **retry with backoff**, **fail fast**, **bounded correction with findings**, or **timeout + escalate**.

| Stage | Likely failure types (transient / deterministic / quality / hung) | Handling pattern | Why |
|---|---|---|---|
| Requirement Validator | | | |
| Sequence Builder | | | |
| Test Generator | | | |
| API Validator | | | |
| Reviewer | | | |
| Parallel workers (if fan-out is used) | | | |

- [ ] Every stage classified with a handling pattern, not "handle errors"
- [ ] At least one stage where **retry is the wrong answer** — and the reason (deterministic/input failure returns the same result)
- [ ] The partial-parallel case has a **decision**, not a default: fail the whole run, or continue with a flag — written down before it happens

---

## Step 2 — Diagnose run `req-2481-run-09`

Read the incident log and fill the findings table (expect **at least six**; the fixture has more):

| # | Event | Failure type | What the run did | What the policy requires | Corrected handling |
|---|---|---|---|---|---|

Checklist of what a thorough diagnosis catches:

- [ ] The **deterministic failure retried three times** (Validator) and the requirement invented to move on
- [ ] The **missing timeout** on Sequence Builder (12-minute hang)
- [ ] The **retry without new information** (API Validator's FAIL carried no findings or locations)
- [ ] The **correction round counter** exceeded (round 3 against a limit of 2)
- [ ] The **idempotency violation** (correction rounds 2 and 3 wrote over earlier attempt artifacts)
- [ ] The **budget breach that did not stop the run** — 63m / 495k tokens / 132 tool calls against 20m / 400k / 120, then committed
- [ ] The **unflagged partial merge** (the refunds worker failed; AC-4 tests silently absent)
- [ ] The **product defect hidden by a test edit** (the AC-3 assertion changed from 403 to 404 so the suite goes green)
- [ ] The **invalid review** (Envelope 5: generator summary in, original AC missing)
- [ ] The **broken trace** (envelopes 1 and 3 with no `pipeline_run_id`) and why that matters after the fact
- [ ] The **skipped human sign-off** before commit
- [ ] One line: for each finding, which Module 17/18 mechanism will enforce it (gate, hook, approval checkpoint)

---

## Step 3 — Write the budget card

Create `orchestration/budget-card.yaml` — the config Module 16 runs under:

```yaml
pipeline: requirement-to-test
budgets:
  run:
    max_wall_clock: 20m
    max_total_tokens: 400k
    max_tool_calls: 120
  per_stage:
    validator:        { timeout: 3m, max_retries: 1 }
    sequence_builder: { timeout: 5m, max_retries: 1 }
    test_generator:   { timeout: 8m, max_retries: 2, max_correction_rounds: 2 }
    api_validator:    { timeout: 5m, max_retries: 1 }
    reviewer:         { timeout: 5m, max_retries: 1 }
on_budget_exceeded: halt_and_escalate
on_partial_parallel: fail_run          # or: continue_with_flag — your call, justified
retry_policy: exponential_backoff(base=5s, factor=2)
idempotency: stage outputs written to new files per attempt (…_attempt2.json)
```

- [ ] Every number has a one-line **rationale** (a comment or a line in `failure-policy.md`) — no copying without reasoning
- [ ] The **Sequence Builder gap from run-09 is closed** (timeout set) and `max_correction_rounds` is enforced, not just declared
- [ ] `on_budget_exceeded: halt_and_escalate` stated — with a sentence on what "escalate" means: who is told and what they see (Module 14's approval/observability artifacts)
- [ ] `on_partial_parallel` decided; if `continue_with_flag`, name where the flag goes so it reaches the reviewer and the human
- [ ] One sentence: why fail-safe (halt) beats fail-open (ship the partial result) in an audited pipeline

---

## Step 4 — Write the failure policy

In `orchestration/failure-policy.md`, combine:

- [ ] The Step 1 classification table
- [ ] The Step 2 findings table with corrected handling
- [ ] The four rules, stated in your own words:
  - **Fail early and cheaply** — a strict Validator at the front saves every downstream token
  - **Retry only what retrying can fix** — transient errors; deterministic failures fail fast
  - **Every retry carries new information** — a quality retry without the reviewer's findings is a re-roll
  - **Every loop has a counter** — no unbounded `while not passed`
- [ ] One sentence defining **fail safe, not open**
- [ ] One sentence: why a retry that reuses the same context and inputs will produce the same failure

---

## Evidence

- `orchestration/failure-policy.md` — classification table + incident findings + the four rules
- `orchestration/budget-card.yaml` — run and per-stage budgets with rationale, retry policy, partial-parallel decision, idempotency rule

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Everything gets "retry 3×" | No failure taxonomy | Classify first: transient vs. deterministic vs. quality vs. hung — only the first retries blindly |
| Budget card copied from the guide without edits | Skipped the incident | Close the gaps run-09 exposed: Sequence Builder timeout, round counter, partial-parallel decision, idempotency |
| "Escalate to the team" | Vague escalation | Name who is told and what they see (findings, artifact refs, attempt count, cost so far) |
| Partial-parallel left undecided | Assumed the merge step handles it | Decide `fail_run` or `continue_with_flag` now; an undecided gap ships silently |
| Only tokens budgeted | Wall-clock and tool calls skipped | All three run-level caps; a hung stage burns wall-clock without burning many tokens |
| Retry overwrites the failed attempt | No idempotency rule | New artifact per attempt — the failed attempt is evidence, not garbage |

---

## Checkpoint questions

1. A stage fails because the requirement has no acceptance criteria. Retry or fail fast — and why?
2. Why must a quality retry include the reviewer's findings?
3. What does "fail safe, not open" mean when a pipeline exceeds its token budget?

<details>
<summary>Answers</summary>

1. **Fail fast.** This is a deterministic/input failure — retrying produces the same failure several times and burns budget. Route it to the requirement owner (the Validator's FAIL path).
2. Without the findings, the generator retries with the same inputs and the same reasoning, so it produces essentially the same output — a re-roll, not a correction. The findings (artifact, location, expected vs. actual) are the new information that makes the next attempt different.
3. The pipeline **halts and escalates to a human**. It never continues silently, and it never presents a partial result as if it were complete — a budget is a control, not a suggestion.

</details>

---

## Next

**Lab 15.3 — Right-Size and Place It: Granularity, Trace & the CI Boundary.** The pipeline is bounded; now decide whether each step should be an agent at all, sketch the trace that proves what happened, and split what stays Cursor-native from what moves to CI.

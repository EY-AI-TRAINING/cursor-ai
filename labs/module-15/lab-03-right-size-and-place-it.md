# Lab 15.3 — Right-Size and Place It: Granularity, Trace & the CI Boundary

**Module 15 · Subagents & Orchestration Patterns Overview | Xebia — Cursor AI Training**
Day 5 · Lab 3 of 3 · ~8 minutes · Individual or pairs

> **Objective:** finish the walkthrough's last two tasks. Route six proposed agents through the §5 decision
> tree — accepting only what earns its handoff, rejecting the anti-patterns; review two proposed merges
> (one hides self-approval); sketch the run trace with one id and mark where the chain broke; and split the
> pipeline's concerns into Cursor-native orchestration versus external orchestration for three real scenarios.

**Guide references:** Module 15, §5 (orchestration granularity), §6 (observability across handoffs; Cursor-native vs. external), §7 walkthrough tasks 6–7
**Learning objectives covered:** 6 — granularity and avoiding unnecessary agents; 7 — observability and the native/external boundary.

---

## Before you start

- Labs 15.1–15.2 complete: envelope contract, failure policy, budget card written
- Open [`samples/granularity-candidates.md`](samples/granularity-candidates.md) and keep [`samples/incident-run-log.md`](samples/incident-run-log.md) nearby
- Create `orchestration/granularity-review.md` and `orchestration/runtime-plan.md`
- No runner needed

---

## Step 1 — Route the six candidates through the decision tree

For each candidate in Part A of the fixture, answer the four questions and give a verdict (§5):

| # | Candidate | Q1 Different role/tools/permissions? | Q2 Context pollution? | Q3 Independent judgement? | Q4 Parallel gain > merge cost? | Verdict | One-line argument |
|---|---|---|---|---|---|---|---|
| 1 | Formatter agent | | | | | | |
| 2 | Codebase explorer subagent | | | | | | |
| 3 | Saver agent | | | | | | |
| 4 | Security reviewer (parallel) | | | | | | |
| 5 | Scheduler agent | | | | | | |
| 6 | Fidelity checker | | | | | | |

- [ ] At least one **accepted subagent** — justified by context isolation, with the structured result it returns named
- [ ] The **scheduler** rejected as **LLM-as-scheduler**, and what replaces it stated (deterministic control flow in config/script/CI — LLM judgement stays for content, not control flow)
- [ ] At least one candidate rejected as **agent-per-verb**, with where the work actually goes (inline step, rule, skill, or script)
- [ ] The parallel candidate judged on **merge cost and token spend**, not enthusiasm — accept with a stated condition, or defer with a named trigger to revisit
- [ ] The fidelity-checker verdict states why it duplicates the Reviewer's mandate or what genuinely new isolation it would need

---

## Step 2 — Review the two proposed merges

| # | Merge | Verdict | Reasoning (§2 single responsibility, §5 tree) |
|---|---|---|---|
| M1 | Requirement Validator + Sequence Builder | | |
| M2 | API Validator into Test Generator | | |

- [ ] M1: apply the test honestly — one role or two? Whichever you choose, state what is lost (fail-fast position, independent re-derivation) and why that loss is or isn't acceptable
- [ ] M2: rejected — merging a validator into the thing it validates is **self-approval**; name the failure that becomes invisible when the same agent generates and verifies
- [ ] Quote **one anti-pattern** from §5's table that appears in the sample pipeline or run-09 (e.g., unbounded orchestrator, telephone game, parallel for show) and where it appears
- [ ] One sentence: what a new agent must earn before it is added (different role/tools, context isolation, or independent judgement)

---

## Step 3 — Sketch the trace

Build the trace for `req-2481-run-09` from the incident log — one run id, one span per stage/attempt. The table below is a starter: add rows as needed (the fixture has a dozen spans).

| Span (stage · attempt) | Status | Tokens | Wall-clock | Notes |
|---|---|---|---|---|
| | | | | |
| | | | | |
| | | | | |
| | | | | |

- [ ] Spans in order, with attempt numbers (`a1`, `a2`, `a3`) so a retry is visible, not hidden
- [ ] **Chain break marked** — which envelopes carried no `pipeline_run_id`, and what that costs when you debug the run three weeks later
- [ ] Each of §6's four questions answered in **one line from the evidence**:
  1. **What happened?** (ordered statuses and attempts)
  2. **Why?** (inputs, evidence, findings at each stage)
  3. **Where did cost go?** (which stage/attempt dominates)
  4. **What changed?** (artifact refs and `stage_version` — and note where the run omitted them)
- [ ] One span a dashboard should flag first, and why that one
- [ ] One sentence: why per-call logs without a shared run id cannot answer these questions

---

## Step 4 — Draw the Cursor-native / external boundary

For each scenario in Part C of the fixture, decide where the concern lives and what each side owns (§6):

| # | Scenario | Cursor-native / external / both | Who drives the sequence | Lifecycle controls | Observability |
|---|---|---|---|---|---|
| 1 | Interactive debugging of a failing generated test | | | | |
| 2 | Required API-validator check on every ticket/PR | | | | |
| 3 | Nightly test-vs-contract audit | | | | |

- [ ] All three placed; the reasoning names the trigger (human steering vs. event/schedule) and the audit requirement
- [ ] One sentence: **one set of versioned role definitions in the repo is shared by both sides** — the same agent files, loaded by the IDE and by the CI runner
- [ ] The rule of thumb in your own words: interactive steering → Cursor-native; deterministic, repeatable, must-be-audited → external
- [ ] One line on what should **not** be moved to CI yet, and the condition that would change that (this is also Module 19's starting point)
- [ ] One sentence: why "we'll add observability when we go to CI" is backwards — the trace must exist while you iterate, or there is nothing to promote

---

## Evidence

- `orchestration/granularity-review.md` — six decision-tree rows, two merge verdicts, anti-pattern quote, the new-agent rule
- `orchestration/runtime-plan.md` — trace sketch with chain break + four answers; boundary table for the three scenarios; shared role-definition statement

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Every candidate has "separation of concerns" as its reason | Rationale borrowed, not tested | Answer Q1–Q4 explicitly; a role that needs no different tools, isolation, or judgement stays inline |
| Parallel reviewer accepted without conditions | Merge cost ignored | Same diff + no shared writes is the bar; state the merge and the token cost you accept |
| Trace looks like a list of log lines | No run id or attempts | One `pipeline_run_id`; a span per attempt; retries visible as spans, not footnotes |
| Boundary drawn along "important vs. unimportant" | Wrong axis | The axis is **human steering vs. event-triggered and auditable** — and deterministic steps belong in code/CI |
| Fidelity checker accepted because "drift is bad" | Duplicate role not noticed | The Reviewer already judges against original AC; a second checker adds a handoff, not a control — or name the new isolation it genuinely needs |
| CI split leaves role definitions duplicated | Two sources of truth | One versioned set in the repo, loaded by IDE and CI alike |

---

## Checkpoint questions

1. Name two situations where adding a separate agent is justified, and one anti-pattern where it isn't.
2. Why is one shared run id more useful than perfectly ordered logs?
3. Give one pipeline concern that belongs in Cursor-native orchestration and one that belongs in external orchestration.

<details>
<summary>Answers</summary>

1. Justified: a different role, tools, or permissions; context isolation that keeps the parent small; or independent judgement over another agent's work. Anti-pattern example: agent-per-verb (a formatter/saver agent for what an inline step or script does), or LLM-as-scheduler for deterministic control flow.
2. Order is not identity: tasks interleave, retries repeat stages, and parallel workers finish out of order. A shared run id reconstructs cause and effect — "which input did the failing attempt receive?" — across interleaved and retried spans, which chronological logs alone cannot.
3. Cursor-native: interactive iteration with subagents and hooks while the developer steers. External: the required API-validator check on every ticket/PR, or the nightly audit — repeatable, event-triggered, and auditable regardless of who is at the keyboard.

</details>

---

## Next

**Lab 15.4 (optional) — Rehearse Module 16 on Your Own Library**, then **Module 16 — Use Case Lab 3: Multi-Agent Requirement-to-Test Automation** builds this pipeline for real. Bring `handoff-envelope.md`, `failure-policy.md`, `budget-card.yaml`, and `runtime-plan.md`: Module 16 runs on them.

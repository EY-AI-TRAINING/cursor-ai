# Lab 7.2 — Debug Mode: Hypothesis Before Fix

**Module 7 · Plan, Debug, Refactoring & Testing | Xebia — Cursor AI Training**
Day 2 · Lab 2 of 3 · ~20–25 minutes · Individual, facilitator-supervised

> **Objective:** take a provided failing scenario through the hypothesis-driven loop — reproduce → explain the
> stack trace → hypothesize → validate → *then* fix. No proposed fix is accepted until its cause has been
> confirmed by evidence you gathered.

**Guide references:** Module 7, §2 (Debug mode and validating hypotheses), §4 (explaining stack traces; suggest/apply fixes)
**Learning objectives covered:** 2 — hypothesis-driven debugging; 4 — explain → identify → fix.

---

## Before you start

- Lab 7.1 complete, still on `module7-lab`
- `<failing-scenario>` provided by your facilitator: a failing test with its output/stack trace (reference
  example from the deck: *"`applyDiscount()` sometimes returns a negative price when discount codes are
  stacked"*)
- Reproduction command known — usually a single test, e.g. `<test-command> <failing-test>`
- **Discipline:** you will *not* ask for or apply a fix until Step 5. If the agent offers one earlier, stop it and
  redirect.

---

## Step 1 — Reproduce and capture the failure verbatim

1. Run the failing case yourself and capture the raw output — the full stack trace, not a paraphrase:

   ```bash
   <test-command> <failing-test> > /tmp/failure.txt   # or copy from the terminal
   ```

2. Note whether it fails every time or only sometimes (intermittent failures change the debugging strategy).

- [ ] Failure reproduced; raw output saved
- [ ] Deterministic? `____________` (if flaky: what varies between runs? `____________`)

---

## Step 2 — Stack-trace handoff: explain, then locate (no fix yet)

Work §4's three-step handoff, stopping before step 3:

1. **Explain:** paste the trace and ask — *"Explain this failure in the context of this codebase: what failed, and
   how execution got there."*
2. **Locate:** *"Which specific line/condition is the most likely origin, and what is the evidence for that?"*
3. (Step 3, "fix," comes later — after your hypothesis is confirmed.)

- [ ] Plain-language explanation captured
- [ ] Candidate origin recorded with the evidence the AI cited: `____________`

---

## Step 3 — Write YOUR hypothesis before any fix

Fill this in yourself — reviewable artifact, not chat exhaust:

> **Because** `____________` (evidence),
> **I think the root cause is** `____________`.
> **If that's true, I predict** `____________` (what a log line, targeted assertion, or focused test will show).

Then ask the agent to **validate, not fix**:

> "Do not change the fix yet. Add temporary logging / a targeted check that would confirm or refute this
> hypothesis, and show me the evidence."

- [ ] Hypothesis written before any code change toward a fix
- [ ] Validation evidence gathered (log output, focused assertion result, inspected state)

---

## Step 4 — Confirm or refute

| Outcome | Evidence | Next |
|---|---|---|
| Confirmed | | Step 5 |
| Refuted | | Back to Step 3 with an alternative hypothesis |

- [ ] Status recorded: confirmed / refuted (if refuted: number of loop iterations `____________`, alternative hypothesis captured)
- [ ] Remove temporary instrumentation before fixing (or keep deliberately as part of the fix evidence)

---

## Step 5 — Fix grounded in the confirmed cause

Now — and only now — request and review the fix with Module 5/6 discipline:

1. Ask for the minimal fix that addresses the confirmed cause (not a symptom).
2. Review the diff; reject anything that changes unrelated behavior.
3. Apply and re-run the failing case, then the **full** suite:

   ```bash
   <test-command> <failing-test>
   <test-command>
   ```

- [ ] Fix reviewed before applying; diff is minimal and on-cause
- [ ] Failing case now passes; full suite green (output recorded)
- [ ] No unrelated behavior changed

---

## Step 6 — Leave a regression test behind

1. Keep or add a test that fails on the old behavior and passes now (if the provided failing test *is* that test, keep it).
2. Commit on the branch:

   ```bash
   git add -A && git commit -m "Module 7 lab: fix <bug> (hypothesis-validated)"
   ```

- [ ] Regression coverage in place; commit hash `____________`

---

## Evidence

- Raw failure output (Step 1)
- Explanation + located origin (Step 2)
- Your written hypothesis + validation evidence (Steps 3–4)
- Reviewed fix diff + full-suite green output (Step 5) + regression test (Step 6)

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Agent proposes a fix immediately | Debug mode/agent defaulting to action | Stop it; paste your Step 3 prompt: "Do not fix yet — validate this hypothesis" |
| Hypothesis can't be tested | Too vague ("something's wrong with state") | Sharpen until it makes a falsifiable prediction |
| Hypothesis refuted repeatedly | Insufficient evidence upfront | Go back to Step 1/2: gather more context before hypothesizing again |
| Fix "works" but you can't explain why | Cause still unconfirmed — fix may mask a symptom | Return to Step 3; a working diff without a confirmed cause is not done |
| Full suite reveals new failures | Fix changed behavior elsewhere | Treat each new failure as its own mini-loop (Steps 1–5); or reconsider the fix |
| Failure is flaky | Timing/state/concurrency | Record what varies; hypothesis must address the nondeterminism, not just one run |

---

## Checkpoint questions

1. Why does Debug mode insist on a stated, validated hypothesis before applying a fix?
2. What are the three steps of the stack-trace handoff, in order?
3. How do you know a hypothesis is confirmed rather than merely plausible?

<details>
<summary>Answers</summary>

1. It prevents a plausible-sounding but ungrounded fix (the Module 1 hallucination risk applied to diagnosis) — a fix without a validated cause just patches a symptom.
2. Explain ("what does this trace mean here?") → Identify/locate ("where exactly and why?") → Fix ("propose/apply the fix"), reviewed and validated.
3. You made a falsifiable prediction and gathered evidence (log output, focused assertion, inspected state) that matched it — the cause is confirmed by observation, not by the fix "seeming to work."

</details>

---

## Next

**Lab 7.3** — lock in behavior with characterization tests, refactor legacy code, and practice the test-failure feedback loop.

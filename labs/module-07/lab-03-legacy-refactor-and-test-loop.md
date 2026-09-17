# Lab 7.3 — Legacy Refactor & the Test Feedback Loop

**Module 7 · Plan, Debug, Refactoring & Testing | Xebia — Cursor AI Training**
Day 2 · Lab 3 of 3 · ~20–25 minutes · Individual

> **Objective:** refactor untested or unclear-intent code safely — characterize first, refactor second — then close
> the loop by writing behavior-focused tests and feeding a failing result back as context until it goes green.

**Guide references:** Module 7, §3 (natural-language refactoring; legacy code), §5 (writing/executing/debugging tests), §6 (validating refactors; failures as context)
**Learning objectives covered:** 3 — legacy refactoring; 5 — AI-assisted tests; 6 — validate against tests, use output as feedback.

---

## Before you start

- Labs 7.1–7.2 complete, still on `module7-lab`
- `<legacy-target>` chosen — untested or unclear-intent code, marked by your facilitator (if none is marked,
  ask; a good candidate is a function with branching edge cases and no dedicated tests)
- Know your `<test-command>`
- Reminder of the rule: characterization tests capture **current** behavior without judging it; behavior must be
  identical before and after the refactor

---

## Step 1 — Understand before changing

Use Chat/Debug mode (not an edit mode) to build understanding of `<legacy-target>`:

> "Explain what `<legacy-target>` does, including every edge case and any surprising behavior. Do not change
> anything."

- [ ] Understanding notes captured: inputs, outputs, edge cases, surprises
- [ ] Any suspicious behavior recorded as a *finding* — not fixed yet: `____________`

---

## Step 2 — Characterization tests first (lock in behavior)

Ask for tests that capture current behavior, warts included:

> "Write characterization tests for `<legacy-target>` that capture its current behavior exactly as it is —
> including edge cases — without judging correctness. Do not modify the code."

- Run them against the **unmodified** code — they must all pass.

- [ ] Characterization tests pass against current code (output recorded)
- [ ] Every branch/edge case you found in Step 1 has coverage

---

## Step 3 — Refactor with a natural-language instruction

Now issue a well-scoped, behavior-preserving refactor, for example:

> "Refactor `<legacy-target>`: extract `<responsibility>` into a separate function and rename `<vague-name>` to
> `<clear-name>`. Preserve behavior exactly. Change nothing outside `<target-file>` and do not alter the tests."

Review the diff with Module 6 discipline before applying.

- [ ] Refactor instruction scoped; boundary stated
- [ ] Diff reviewed — every change is structural, none behavioral

---

## Step 4 — Validate, and feed failures back (the §6 loop)

1. Run the characterization tests, then the full suite:

   ```bash
   <test-command>          # characterization tests included
   ```

2. **If everything is green:** the refactor is validated — record the output as your safety-net evidence.
3. **If something fails:** do not hand-describe the failure. Paste the exact output (which test, expected vs.
   actual) back to the agent as context and ask it to revise the refactor accordingly. Re-run. Record each
   iteration:

| Iteration | What failed (test + expected vs. actual) | Feedback given to agent | Result |
|---|---|---|---|
| 1 | | | |
| 2 | | | |

- [ ] All characterization tests + full suite green against the refactored code
- [ ] At least one feedback iteration logged with the verbatim failure output (if no failure occurred, document
      the green run and answer: what output *would* you paste if a test failed?)

---

## Step 5 — Behavior-focused tests + classify a failing test

Write new tests for expected behavior — not a mirror of the implementation. Use the §5 patterns:

| Test type | Prompt pattern |
|---|---|
| Unit | "Test `<fn>` for zero, negative, and boundary values" |
| API | "Test that `<method> <route>` returns 400 when `<field>` is missing" |

1. Pick a small piece of functionality (the refactored code is a fine choice) and write 2–3 behavior-focused tests.
2. Deliberately include one case for behavior the code does **not** currently guarantee (an edge case or an
   expected-but-missing rule).
3. Run them and classify each failure per §5's flow:
   - **Fail — bug in code** → fix with Lab 7.2 discipline (hypothesis first, then fix)
   - **Fail — bad test** → fix the test (the expectation was wrong)
4. Record which way you classified it and why.

- [ ] 2–3 behavior-focused tests written and executed
- [ ] The deliberate failure classified: bug in code / bad test — with reasoning
- [ ] Whatever you fixed (code or test) re-validated with the full suite

---

## Step 6 — Commit and wrap up

```bash
git add -A
git commit -m "Module 7 lab: refactor <legacy-target> + characterization & behavior tests"
```

- [ ] Commit on `module7-lab`; hash `____________`

---

## Evidence

- Understanding notes (Step 1) + finding(s) recorded without fixing
- Characterization tests passing against original code (Step 2)
- Refactored diff (Step 3)
- Feedback-loop table with verbatim failure output and the revision result (Step 4)
- New behavior tests + failure classification (Step 5)

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Characterization test fails against original code | The test asserts *expected* rather than *current* behavior, or found a real bug | Decide deliberately: adjust to capture current behavior, or record it as a Step 1 finding; don't silently "fix" the code |
| Refactor changes behavior (suite red) | Instruction said "clean up" without "preserve behavior" | Revert; re-instruct with "preserve behavior exactly; change nothing outside `<scope>`" |
| Agent edits the tests to make them pass | Tests are the safety net — not to be adjusted | Revert test changes; re-run; feed the code failure back instead |
| Feedback loop doesn't converge after 2–3 iterations | Refactor step was too broad | Revert to the last green commit; decompose the refactor (Module 6, §6) and redo smaller |
| New test deliberately "fails" but classification is unclear | Ambiguous expectation | State the expected behavior in plain language first; if it's not guaranteed today, it's a bug or a changed requirement — decide which |

---

## Checkpoint questions

1. What should you do before refactoring legacy code that has no tests?
2. What makes a test prompt "behavior-focused," and why is that more durable?
3. In the refactor-validate-feedback loop, what exactly gets fed back — and what makes it valuable?

<details>
<summary>Answers</summary>

1. Write characterization tests that lock in the code's current behavior (warts included), giving the refactor a safety net to validate against.
2. It describes an observable outcome under specific conditions ("returns 404 for an unknown ID") rather than mirroring the implementation — so it stays valid when the implementation changes, as long as behavior doesn't.
3. The raw failing test output — which test, expected vs. actual. It's valuable because it's precise, tool-generated context that the agent can act on directly, closing the loop faster than a human-paraphrased description.

</details>

---

## Next

Module 7's exercise is complete — your facilitator delivers the knowledge check (Plan mode's stages, confirmed vs. unconfirmed hypotheses, root-cause frames) separately.
**Module 8 — Rules, AGENTS.md, Skills & Team Standards** turns these habits into team-wide, durable instructions.

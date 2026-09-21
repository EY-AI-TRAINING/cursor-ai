# Lab 13.4 — Stress-Test the Grounding

**Module 13 · Use Case Lab 2: Knowledge-Grounded Engineering Agent | Xebia — Cursor AI Training**
Day 4 · Lab 4 of 5 · ~20 minutes · Individual or pairs

> **Objective:** do guide §4 — prove the agent is grounded by attacking it. Run the adversarial set across all
> four categories (in-scope, ambiguous, out-of-scope, plausible trap) plus the Module 12 regression, record
> predictions **before** each run, and put every FAIL through the diagnose → fix → re-run loop: scoping gap,
> citation gap, or rule not enforced.

**Guide references:** Module 13, §4 (stress-testing refusal/grounding); Module 11 §5 (test each asset independently)
**Learning objectives covered:** 5 — stress-test with out-of-scope questions and verify refusal behavior.

---

## Before you start

- Lab 13.3 complete: rule loaded and enforcement-tested (refusal phrase + citation format proven without restating)
- Open [`samples/grounding-stress-questions.md`](samples/grounding-stress-questions.md) — ST-1…ST-6
- `shared-agent-library/testing/grounding-stress-test.md` exists with the enforcement-layer table and ST-1 row
- Every run: **fresh chat**, rule not restated, grounded sources reachable

---

## Step 1 — Predict before you run

A stress test is only evidence if the expectation is written first. Fill the Expected column for ST-1…ST-6 **before** any run:

| # | Category | Expected (from the question's required behaviour — no answers) |
|---|---|---|
| ST-1 | In-scope, well-supported | |
| ST-2 | In-scope, ambiguous | |
| ST-3 | Out-of-scope | |
| ST-4 | Plausible-sounding trap | |
| ST-5 | Partial coverage | |
| ST-6 | Regression (GQ-3) | |

- [ ] All six predictions written down before running
- [ ] At least one category gets a question of **your own** (about `<feature>`), added as ST-7 — the shipped set is a starting point, not the whole test

---

## Step 2 — Run the set

- [ ] Each question run in a fresh chat; transcript captured and linked from the matrix
- [ ] The rule was **not** restated in any prompt (that's the point)
- [ ] Actual column recorded verbatim enough to check citations

---

## Step 3 — Mark PASS/FAIL and diagnose every failure

Fill the matrix:

```markdown
| # | Category | Expected | Actual | PASS/FAIL | Evidence |
```

Diagnose each FAIL with the guide's loop — the cause determines the fix:

| Diagnosis | Symptom | Fix |
|---|---|---|
| **Scoping gap** | Relevant source never retrieved, or wrong source retrieved | Fix `retrieval-scope.yaml` allow/deny lists; re-check MCP scope |
| **Citation gap** | Claim present but no citation, or vague/wrong citation | Fix the citation format clause in the rule |
| **Rule not enforced** | Behavior changes with phrasing; refusal phrase absent; premise accepted | Fix the rule's load location or wording; re-run the enforcement test |

- [ ] Every FAIL has a named diagnosis (not "the model was off today")
- [ ] **ST-3** declines and **ST-6** declines without substituting the 30-day log retention
- [ ] **ST-4** does not agree with the false premise — it checks the standard and runbook, then corrects or declines
- [ ] **ST-2** presents both enforcement layers with citations; a one-sided answer is a FAIL
- [ ] **ST-5** carries a caveat for the undocumented part, not a confident generalization
- [ ] ST-7 (your own) behaved as predicted, or was diagnosed and fixed like the rest

---

## Step 4 — Fix, re-run, version

- [ ] For each FAIL: apply the fix, **re-run the same question in a fresh chat**, attach the new transcript
- [ ] Bump the agent version `0.1.0-draft` → `0.2.0` and record what changed in a revision log (in the matrix file or `testing/revision-log.md`)
- [ ] If everything passed on the first run: add one more question per category (ST-8+) rather than declaring victory — a test set that never challenges anything isn't a stress test
- [ ] The matrix shows, for each fixed row, the failing run **and** the passing re-run

---

## Evidence

- `shared-agent-library/testing/grounding-stress-test.md` — six-plus rows: category, prediction, actual, PASS/FAIL, evidence; diagnoses for every FAIL
- Transcripts for every run and re-run
- Revision log + agent version bumped to `0.2.0`
- Rule/scope changes linked from the failing rows

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Agent agrees with the ST-4 premise | Rule lacks a clause about not accepting the question's premise | Add: "Do not accept a premise from the question; verify it against the sources and correct or decline" |
| ST-2 answered from only one source | Allow list or retrieval pulls one layer only | Check both SDS and runbook are in `allow_paths` and reachable; re-run |
| An answerable question gets declined | Scope too narrow, or source not actually reachable | Widen `allow_paths`; verify reachability again (Lab 13.1 Step 6) |
| ST-5 answered confidently with no caveat | Rule silent on partial coverage | Add: "If only part of the question is supported, answer that part and flag the rest as not found" |
| Every run passes instantly | Questions are too easy (or you restated the rule) | Fresh chat, rule not restated; add your own adversarial questions — especially the trap category |
| Refusal phrase varies run to run | Phrase not mandatory/exact in the rule | Quote it exactly; re-run ST-3 |
| Transcripts lost | Chat closed without capture | Re-run — the re-run is also evidence of reproducibility, and note the nondeterminism |

---

## Checkpoint questions

1. Why does an out-of-scope question prove grounding better than a well-answered one?
2. What exactly does the plausible-sounding trap question check?
3. How do you tell a scoping gap from a citation gap from a rule-enforcement gap?

<details>
<summary>Answers</summary>

1. A correct answer can come from the model's general knowledge; a correct **refusal** can only come from the grounding discipline — the agent must know what it doesn't have. It's the behaviour that separates a grounded agent from a fluent one.
2. That the agent doesn't accept a confidently-phrased false premise. It must verify the claim against the actual sources — the standard and the runbook — and correct or decline, rather than agreeing because the question implied it.
3. Where the failure occurred: retrieval (the right source never arrived → scoping), the answer (claim present but not checkably cited → citation format), or the behavior (refusal/premise handling changes with phrasing or the rule isn't loaded → enforcement).

</details>

---

## Next

**Lab 13.5 — Commit, Peer Review, and Adopt.** The agent is tested; now it earns trust. Commit and tag, let another team try to break the grounding, run the changes-requested loop if needed, and adopt the asset into the shared library.

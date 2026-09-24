# Lab 16.7 — Close the Loop: Traceability, Run Log & Human Approval

**Module 16 · Use Case Lab 3: Multi-Agent Requirement-to-Test Automation | Xebia — Cursor AI Training**
Day 5 · Lab 7 of 8 · ~15 minutes · Individual or pairs

> **Objective:** make the run walkable in both directions. Anyone — reviewer, auditor, future maintainer —
> must be able to start from any acceptance criterion and reach its tests and results, or start from any
> test and reach its AC, without asking who built it. Then put the run log and human approval in place so
> the commit is a documented decision, not a habit.

**Guide references:** Module 16, §6 (end-to-end run, traceability, run log)
**Learning objectives covered:** 6 — end-to-end traceability; evidence for the human approval checkpoint.

---

## Before you start

- Labs 16.2–16.6 complete: artifacts 01–05 in `runs/req-2481-run-01/`
- The suite runs against the sandbox (Lab 16.5 execution results at hand)
- Human approver available: your facilitator, a peer team member, or the requirement owner role

---

## Step 1 — Build `traceability.md`

| AC-ID | Scenario(s) | Test function(s) | Result | Evidence / notes |
|---|---|---|---|---|
| AC-1 | | | | |
| AC-2 | | | | |
| AC-3 | | | | |
| AC-4 | | | | |

- [ ] Every AC row: scenarios → tests → result → evidence pointer (04 report section, JUnit XML)
- [ ] Every test row: reachable from an AC; no test without a SEQ and an AC (walk the test file's markers)
- [ ] The known failure is recorded honestly with its defect id (`DEF-…`) and "test stays failing" — not hidden, not `xfail` without a link
- [ ] `AC-4` points at the scenario that implements the owner's clarification from Lab 16.2

---

## Step 2 — Generate results and join them

```bash
pytest -m "req('REQ-2481')" --junitxml=runs/req-2481-run-01/results.xml
```

- [ ] `results.xml` written to the run folder
- [ ] The results table in `traceability.md` matches the raw output — **spot-check one row by hand** (pick a test, find its line in the XML/output, confirm pass/fail)
- [ ] One sentence: how you joined markers ↔ `02_test_sequence.json` ↔ results (script, reviewer agent, or careful manual join — name the method)

---

## Step 3 — Complete the run log

One line per **stage attempt**, not per stage — the retry history is the point:

```jsonc
{"run_id":"req-2481-run-01","stage":"requirement-validator","v":"1.0.0","attempt":1,"status":"NEEDS_HUMAN","out":"01_validated_requirement.md","tokens":…,"duration_s":…,"ts":"…"}
{"run_id":"req-2481-run-01","stage":"requirement-validator","v":"1.0.0","attempt":2,"status":"PASS","out":"01_validated_requirement.md","tokens":…,"duration_s":…,"ts":"…"}
```

- [ ] All five stages present; **both validator attempts** visible; generator attempts visible (including any correction round)
- [ ] Each line carries `run_id`, `stage`, `v`, `attempt`, `status`, `out`, tokens, duration, timestamp — the Module 14 §5 fields
- [ ] Totals against your Module 15 budget card: wall-clock, tokens, correction rounds (2 max) — note any near-miss
- [ ] One sentence: which stages Module 18 would re-run if only the Generator's output changed (stages 3–5, because 1–2 are upstream)

---

## Step 4 — Human approval

- [ ] Prepare the approval packet: `05_review_signoff.md` verdict, coverage line, known defect id, run id, test results summary
- [ ] The human approver reviews and records their decision — in the approval note file, PR description, or commit trailer: approver name/role, date, run id, verdict, and what happens to the open defect
- [ ] If approval is withheld, the run does not proceed — the pipeline stops and reports, exactly like a `NEEDS_HUMAN` status
- [ ] One sentence: why "tests pass" is not sufficient grounds for approval in this pipeline

---

## Evidence

- `runs/req-2481-run-01/traceability.md` — bidirectional mapping with results and evidence
- `runs/req-2481-run-01/results.xml` — raw test results
- `runs/req-2481-run-01/run_log.jsonl` — one line per attempt, all five stages, tokens/time
- Human approval record (approver, date, run id, verdict, defect disposition)
- Spot-check note

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Traceability written by hand and already stale | Manual table, no join | Regenerate it from markers + sequence + results; keep the generation method in the run notes |
| Only final attempts in the log | "The retry doesn't matter" | Log every attempt — retries are what Modules 17–18 gate and correct on |
| AC row with no result | Test skipped or missing | Missing test = coverage gap (traceability finding); skipped test needs a linked defect id |
| All results ✔ but the defect exists | Assertion changed to match the API | Recheck Lab 16.5's classification; failure honesty beats a green suite |
| Approver has nothing to read | Approval packet not prepared | Assemble 05 + coverage + defect + run id into one place; that packet *is* the decision context |
| `results.xml` outside the run folder | Path slip | Every run artifact lives under `runs/<run_id>/` — move it and note the path in traceability |

---

## Checkpoint questions

1. What makes the suite "traced back to its source requirement," concretely?
2. Why does the run log need one line per attempt rather than one per stage?
3. What does the human approver need to see before approving the commit?

<details>
<summary>Answers</summary>

1. Every test carries `req`/`ac`/`seq` markers; `traceability.md` maps each AC to its scenarios, tests, and results in both directions; `run_log.jsonl` and the run folder show how each artifact was produced. Anyone can walk any point of the chain to any other without asking the author.
2. Attempts are the evidence of honesty and bounded execution: a validator that returned `NEEDS_HUMAN` then `PASS` tells a different story from one that passed first time; a generator that needed 3 rounds is a signal. Collapsing attempts hides both retries and budget consumption — the raw material for Module 17 gates and Module 18 correction loops.
3. The reviewer's verdict and per-AC coverage, any open product defects and their disposition, the run id, and the test results summary — enough to make an accountable decision, not just "the suite is green."

</details>

---

## Next

**Lab 16.8 — Commit & Peer Review: Run It on a Second Requirement.** The deliverable is complete. Commit it with a message that references the run, then swap pipelines with another team and run theirs on a requirement they have never seen.

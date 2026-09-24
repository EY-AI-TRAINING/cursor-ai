# Lab 16.8 — Commit & Peer Review: Run It on a Second Requirement

**Module 16 · Use Case Lab 3: Multi-Agent Requirement-to-Test Automation | Xebia — Cursor AI Training**
Day 5 · Lab 8 of 8 · ~15 minutes · Team A ↔ Team B peer review

> **Objective:** finish the use-case-lab lifecycle — self-check the deliverable, commit it with the run
> referenced, then **swap pipelines** with another team and run theirs on a second requirement
> ([`samples/requirements-REQ-2482.md`](samples/requirements-REQ-2482.md)) they have never seen. Reading
> the files is not a peer review; running the pipeline is.

**Guide references:** Module 16, §7 (deliverable, commit, peer review)
**Learning objectives covered:** 7 — peer-review a multi-agent pipeline for role separation, handoff quality, and traceability.

---

## Before you start

- Labs 16.1–16.7 complete: all artifacts 01–05, `traceability.md`, `run_log.jsonl`, human approval recorded
- `<reviewer>` arranged: Team A ↔ Team B (same pairing as Modules 11 and 13)
- Second requirement ready: [`samples/requirements-REQ-2482.md`](samples/requirements-REQ-2482.md) → copy into the **reviewing** team's own checkout (not the peer's repo)
- Sandbox running for the peer run

---

## Step 1 — Self-check the deliverable

| Deliverable item | Evidence | Pass |
|---|---|---|
| Five agent definitions, versioned, each with role / inputs / tools / guardrails / outputs | `.cursor/agents/*.md` | [ ] |
| `PIPELINE.md` + shared handoff rule | repo root + `.cursor/rules/pipeline-handoff.mdc` | [ ] |
| One complete run folder with 01–05 + `traceability.md` + `run_log.jsonl` (+ `results.xml`) | `runs/req-2481-run-01/` | [ ] |
| Executable tests that collect and run, with `req`/`ac`/`seq` markers | `tests/test_req_2481_*.py` + `pytest.ini` | [ ] |
| Human approval recorded, referencing run id and reviewer verdict | approval note / commit trailer | [ ] |

- [ ] All five pass on your own pipeline before anyone else touches it; fix what fails first

---

## Step 2 — Commit

```bash
git status          # expect: requirement-to-test/ (agents, PIPELINE.md, rule, tests, runs/)
git add .
git commit -m "test(REQ-2481): add order-cancellation suite from requirement-to-test pipeline

Run: runs/req-2481-run-01 · Reviewer verdict: ESCALATE (tests approved; DEF-5520 open)
Coverage: AC-1..AC-4 · 6 tests · 5 pass / 1 fail (known product defect)"
git log --oneline -1
```

- [ ] Committed on `module16-lab`; hash `____________`
- [ ] Commit message references the run id and the reviewer verdict (adapt coverage/test counts to your run)
- [ ] Failing test and open defect included in the commit — no cleanup, no `xfail`

---

## Step 3 — Peer run on the second requirement

Swap with Team B. Each team runs the **other team's pipeline**, unchanged, on REQ-2482 — a requirement its
authors have never seen.

- [ ] Copy `REQ-2482.md` into the peer pipeline's `requirements/`; run in a new folder `runs/req-2482-run-01/`
- [ ] Time-box: run at least stages 1–2 in-session; complete the full run if time allows (or take it home and commit the run folder)
- [ ] Record what happened honestly: where it stopped, which statuses, what broke under a new requirement
- [ ] One sentence: did the pipeline prove **reusable** (same agents, new requirement) or over-fitted (agent names/files/ACs baked in from REQ-2481)?

Expected shape (facilitator answer key): validator PASS; ~4–5 tests generated; API Validator flags the
AC-3 unknown-order case (spec: 200 with empty list; sandbox: 404) as a product defect; Reviewer escalates
or approves with the defect acknowledged — but your run's evidence decides, not this paragraph.

---

## Step 4 — Review the peer pipeline against the eight dimensions

| Dimension | Question | Red flag |
|---|---|---|
| **Role separation** | Does each agent stay in its lane? | Validator rewrote an AC; Generator changed the sequence |
| **Least privilege** | Could any agent other than the Generator write files? | Reviewer "fixed" a test directly |
| **Handoff quality** | Could you run stage N using only stage N-1's artifact? | Stage relies on chat history |
| **Independent review** | Did the Reviewer see only the original requirement + tests + report? | Reviewer given generator notes |
| **Traceability** | Pick a random test: can you reach its AC in < 30 s? And the reverse? | Orphan tests or uncovered ACs |
| **Failure honesty** | Are failing tests reported, not hidden? | Assertions changed to match the buggy API |
| **Bounded execution** | Were correction rounds counted and capped? | "Kept asking until it passed" |
| **Granularity** | Does every agent earn its place (Module 15 §5)? | Two stages that could clearly merge |

- [ ] Per-dimension notes with evidence (file + line or artifact), not verdict-only
- [ ] At least one real question asked and answered
- [ ] Review record written by the **reviewer** team into the peer's repo (`shared-agent-library/reviews/` or the peer's run notes), outcome: `approved` / `changes-requested`
- [ ] Changes-requested loop: peer fixes within the day, re-runs the affected stages, and the reviewer confirms

---

## Step 5 — Optional: red-team the flawed run

If your peer run is clean or time remains, review [`samples/flawed-run-excerpt.md`](samples/flawed-run-excerpt.md) with the same eight dimensions.

- [ ] Each planted violation named with its dimension and the concrete consequence
- [ ] Count recorded: `____ of 8 dimensions failed` (facilitator debrief will compare)

---

## Step 6 — Adopt into the shared library

- [ ] Copy the five agent definitions (or the ones you will reuse) into `shared-agent-library/` with `status`, version, and `reviewed-by`/`reviewed-on` recorded
- [ ] Add a library index row for each; note that the run evidence lives in the pipeline repo
- [ ] Keep everything: agent definitions, rule, `PIPELINE.md`, tests, run folders — Modules 17, 18, 19, and the capstone build directly on them

---

## Evidence

- Commit hash + commit message referencing run id and verdict
- Peer-run folder `runs/req-2482-run-01/` (or the time-boxed partial with a note on where it stopped)
- Peer-review record with eight per-dimension notes, a real question, and an outcome — written by the reviewer
- Flawed-run findings (if used)
- Library adoption rows (`AGENTS.md` + assets)

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Reviewer only read files | Peer review treated as a read-through | Run the peer pipeline on REQ-2482; the second run is the review |
| Second run "just uses REQ-2481's artifacts" | Folders confused | New requirement → `requirements/REQ-2482.md`, new run folder, stages read their own artifacts |
| Pipeline fails on the second requirement | Over-fitting (hard-coded req id, AC ids, file names) | That is the finding: parameterize by run/requirement id, re-run, re-review |
| Review has no questions | Reviewing the summary | Open one agent definition and one artifact; ask about a guardrail you cannot verify |
| Commit includes the failing test only after "fixing" it | Failure honesty violation | Revert; the defect stays open and visible in the commit message |
| Nothing adopted into the library | Lab ended at the commit | Adoption is the tenth step of the lifecycle: versioned, reviewed, indexed assets |

---

## Checkpoint questions

1. What does running the peer's pipeline on a second requirement prove that reading it does not?
2. Why does the commit message reference the run id and the reviewer verdict?
3. Why must the failing test be committed, not hidden?

<details>
<summary>Answers</summary>

1. Reusability. A pipeline can look correct on its home requirement and still be over-fitted — hard-coded ACs, file names, or assumptions baked in by running it once. A clean second run on a requirement the authors never saw is the strongest evidence that the agents are real assets, not curiosities.
2. It ties the code to its evidence: the run folder, the artifacts, and the independent verdict. Weeks later, anyone can walk from the commit to how the tests were produced and who judged them — the traceability spine extended to version control.
3. Hiding it (assertion change, `xfail` without a defect link, skip) removes the only artifact that documents a real API defect. The failure is the finding; the suite's honesty is part of the deliverable, and the reviewer escalates the defect to the owner.

</details>

---

## Next

**Module 17 — Quality Gates, Hooks & Self-Correction Fundamentals.** Your manual "send it back" steps and `status` fields become automated PASS/FAIL gates; hooks enforce validation and logging; correction loops get explicit bounds. Keep every artifact — the gates are wired onto this pipeline, tracked by this run log.

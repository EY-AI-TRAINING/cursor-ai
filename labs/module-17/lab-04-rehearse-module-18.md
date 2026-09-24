# Lab 17.4 (Optional, Take-Home) — Rehearse Module 18: Dry-Run All Five Gates

**Module 17 · Quality Gates, Hooks & Self-Correction Fundamentals | Xebia — Cursor AI Training**
Day 5 · Optional extension · ~10 minutes · Individual + peer check

> **Objective:** rehearse Module 18's build by playing the gate engine yourself. Evaluate G1–G5 against
> the Module 16 run's real artifacts, write the gate-log entries the automation will later write, assemble
> the human decision packet, and list exactly what still has to be wired. **This is a rehearsal, not
> Module 18's deliverable.**

**Guide references:** Module 17, §1–§6 applied to the whole gate set
**Learning objectives covered:** 1–6 in rehearsal — the decisions Module 18 automates.

---

## Before you start

- Labs 17.1–17.3 complete: `gates.yaml`, hooks, gate-log schema written
- Your Module 16 run at `runs/req-2481-run-01/` (or use [`samples/failure-scenarios.md`](samples/failure-scenarios.md)'s status snapshot if the run is unavailable)
- Work in `notes/module17/module18-rehearsal.md`; append to `runs/req-2481-run-01/gate_log.jsonl`

---

## Step 1 — Evaluate the five gates by hand

For each gate, check the criteria in `gates.yaml` against the actual artifacts and record the verdict:

| Gate | Artifact(s) checked | Checks that ran | Verdict | Route |
|---|---|---|---|---|
| G1 requirement ready | `01_validated_requirement.md` | | | |
| G2 sequence coverage | `02_test_sequence.json` | | | |
| G3 tests collect & conform | test file + envelope | | | |
| G4 no test defects | `04_api_validation_report.md` | | | |
| G5 review verdict | `05_review_signoff.md` | | | |

- [ ] Every verdict is PASS / FAIL / NEEDS_HUMAN — no "looks fine"
- [ ] G3's round count is taken from `run_log.jsonl` (attempts), and G4's classification of the 403-vs-404 failure is reflected in the route
- [ ] The gate that should have caught the missing refund tests (if any) is named, with the check that failed or the gap in the criteria

---

## Step 2 — Write the gate-log entries

Append one line per gate evaluation to `gate_log.jsonl`, using the schema from Lab 17.3 (version, round, input hash, checks[], routed_to, decided_by).

- [ ] Five gate entries, each with `gates_version`, `input_ref` + hash, and `checks[]`
- [ ] The FAIL or NEEDS_HUMAN entry (if any) names `routed_to` and a reason
- [ ] One `HITL_commit` entry with `decided_by: human:<role>`, `reason`, and an evidence list
- [ ] One sentence: which entries could not have been produced automatically today, and what Module 18 must add to produce them

---

## Step 3 — Assemble the decision packet

Write the packet in `module18-rehearsal.md` as the approver would receive it:

- [ ] Decision needed (APPROVE / REJECT / REQUEST CHANGES)
- [ ] Gate trail (`G1 ✔ G2 ✔ G3 ✔ (round 2) G4 ✔ G5 ESCALATE` — adapted to your run)
- [ ] Coverage + open defect (`DEF-5520`, product defect, test kept failing)
- [ ] Diff scope · risk notes from hooks · cost from `run_log.jsonl` · evidence paths
- [ ] One sentence: what the approver must **not** be shown, and why

---

## Step 4 — List the automation gaps

| What must be automated in Module 18 | Owner (script / hook / CI) | What stays human |
|---|---|---|
| Gate ordering and evaluation | | |
| FAIL → structured findings → producer retry | | |
| Round counters + progress/hash checks | | |
| Downstream reruns by dependency | | |
| Gate-log writing | | |
| Decision-packet assembly | | |

- [ ] Every row filled; the "stays human" column keeps only judgement calls (ambiguity, escalations, commit approval)
- [ ] One sentence: the single biggest risk if the loop's progress check is omitted
- [ ] Peer check: another participant verifies one gate verdict against the artifact and one gate-log entry against the schema

---

## Evidence

- `notes/module17/module18-rehearsal.md` — five-gate table, decision packet, automation-gap table
- `runs/req-2481-run-01/gate_log.jsonl` — five gate entries + one human approval entry
- Peer-check note (what was verified, what was challenged)

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Verdicts are guesses | Checks not run against artifacts | Execute each check (grep for markers, run collect-only, read the 04 report) before recording |
| G4 fails the product defect | Classification ignored | Allowed through, flagged to the reviewer — retrying the generator would be wrong |
| Gate log lacks the human entry | Only machine gates logged | The human checkpoint is a gate too; log identity, reason, and evidence |
| Every gap marked "hook" | Convenience | Scripts, hooks, and CI each own different checks; state which and why |
| Packet is the full diff | Convenience | The packet is the decision context: trail, coverage, defect, scope, risk, cost, evidence |

---

## Checkpoint questions

1. Which gate verdicts should a human see, and which should the pipeline handle alone?
2. Why does the rehearsal write the gate log by hand before Module 18 automates it?
3. What does the automation-gap table tell you to build first?

<details>
<summary>Answers</summary>

1. Humans see NEEDS_HUMAN (ambiguity/control-plane failure), ESCALATE (product defect/policy), and the commit approval. PASS/FAIL routing, retries, and logging are machine work; involving a human in every FAIL causes fatigue.
2. Writing the entries by hand proves the schema is complete and the verdicts are derivable from artifacts before code depends on them — the same "test the contract first" discipline used in earlier labs.
3. The ordering + routing engine and the gate-log writer, because every other behaviour (retries, reruns, packets) hangs off a trustworthy verdict record with counters and hashes.

</details>

---

## Next

**Module 18 — Use Case Lab 4: Self-Correcting Agent Orchestration with Quality Gates** builds exactly this: automated gates on the Lab 3 pipeline, a bounded correction loop, downstream reruns, validation hooks, and a human approval checkpoint with the approval trail as a deliverable. Bring your `gates.yaml`, hooks, gate-log schema, and this rehearsal.

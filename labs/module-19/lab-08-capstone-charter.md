# Lab 19.8 — Capstone Intro: Charter, Roles, Acceptance Criteria

**Xebia — Cursor AI Training | AI-Assisted Software Engineering**
Day 6 · Module 19 · Lab 19.8 of 8 · ~5 min + the 15-minute facilitator intro · Team (3–4 people)

> **Objective:** leave Day 6 with the capstone already started on paper. Map the five roles onto your
> team, trace each acceptance criterion (CA-1…CA-10) to artifacts you already have and the gaps you
> must fill, note the repository layout, baseline yourselves against the evaluation rubric, and name the
> top three risks for Day 7 — before the first line of capstone work.

**Guide reference:** §10 Capstone Project Intro · Module 20 for the build
**Learning objectives covered:** 9 (describe the capstone: workflow, roles, acceptance criteria, repository, rubric)

## Before you start

| Need | Notes |
|---|---|
| Modules 16–19 artifacts | Pipeline, gates, approval, bundle, CI workflow, readiness policy — most of the capstone exists already |
| Team formed | 3–4 people; one person may hold two roles |
| File you will create | `notes/module19/capstone-charter.md` |
| New sandbox ticket | Facilitator-provided on Day 7; do not start it now |

---

## Steps

### Step 1 — Map the five roles onto your team

| Role | Owns | Signs off on | Your name |
|---|---|---|---|
| **Ticket owner / product proxy** | The ticket, clarifications, AC agreement | Requirement bundle and spec ACs | |
| **Pipeline engineer (orchestrator)** | Agents, gates, hooks, reruns, CI workflow | Control-plane changes (as code owner) | |
| **Quality lead** | Test sequence, test quality, validation report, defect classification | HITL sign-off on tests (hash-bound) | |
| **Reviewer / risk owner** | Independent review, security and readiness checks, delegation checklist | Readiness decision | |
| **Report owner** (often combined) | Final engineering report, observability/cost summary, demo | Report completeness | |

- [ ] Every role has a name; no role is "everyone" (that is nobody)
- [ ] The quality lead and the pipeline engineer are different people — the sign-off must not be the author
- [ ] Record who is accountable if the demo is incomplete

### Step 2 — Trace CA-1…CA-10 to what you already have, and the gaps

| # | The package must… | You have it from | Gap to close on Day 7 |
|---|---|---|---|
| CA-1 | Start from a ticket via MCP + schema-valid bundle | Lab 19.2 | New ticket (unseen) |
| CA-2 | Implementation plan with **recorded human approval** before code | (new) | Plan approval checkpoint |
| CA-3 | Spec note whose ACs match bundle AC-IDs one to one | Module 9 SDD + 19.2 | Spec note for the new ticket |
| CA-4 | Test sequence + executable suite, every test marked `req`/`ac` | Module 16 + 18 | Re-run on the new ticket |
| CA-5 | Execution against the sandbox with results + defect classification | Modules 16/18 | — |
| CA-6 | Independent reviewer verdict from a separate context | Module 16 | — |
| CA-7 | Gate logs from ≥1 self-correction round + hash-bound sign-off | Modules 17/18 | Seed or wait for a real round |
| CA-8 | CI pass + readiness report from versioned policy | Labs 19.5–19.6 | Point CI at the new run |
| CA-9 | Final report linking ticket → … → readiness + cost summary | Modules 16/18 + (new) | Report template |
| CA-10 | *(optional)* One delegated task + delegation checklist | Lab 19.7 | Decide if enabled |

- [ ] Each row has a source and either "—" or a concrete gap; no row is blank
- [ ] CA-2 and CA-7 are flagged as the two human checkpoints (plan approval, sign-off) — no approval fatigue beyond them

### Step 3 — Repository, rubric baseline, and risks

- [ ] Note the repository layout the capstone adds (guide §10): `tickets/`, `plans/<ticket>/plan.md` +
      approval, `specs/<ticket>-spec-note.md`, `runs/<run_id>/`, `reports/<ticket>/final_engineering_report.md`,
      `.github/workflows/agent-pipeline.yml`
- [ ] Baseline your team against the rubric — for each criterion, rate **now / Day 7 target**:

| Criterion | Weight | Now | Target |
|---|---|---|---|
| End-to-end traceability | 20% | | |
| Test quality and correctness | 20% | | |
| Gates and self-correction | 15% | | |
| Security and governance | 15% | | |
| Human-in-the-loop design | 10% | | |
| Report quality | 10% | | |
| Observability and cost | 5% | | |
| Demo and peer review | 5% | | |

- [ ] Name the top three risks for Day 7 (e.g. "new ticket's ACs are prose → owner confirmation latency",
      "no real correction round occurs → seed one and record it", "readiness blocked by an unknown
      criterion") with a mitigation each
- [ ] Confirm the demo shape: a 5-minute story from ticket to readiness

---

## Evidence

- `notes/module19/capstone-charter.md` with: five roles named, CA-1…CA-10 source/gap table, repo layout,
  rubric baseline, top three risks with mitigations
- Team agreement recorded (who signs off on what)

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Two roles on one person, including sign-off and author | Small team | At minimum, the quality lead's sign-off must come from someone who did not generate the tests |
| "We'll figure out roles on Day 7" | Charter skipped | Roles are the first thing that wastes time under deadline — decide now |
| CA-8 "CI pass" assumed without a repo | No GitHub sandbox | Use the local simulation from Lab 19.5 and record the simplification in `PIPELINE.md` |
| Rubric baseline all "10/10" | Optimism | Baseline honestly; the target column is what matters |

## Checkpoint questions

<details>
<summary>Why must the quality lead be different from the pipeline engineer?</summary>

The sign-off is a control, not a formality. If the person who built the generator also signs off on its
output, the independent-context principle collapses — the same reason Module 16's reviewer never reads
the generator's reasoning.
</details>

<details>
<summary>Why does the capstone require a recorded plan approval *before* code or tests are generated?</summary>

It is the cheapest checkpoint in the whole workflow: a wrong plan caught before generation saves the
entire run. It also matches the Module 17 HITL rule — approval where the cost of being wrong is high and
the decision is human (intent), not mechanical.
</details>

<details>
<summary>Most of CA-1…CA-10 already exist from Modules 16–19. What is the capstone actually adding?</summary>

A new, unseen ticket end to end — and the report that ties every artifact together for a stakeholder.
The components are built; the capstone proves they compose on first contact with an unknown requirement,
within the team roles and the rubric.
</details>

---

*Next: Module 20 — Use Case Lab 5 (Capstone): End-to-End Ticket-to-Report Engineering Copilot. Bring the charter, the pipeline, and the control plane — Day 7 starts from a new ticket.*

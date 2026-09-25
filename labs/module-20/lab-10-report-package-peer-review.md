# Lab 20.10 — Stages 9–10: Report Package, Package Check, Peer Review and Freeze

**Xebia — Cursor AI Training | AI-Assisted Software Engineering**
Day 7 · Module 20 · Lab 20.10 of 10 · ~35 min (25 build + 10 freeze/peer) · Team (3–4)

> **Objective:** turn the run into the deliverable a stakeholder signs off without asking
> questions: decision first, links not restatements, honest limits — plus the checklist, evidence
> index and cost summary, all passing `package_check.py`. Then swap packages with another team,
> run the four-step review protocol, and freeze what you submitted.

**Guide reference:** §9 Stage 9 — Checklist, Final Engineering Report and Observability/Cost Summary · §10 Deliverable Package, Package Check and Peer Review
**Learning objectives covered:** 8 (traceable report + cost summary), 9 (peer review against the rubric)

## Before you start

| Need | Notes |
|---|---|
| CP5 complete | Readiness report + security + CI/sim evidence |
| Flawed drafts | [`samples/final-report-draft.md`](samples/final-report-draft.md) · [`samples/run-log-draft.jsonl`](samples/run-log-draft.jsonl) · [`samples/gate-log-draft.jsonl`](samples/gate-log-draft.jsonl) |
| Another team | Team A ↔ Team B for the peer review |
| Tools | `package_check.py`, `cost_summary.py`, `evidence_index.py` |

---

## Steps

### Step 1 — Attack the drafts (5 min)

Find the planted problems in the final report draft (six) and in the run/gate log pair (six) and
record them in `notes/capstone/report-review.md`. The log pair is the CA-2/CA-7 test: generation
before approval, a missing plan entry, G4 PASS with failing tests, no LOOP event, an agent
sign-off, and a hash that matches nothing.

### Step 2 — Write the final report (decision first)

`reports/REQ-2502/final_engineering_report.md` — the guide's 15 sections, in order:

| § | Section | Rule |
|---|---|---|
| 1 | Decision requested | The first screen: what is being asked + readiness + known risks |
| 2–8 | Ticket/scope · traceability matrix · plan+approval · spec note · sequence+tests · results+defects · review | Every claim links to the file that produced it |
| 9–11 | Gates/self-correction · security+governance · readiness | Link the logs; label any simulation explicitly |
| 12 | Observability & cost | From `cost_summary.md` + one data-backed improvement idea |
| 13 | Delegated work (optional) | PR link + checklist, or "not run" |
| 14 | Limitations, open issues, risks | Honest: DEF-5561, DEF-5520 sibling, simulations, seeded faults |
| 15 | Sign-off table | Named humans, decision, date |
| A | Evidence index | Path · sha256[:12] · produced by |

- [ ] Every number in the report traces to a log or artifact — if it can't be traced, it doesn't belong
- [ ] Traceability matrix: one row per AC with spec → scenarios → tests → result → defect → review → gate → readiness
- [ ] Limitations list includes anything simulated, seeded, parked or skipped
- [ ] No "see the chat" anywhere

### Step 3 — Checklist, evidence index, cost summary

```bash
python3 tools/cost_summary.py --run req-2502-run-01 --usd-per-mtok 6.0 \
    > reports/REQ-2502/cost_summary.md
python3 tools/evidence_index.py --ticket REQ-2502 --run req-2502-run-01 \
    --out reports/REQ-2502/evidence_index.md
```

- [ ] `checklist.md`: CA-1…CA-10 with evidence links; any FAIL listed **honestly** in report §14
- [ ] Evidence index regenerated **last** — hashes go stale the moment an artifact changes
- [ ] Cost summary: per-stage attempts/tokens/minutes/USD; loops, escalations, human decisions, denies
- [ ] One improvement idea backed by the numbers (e.g. "confirm CL-2 before stage 4 would have avoided round 1")

### Step 4 — Package check and freeze (CP6)

- [ ] `python3 tools/package_check.py` → all required rows PASS (exit 0)
      — a FAIL row listed honestly in §14 still needs the rest of the package complete
- [ ] The checker was **not edited** to go green (it lives under CODEOWNERS; that would fail CA-9 in spirit)
- [ ] Annotated tag on the PR branch: `git tag -a capstone-REQ-2502-v1 -m "Capstone package"`

### Step 5 — Peer review (swap with another team)

| Step | Protocol | Red flag |
|---|---|---|
| 1 | Run `package_check.py` on their package | Checker edited; FAILs unmentioned |
| 2 | One-minute trace test on **two random ACs**: ticket → readiness by links alone, < 60 s | "It's in the chat" / "ask Arjun" |
| 3 | Break-it: change one test, commit | Stale sign-off still accepted; commit guard silent |
| 4 | Score the rubric + **three specific comments** with `file:line` | Generic praise |

- [ ] Review notes written as `notes/capstone/peer-review-<team>.md` (findings, not scores alone)
- [ ] Your package's three comments received and recorded; fix only what time allows — honesty over polish
- [ ] AI-assisted review is welcome as a **reviewer, not a judge**: scores are human decisions

---

## Evidence

- `reports/REQ-2502/` — final report, checklist, readiness, cost summary, security, evidence index
- `notes/capstone/report-review.md` — twelve draft defects (report six + logs six)
- `package_check.py` output (green) and the freeze tag
- Peer-review notes: their findings on yours, yours on theirs

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| CA-9 "missing links" | Report restates instead of linking | Add the artifact paths/links; regenerate the index |
| Evidence hashes all "MISSING" | Index generated before artifacts were written | Regenerate last, after the freeze candidate is complete |
| Package check green, tests meaningless | Floor, not verdict | The peer review and rubric "test quality" line catch it; cite specific tests |
| Break-it doesn't go stale | Sign-off not hash-bound, or guard bypassed | Fix the guard; a stale approval that is accepted invalidates CA-7 |

## Checkpoint questions

<details>
<summary>Why is `package_check.py` "a floor, not a verdict"?</summary>

It checks existence, hashes, sets and ordering. It cannot judge meaning: a test marked `@ac("AC-2")`
that only asserts `status_code != 500` passes every row without proving AC-2. Judgement belongs to
the reviewer, the peer review and the rubric — which is why the script lives under CODEOWNERS and
why editing it to go green fails CA-9 in spirit.
</details>

<details>
<summary>What makes the final report trustworthy to a stranger?</summary>

Three properties: decision first (what is being asked, readiness, known risks), links not
restatements (every number resolves to the artifact that produced it), and honesty about limits
(simulated, seeded, parked, skipped). Reviewers reward candour and penalise surprises.
</details>

---

*Next: Day 8 — peer/AI-assisted review (45 min) and team demos (75 min), then Module 21 — Best Practices, Enterprise Rollout & ROI, where your cost summary and failure modes become the evidence for adoption.*

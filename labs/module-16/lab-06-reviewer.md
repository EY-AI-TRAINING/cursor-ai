# Lab 16.6 — Build the Reviewer: Fresh Context, One Verdict

**Module 16 · Use Case Lab 3: Multi-Agent Requirement-to-Test Automation | Xebia — Cursor AI Training**
Day 5 · Lab 6 of 8 · ~15 minutes · Individual or pairs

> **Objective:** build the independent-context stage. The Reviewer receives the **original requirement**
> (with the owner's clarification), the tests, and the API validation report — never the Generator's
> reasoning or the upstream chat. It judges the suite against the source of truth and returns one
> verdict: **APPROVE**, **REQUEST_CHANGES**, or **ESCALATE**.

**Guide references:** Module 16, §5 (Reviewer — independent review and sign-off)
**Learning objectives covered:** 5 — chain the Reviewer for independent sign-off; 7 — peer-review discipline is rehearsed here.

---

## Before you start

- Lab 16.5 complete: `04_api_validation_report.md` written; product defect flagged and test unchanged
- Write your definition in `<pipeline-root>/.cursor/agents/reviewer.md`
- Start a **fresh chat / fresh subagent** — this is the isolation boundary, not a formality

---

## Step 1 — Write the agent definition

- [ ] **Role** — independently judges the suite against the original requirement; reports, never edits
- [ ] **Inputs (exactly three)** — `requirements/REQ-2481.md` (**original**, including the owner's clarification), `tests/test_req_2481_*.py`, `runs/<run_id>/04_api_validation_report.md`
- [ ] **Must NOT receive** — artifacts 01–03, the generator's summary or reasoning, chat history, prior verdicts
- [ ] **Tools** — read + run tests; the only write is `runs/<run_id>/05_review_signoff.md`
- [ ] **Verdicts** — `APPROVE` (all ACs covered, tests correct, open defects acknowledged); `REQUEST_CHANGES` (specific findings, each tied to AC-ID or test); `ESCALATE` (product defect, requirement conflict, out-of-scope concern)
- [ ] **Embedded checklist**:
  - [ ] **Coverage:** every AC-ID in the *original* requirement has ≥1 test with a matching `ac` marker
  - [ ] **Correctness:** assertions match the AC wording, not only the sequence wording
  - [ ] **Negative paths:** error ACs assert both the error response and the unchanged state
  - [ ] **Independence:** no test depends on execution order or shared mutable state
  - [ ] **Hygiene:** no secrets, hard-coded URLs, sleeps, or disabled assertions
  - [ ] **Honesty:** known failures are reported, not skipped or `xfail`-ed without a linked defect
  - [ ] **Traceability:** `traceability.md` is complete and consistent with the markers

---

## Step 2 — Prove the isolation

In your run notes, record exactly what crossed the boundary:

```text
IN  → requirements/REQ-2481.md (original) · tests/test_req_2481_*.py · 04_api_validation_report.md
EXCLUDED → 01_validated_requirement.md · 02_test_sequence.json · 03_generation_notes.md ·
           generator chat/reasoning · previous attempts
```

- [ ] The prompt for the review names the three inputs and explicitly excludes the rest
- [ ] The reviewer did not ask for (or get given) the Generator's explanation — if your tooling cannot prevent it, state in the run notes how you would enforce it (fresh subagent, new chat, file-scoped prompt)
- [ ] One sentence: why the guide calls this the difference between review and **anchoring**

---

## Step 3 — Apply the checklist and record the verdict

- [ ] Per-AC coverage is taken from the **original** requirement: `AC-1 ✔ (2 tests) · AC-2 ✔ · AC-3 ✔ (failing — product defect) · AC-4 ✔`
- [ ] Findings: none on test quality (expected); the AC-3 403-vs-404 case is an open **product defect**, not a test finding
- [ ] Verdict recorded — expected: **ESCALATE** (tests approved; 1 open product defect) — or APPROVE if your run has no open defect; either must be justified by the checklist
- [ ] `05_review_signoff.md` contains: verdict, reviewer version, run id, coverage line, findings, escalation/recommendation (e.g., commit tests, raise `DEF-5520`, keep the test failing)
- [ ] Envelope carries `status` (map `ESCALATE` → `NEEDS_HUMAN` for routing) and `ac_ids_covered`
- [ ] `run_log.jsonl` — reviewer line

---

## Step 4 — If the verdict is REQUEST_CHANGES

- [ ] Route findings back to the Test Generator with the specific AC-ID/test/fix hint — this is a **manual correction round**, counted (max 2)
- [ ] Re-run only the affected downstream stages (Generator → API Validator → Reviewer) — upstream artifacts 01–02 are unchanged, so they are reused
- [ ] Re-review in a fresh context; the new verdict supersedes the old one and is logged as a new attempt

---

## Evidence

- `.cursor/agents/reviewer.md` — five slots, three inputs, must-nots, embedded checklist
- `runs/req-2481-run-01/05_review_signoff.md` — verdict + coverage + findings + escalation
- Isolation note: what was passed, what was excluded, how exclusion was enforced
- `run_log.jsonl` — reviewer line (and any correction-round attempts)

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Reviewer approves everything | It received the generator's notes | Start a genuinely fresh chat; pass only the three inputs |
| Verdict with no per-AC coverage | Checklist skimmed | Coverage must be computed against the **original** requirement, AC by AC |
| Reviewer "fixes" a failing test | Role violation | Reviewers report; the Generator fixes. Revert the edit and issue a finding |
| Reviewer requests changes for the product defect | Misclassification | Product defects are escalated, not routed to the Generator — the test is correct |
| Verdict contradicts the checklist | Checklist present but not applied | Every verdict line must be traceable to checklist evidence |
| `traceability.md` not yet written | Sequencing | It is Lab 16.7's artifact; the reviewer flags its absence as a **traceability** finding and relies on markers for the verdict |

---

## Checkpoint questions

1. Why does the Reviewer read the original requirement while the Builder reads the validated one?
2. What is anchoring, and how does context isolation prevent it?
3. Why does the Reviewer report a bug in a test instead of fixing it?

<details>
<summary>Answers</summary>

1. The Builder works from the checked, clarified source to design against resolved facts; the Reviewer works from the **source of truth** so that any drift introduced by stages 1–3 is caught rather than inherited. If the reviewer only saw the Builder's interpretation, an early error could pass every gate unnoticed.
2. Anchoring is the bias to agree with a justification once you have read it. A reviewer that sees the generator's reasoning tends to approve it. Isolation — artifact + original criteria only — forces an independent judgement against the requirement.
3. Separation of duties: one writer (the Generator) means the path of every change is clear and reviewable. The Reviewer issues a finding tied to an AC-ID/test; the Generator makes the change; the downstream stages re-run.

</details>

---

## Next

**Lab 16.7 — Close the Loop: Traceability, Run Log & Human Approval.** All five stages exist. Now make the run walkable in both directions — AC ↔ scenario ↔ test ↔ result — and put the evidence a human needs to approve the commit.

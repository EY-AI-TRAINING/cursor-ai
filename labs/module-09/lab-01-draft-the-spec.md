# Lab 9.1 — The Spec: Durability & Testability

**Module 9 · AI-Assisted Design & Spec-Driven Development (SDD) | Xebia — Cursor AI Training**
Day 3 · Lab 1 of 3 · ~20–25 minutes · Individual + peer/facilitator approval

> **Objective:** decide the right level of rigor for the task, ground the requirement in the actual repository,
> and write a one-page spec whose acceptance criteria can unambiguously pass or fail — then get it approved
> before a single line of implementation exists. The approval gate is the point of the lab.

**Guide references:** Module 9, §1 (spec as durable source of truth), §3 (rigor spectrum), §4 (exploring requirements), §7 (spec vs prompt; testable acceptance criteria; approval)
**Learning objectives covered:** 1 — spec as source of truth; 3 — choose the right rigor; 4 — explore requirements; 7 — testable criteria + approval.

---

## Before you start

- Modules 3–8 complete; Module 8 starter kit committed. Create your branch:

  ```bash
  git switch -c module9-lab
  ```

- Take the facilitator's seeded `<feature>` — a raw ticket for a small slice (one endpoint, one behavior, one thin
  vertical). If choosing your own, keep the first pass implementable in ~15 minutes of agent work.
- Know your `<approver>` (a peer or the facilitator) and your `<test-command>`.
- Keep all artifacts under `specs/<feature>/`; the spec path is `<spec-file>` = `specs/<feature>/spec.md`.

---

## Step 0 — Choose the rigor point (30 seconds, deliberately)

SDD is the high-rigor end of a spectrum, not a universal default. Record where `<feature>` sits and why:

| Approach | Durable artifact? | Traceability | Best fit (guide §3) |
|---|---|---|---|
| Vibe-coding | None | None | Throwaway prototypes, spikes |
| Prompt-driven (Modules 5–7) | Ephemeral prompt | Weak | Small, well-scoped, single-session tasks |
| **SDD** | **Versioned, reviewed spec** | **Clause ↔ code ↔ test links** | **Production features, multi-session/multi-agent work, anything audited** |

- [ ] Rigor chosen and justified in one sentence: `____________`
- [ ] Also name one nearby task that would *not* warrant SDD (keeps the judgment honest): `____________`

---

## Step 1 — Explore before drafting (Ask mode, no edits)

A spec written from the ticket text alone will contradict the codebase. Ground it first, using Module 4's Ask mode:

1. In **Ask mode** (not Agent mode — no edits before approval), ask the repo:
   - "Where does similar behavior already live in this codebase? Cite files."
   - "What conventions from `.cursor/rules/` and `AGENTS.md` apply to `<feature>`?"
   - "What existing code must `<feature>` integrate with, and what does its interface look like?"
2. Capture 5–8 grounding bullets **with file references** into `specs/<feature>/notes.md`.

- [ ] Grounding notes saved, with real file paths
- [ ] At least one ambiguity or assumption surfaced that the spec must resolve or explicitly defer

---

## Step 2 — Draft the spec

Create `<spec-file>` from this structure (adapt section names if your team has a template):

```markdown
# Spec: <feature>
**Version:** 0.1 (draft) · **Status:** Draft · **Owner:** <you> · **Date:** YYYY-MM-DD
**Source:** <ticket ID/link or one-line raw requirement>

## 1. Purpose & scope
<2–3 sentences: what the feature does, for whom, and the boundary of this spec>

## 2. Acceptance criteria (testable)
| ID | Criterion (observable, unambiguous) | Verification |
|----|-------------------------------------|--------------|
| AC-1 | ... | automated test / manual check |
| AC-2 | ... | ... |

## 3. Non-functional constraints
- <e.g., no secrets in logs; p95 response < 2s; rate limit 5 req/min/IP>

## 4. Explicit exclusions (out of scope for this spec)
- <e.g., SSO-based flow, bulk import, UI redesign>

## 5. Open questions
- [ ] <question> — owner / due

## Change log
| Version | Date | Change | Author |
|---------|------|--------|--------|
| 0.1 | | Initial draft | |
```

Rules that make this a spec rather than a wish list:

- **Observable, not adjectival.** "`POST /<endpoint>` returns 202 within 2s for a valid request; returns 400 with
  error code `X-004` for an invalid one" — never "should be fast and user-friendly".
- **IDs are mandatory.** `AC-1`, `AC-2`, … are the handles Lab 9.3's traceability matrix and Module 11's agents use.
- **4–7 criteria.** More means the slice is too big; split it or move criteria to an explicit exclusion.
- **Every criterion names its verification** — the test or manual check that will decide pass/fail.
- **Non-functional constraints and exclusions are part of the spec**, not an afterthought (guide §7).

- [ ] `<spec-file>` created with version, status, owner, and scope
- [ ] Every acceptance criterion is testable, numbered, and names a verification method
- [ ] At least one NFR constraint and at least one explicit exclusion recorded

---

## Step 3 — The testability pass (rescue a weak criterion)

Swap specs with a partner (or give yours to Cursor with: "Review this spec against Module 9 §7 — for each
criterion, say whether a test could unambiguously pass/fail. Flag anything that belongs in a prompt instead.").

1. Pick the weakest criterion and rewrite it.

   > **Before:** "Password reset should work reliably for all users."
   > **After:** "`POST /reset-password` returns 202 within 2s for a valid email; returns 400 with `AUTH-004` for
   > an invalid one; no more than 5 requests/min/IP."

2. Log the **spec vs prompt split** — ideas that surfaced while drafting but don't belong in the spec:

   | Item that came up | Spec (durable, testable) or prompt (this session only)? | Why |
   |---|---|---|
   | e.g., "do the API layer before the email integration" | Prompt | Sequencing instruction for this implementation, not a permanent requirement |
   | e.g., "no plaintext tokens in logs" | Spec | Stays true for every implementation; independently checkable |
   | | | |

- [ ] Weakest criterion rewritten (before/after captured)
- [ ] At least two spec-vs-prompt decisions logged with the durability/testability test applied
- [ ] Partner or agent review confirmed no untestable criteria remain

---

## Step 4 — The human approval gate (still zero code)

1. Submit spec `v0.x` to `<approver>` with a three-line summary and **two explicit questions**, e.g.:
   > "Is AC-3 observable as written? Is anything missing from the exclusions that you'd expect to be in scope?"
2. Approver checks: scope bounded · criteria testable · exclusions explicit · verification named.
3. On approval:
   - Set the header to `Version: 1.0 · Status: Approved`, record approver + date.
   - Add the change-log row.
4. On revision requested: capture the feedback, revise, bump `v0.2`, re-submit — log the cycle.

Then prove the gate held:

```bash
git status        # expect: spec + notes files only — ZERO source code changes
git add specs/
git commit -m "Module 9 lab: approve spec v1.0 for <feature>"
git log --oneline -1
```

- [ ] Approved spec v1.0 with approver and date recorded
- [ ] Revision cycle logged if approval wasn't immediate
- [ ] `git status` confirmed no source changes before approval; commit hash `____________`

---

## Evidence

- `spec.md` (approved v1.0) + `notes.md` grounding notes
- Weak-criterion before/after
- Spec-vs-prompt split table
- Approval record + `git status` output + commit hash

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Spec reads like a design document | You're writing *how*, not *what* | Move mechanism into Lab 9.2/plan; keep the spec to observable behavior |
| Criteria can't fail | Not testable — "should be fast" | Name an observable threshold or tool: "returns 202 within 2s; `pytest` case passes" |
| 15+ criteria | Scope too big | Split the feature; keep one thin slice; move the rest to exclusions or a future spec |
| Approval becomes a rubber stamp | Reviewer wasn't asked a real question | Ask "Is AC-3 ambiguous? What's missing from exclusions?" — require an answer |
| Agent starts editing during Step 1 | You were in Agent mode | Exploration is Ask mode; no edits before spec approval (ground rule 2) |
| Not sure something is durable enough for the spec | Mixing sequencing with requirements | Apply the test: stays true across every future implementation **and** independently checkable → spec; otherwise prompt |

---

## Checkpoint questions

1. What's the practical test for deciding whether an instruction belongs in the spec or in a one-off prompt?
2. Why does every acceptance criterion need an ID?
3. Why is human approval placed *before* implementation, rather than only at final code review?

<details>
<summary>Answers</summary>

1. If it must remain true across every future implementation and can be independently checked, it belongs in the spec. If it's a one-time instruction about how to do the work in this session, it belongs in the prompt.
2. The ID is the traceability handle: code and tests reference it, and the Lab 9.3 matrix (and later Module 11/16/20 pipelines) can mechanically answer "what satisfies AC-3?" and "why does this code exist?"
3. Because correcting a misunderstanding in a document is far cheaper than correcting generated code and tests built on top of a flawed spec — the "catch it early" logic Module 17 later automates as a quality gate.

</details>

---

## Next

**Lab 9.2** — turn the approved spec into the first *how* artifacts: a Mermaid architecture diagram, an interface contract, and one ADR.

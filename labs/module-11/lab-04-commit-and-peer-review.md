# Lab 11.4 — Commit and Peer Review

**Module 11 · Use Case Lab 1: Reusable Agents, Prompts & Skills Framework | Xebia — Cursor AI Training**
Day 3 · Lab 4 of 4 · ~15 minutes · Team A ↔ Team B peer review

> **Objective:** finish the lifecycle the course has used since Module 8 — draft → test → **peer review** →
> commit → adopt. Commit and tag the library, then review another team's library against the six-check rubric,
> with real questions and a recorded outcome. Nothing is "done" until a peer says so.

**Guide references:** Module 11, §6 (deliverable, commit, peer review); Module 8 §7 (lifecycle)
**Learning objectives covered:** 6 — commit the library and participate in peer review against a consistent rubric.

---

## Before you start

- Lab 11.3 complete: all assets tested, final matrix in `shared-agent-library/testing/pass-fail-matrix.md`
- `<reviewer>` arranged — another team/participant (Team B) reviews your library; you review theirs
- Working tree clean enough to review: `git status` shows only intended library changes

---

## Step 1 — Pre-commit self-check

Run the guide's six-check rubric on yourself before anyone else does:

| Check | Question | Evidence in your library |
|---|---|---|
| Completeness | All four agents, their templates, and the one subagent present and named clearly? | `AGENTS.md` index |
| Anatomy | Every agent specifies role, inputs, tools, guardrails, outputs (Module 10 §2)? | `agents/*.agent.md` |
| Testability | Evidence each asset ran against a sample input and matched its contract? | `testing/pass-fail-matrix.md` + transcripts |
| Scope discipline | Is the subagent's independence justified? | `subagents/*.subagent.md` + justification sentence |
| Library hygiene | Rules/skills at the right level; one canonical + one load location documented? | `AGENTS.md` sync note |
| Version control | Everything committed with a message a future reader understands? | Step 2 |

- [ ] All six checks pass on your own library; anything failing is fixed **before** requesting review

---

## Step 2 — Commit and tag

```bash
git status                       # expect: shared-agent-library/ (+ .cursor/ if you updated active copies)
git add shared-agent-library/ .cursor/
git commit -m "Module 11 lab: shared agent/skill library (4 agents, templates, subagent, rules+skills)"
git tag v0.1.0
git log --oneline -1 && git tag --list 'v0.1.*'
```

- [ ] Committed on `module11-lab`; hash `____________`
- [ ] Tagged `v0.1.0` (per the deck — the tag is what Module 13 and future teammates pin against)
- [ ] If your cohort uses one shared repo: pushed to the shared remote / opened a PR per facilitator instructions

---

## Step 3 — Peer review exchange (Team A ↔ Team B)

Reviewer instructions: read the library **cold** — start at `AGENTS.md`, then open assets. Ask at least one real question; no rubber stamps.

- [ ] Reviewer runs the six-check rubric against the other team's library
- [ ] Reviewer opens at least one definition and one transcript, and **re-runs one asset** if the runner is available (spot-check the claimed PASS)
- [ ] Reviewer records the review in `shared-agent-library/reviews/v0.1.0-review.md`:

```markdown
# Peer review — v0.1.0
reviewer: <name/team> · date: <date> · outcome: approved | changes-requested
## Checklist
- completeness: pass/fail — note
- anatomy: pass/fail — note
- testability: pass/fail — note (which transcript was spot-checked)
- scope discipline: pass/fail — note
- library hygiene: pass/fail — note
- version control: pass/fail — note
## Questions asked + author's answers
## Required changes (if any)
```

- [ ] Review record committed by the **reviewer** (not the author) — the review is part of the deliverable

---

## Step 4 — Changes-requested loop (if any)

- [ ] For each required change: fix the asset, **re-test the affected asset** (Lab 11.3 discipline — a fix without a re-run isn't verified), and note the version bump
- [ ] If fixes changed the reviewed artifact, tag the fix commit `v0.1.1` and note that it supersedes `v0.1.0`
- [ ] Re-request review only for the changed assets; reviewer confirms and updates the outcome to `approved`

---

## Step 5 — Adopt

- [ ] For each approved asset: frontmatter `status: adopted`, `version: 1.0.0`, `reviewed-by: <reviewer>`, `reviewed-on: <date>`
- [ ] Update `AGENTS.md` index to match (version/status/reviewer)
- [ ] Final commit:

```bash
git add shared-agent-library/
git commit -m "Module 11 lab: adopt library v1.0.0 after peer review"
git log --oneline -3
```

- [ ] Library and evidence intact for Module 13 (knowledge grounding), Module 16 (chaining), Module 18, and the Module 20 capstone — do not clean up the branch

---

## Evidence

- Self-check + peer review record (`reviews/v0.1.0-review.md`) with reviewer name, checklist, questions, outcome
- Commit hash + tag(s) `v0.1.0` (and `v0.1.1` if changes were requested)
- Adopted assets at `1.0.0` with `reviewed-by`/`reviewed-on` recorded
- Updated library index

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Reviewer has no questions | Review done from the summary, not the files | Open `AGENTS.md` → one agent → one transcript; re-run one asset; ask about a guardrail you can't verify |
| Review is a rubber stamp | Outcome not recorded with specifics | Require per-check notes and the spot-checked transcript in the review record |
| Changes requested but no re-test | Fix treated as self-evident | Re-run the affected asset and attach the new transcript; update the version |
| Tag placed after adoption | Sequencing slip | The deck's tag `v0.1.0` marks the reviewed release; keep it at the commit that was reviewed (or `v0.1.1` after fixes) |
| Author edits the review record | Wrong ownership | The reviewer writes and commits the review; authors respond in the PR/thread |
| Version numbers inconsistent across assets | Manual drift | Bump only changed assets; keep the index authoritative and regenerate it from the files |

---

## Checkpoint questions

1. What does peer review add that self-review doesn't?
2. Why does the tag matter as much as the commit?
3. When a reviewer requests a change, what has to happen before the asset is adopted?

<details>
<summary>Answers</summary>

1. A second reviewer checks the library against a consistent, shared rubric and catches what the author is too close to see — the same benefit code review provides. It also produces an auditable record.
2. The tag is the pinned, named release that Module 13, future labs, and other teams reference — it says *this* reviewed state is what gets reused, not whatever the branch happens to contain later.
3. The asset is fixed, **re-tested** against its sample input (evidence attached), version-bumped, re-reviewed only for what changed, and only then marked adopted with `reviewed-by`/`reviewed-on` recorded.

</details>

---

## Next

**Module 12 — Context Engineering, Knowledge Grounding & MCP** opens Day 4: the library you just adopted learns to ground its answers in repository code, SRS/SDS documents, standards, and enterprise knowledge sources. **Module 13 (Use Case Lab 2)** connects this library to a knowledge source — pin it against your `v0.1.0` tag.

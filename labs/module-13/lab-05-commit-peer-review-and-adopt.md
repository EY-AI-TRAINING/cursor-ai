# Lab 13.5 — Commit, Peer Review, and Adopt

**Module 13 · Use Case Lab 2: Knowledge-Grounded Engineering Agent | Xebia — Cursor AI Training**
Day 4 · Lab 5 of 5 · ~15 minutes · Team A ↔ Team B peer review

> **Objective:** do guide §5 — finish the lifecycle: self-check the six review criteria, commit and tag, have
> another team try to break the grounding, run the changes-requested loop if needed, and adopt the agent into
> Module 11's shared library with `reviewed-by`/`reviewed-on` recorded. Nothing is done until a peer says so.

**Guide references:** Module 13, §5 (deliverable, commit, peer review); Module 11 §6 (lifecycle and adoption)
**Learning objectives covered:** 6 — produce, test, and peer-review a committed, reusable grounded agent.

---

## Before you start

- Lab 13.4 complete: stress matrix with all categories, FAILs diagnosed and re-run, agent at `0.2.0`
- `<reviewer>` arranged — Team A ↔ Team B, same pairing as Module 11 (swap libraries again)
- Working tree reviewable: `git status` shows only intended changes

---

## Step 1 — Pre-commit self-check (the reviewer's six criteria, applied to yourself)

| Criterion | Question | Evidence in your library |
|---|---|---|
| **Connection correctness** | All five source categories actually reachable — not just configured-looking? | `testing/source-reachability.md` with retrieval evidence |
| **Scoping** | Retrieval returns relevant material, not whole-document dumps? | `retrieval-scope.yaml` + ST-1 scoped-vs-dumped note |
| **Citation format** | Every factual claim in sample outputs has a specific, checkable source? | Stress transcripts with citations spot-checked |
| **Guardrail enforcement** | The rule loads automatically — not manually re-stated? | Enforcement transcript from Lab 13.3 |
| **Refusal test coverage** | At least one case per category from guide §4? | Stress matrix: ST-1…ST-6 + your own ST-7 |
| **Library hygiene** | Committed to the shared structure, documented for reuse? | `AGENTS.md` index rows + sync direction |

- [ ] All six pass on your own agent; fix anything failing **before** requesting review

---

## Step 2 — Commit and tag

```bash
git status                       # expect: shared-agent-library/, .cursor/, knowledge/
git add shared-agent-library/ .cursor/ knowledge/
git commit -m "Module 13 lab: knowledge-grounded agent (sources, scope, guardrail rule, stress test)"
git tag v0.2.0
git log --oneline -1 && git tag --list 'v0.*'
```

- [ ] Committed on `module13-lab`; hash `____________`
- [ ] Tagged `v0.2.0` — Module 11 released `v0.1.0`; this release adds the grounded agent (if review changes the artifact, the fix commit gets `v0.2.1`)
- [ ] No secrets in any committed file; `.cursor/mcp.json` is secret-free (or excluded)

---

## Step 3 — Peer review exchange (Team A ↔ Team B)

Reviewer instructions: read the agent **cold** — start at `AGENTS.md`, then the agent definition, the scope contract, the rule, and the stress matrix. Ask at least one real question; no rubber stamps.

- [ ] Reviewer runs the six criteria against the other team's agent
- [ ] Reviewer opens at least one transcript and **re-runs one stress question** (ideally ST-3 or ST-4) to spot-check the claimed PASS — with the rule not restated
- [ ] Reviewer records the review in `shared-agent-library/reviews/v0.2.0-review.md`:

```markdown
# Peer review — v0.2.0 (knowledge-grounded agent)
reviewer: <name/team> · date: <date> · outcome: approved | changes-requested
## Checklist
- connection correctness: pass/fail — note (which source was re-verified)
- scoping: pass/fail — note (what was retrieved for the re-run)
- citation format: pass/fail — note (which citation was spot-checked)
- guardrail enforcement: pass/fail — note (was the rule restated? no)
- refusal test coverage: pass/fail — note (which question was re-run, result)
- library hygiene: pass/fail — note
## Questions asked + author's answers
## Required changes (if any)
```

- [ ] Review record committed by the **reviewer** (not the author) — the review is part of the deliverable
- [ ] If the re-run disagreed with the author's claimed PASS, record both runs (nondeterminism is a finding, not a verdict)

---

## Step 4 — Changes-requested loop (if any)

- [ ] For each required change: fix the agent, rule, or scope; **re-run the affected question**; note the version bump
- [ ] If fixes changed the reviewed artifact, tag the fix commit `v0.2.1` and note it supersedes `v0.2.0`
- [ ] Re-request review only for what changed; reviewer confirms and updates the outcome to `approved`

---

## Step 5 — Adopt

- [ ] Agent frontmatter: `status: adopted`, `version: 1.0.0`, `reviewed-by: <reviewer>`, `reviewed-on: <date>`
- [ ] Update `shared-agent-library/AGENTS.md` to match (version/status/reviewer/load location)
- [ ] Final commit:

```bash
git add shared-agent-library/
git commit -m "Module 13 lab: adopt knowledge-grounded agent v1.0.0 after peer review"
git log --oneline -3
```

- [ ] Library, corpus, rule, scope contract, stress evidence, and review record intact for Module 14 (governance), Module 16 (pipeline), and the Module 20 capstone — do not clean up the branch

---

## Evidence

- Self-check table + reviewer-authored `reviews/v0.2.0-review.md` (six checks, a re-run question, questions asked, outcome)
- Commit hash + tag(s) `v0.2.0` (and `v0.2.1` if changes were requested)
- Adopted agent at `1.0.0` with `reviewed-by`/`reviewed-on`; updated `AGENTS.md` index

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Reviewer has no questions | Review done from the summary, not the artifacts | Open `AGENTS.md` → agent → scope → rule → one transcript; re-run ST-3 or ST-4 |
| Reviewer's re-run fails where author's passed | Nondeterminism, or the rule didn't load in their session | Record both runs; confirm the rule is in `.cursor/rules/` with activating frontmatter; if behavior differs, it's a finding — tighten the rule wording |
| Review is a rubber stamp | Outcome recorded without specifics | Require per-check notes, the spot-checked citation, and the re-run result |
| Changes requested but no re-test | Fix treated as self-evident | Re-run the affected question in a fresh chat; attach the transcript; bump the version |
| Author wrote the review record | Wrong ownership | The reviewer writes and commits it; authors respond in the PR/thread |
| Tag placed after adoption | Sequencing slip | `v0.2.0` marks the reviewed release; keep it at the reviewed commit (or `v0.2.1` after fixes) |
| Version numbers disagree across files | Manual drift | Bump only changed assets; `AGENTS.md` is authoritative |

---

## Checkpoint questions

1. What does peer review add for a grounded agent specifically, beyond code-review habits?
2. Why must the reviewer re-run a stress question instead of reading the author's transcript?
3. What makes the refusal behavior trustworthy to another team?

<details>
<summary>Answers</summary>

1. It independently verifies the two things an author is least able to judge about their own grounding: whether the sources were truly reachable/scoped (not just configured), and whether refusal actually triggers when pushed — the agent's silence is as much a deliverable as its answers.
2. A transcript is the author's claimed evidence, and nondeterminism is real: the reviewer's fresh run is the independent reproduction. If it differs, that difference is itself a finding about rule robustness or scoping.
3. It's demonstrable and reproducible: the rule loads automatically (not restated), the stress set covers all four categories, a peer re-ran a question and saw the same behavior, and the review record is committed. Trust comes from verified behavior, not from documentation claiming it.

</details>

---

## Next

**Module 14 — Governance, Security & Observability** closes Day 4: who can grant this agent access to repository, document, and knowledge sources; what gets logged at each handoff; how secrets are handled; and what the whole pipeline costs to run. Your scope contract and MCP config become the policy artifacts it governs.

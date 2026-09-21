# Lab 13.3 — Enforce the Guardrail as a Rule

**Module 13 · Use Case Lab 2: Knowledge-Grounded Engineering Agent | Xebia — Cursor AI Training**
Day 4 · Lab 3 of 5 · ~15 minutes · Individual or pairs

> **Objective:** do guide §3 — implement "no unsupported facts" the way Module 8 taught any standing behavior:
> as a **Project Rule** (canonical in the library, loaded from `.cursor/rules/`), not something re-typed into
> each conversation. Then prove it holds automatically — refusal phrase included — with the rule never restated.

**Guide references:** Module 13, §3 (rules/skills constrain behavior); Module 12 §6 (no-unsupported-facts); Module 8 §6 (rules/skills); Module 11 §3 (canonical vs. load location)
**Learning objectives covered:** 4 — constrain behavior with a standing rule/skill guardrail.

---

## Before you start

- Lab 13.2 complete: `agents/knowledge-grounded.retrieval-scope.yaml` written; ST-1 run and recorded
- Module 12's `.cursor/rules/grounding-discipline.mdc` still on the branch
- Open [`samples/grounding-stress-questions.md`](samples/grounding-stress-questions.md) — ST-3 is the enforcement probe

---

## Step 1 — Promote the rule into the library

Module 12's rule was a first cut; this lab makes it the agent's **standing guardrail** with one canonical home and one load location (Module 11 §3).

- [ ] Canonical: `shared-agent-library/rules/grounded-agent.mdc` (adapted from `grounding-discipline.mdc`)
- [ ] Loaded: `<sandbox-repo>/.cursor/rules/grounded-agent.mdc`
- [ ] Sync direction documented in `shared-agent-library/AGENTS.md`: library is source of truth → copy into `.cursor/rules/` (and note the copy step)
- [ ] Remove or fold the old `grounding-discipline.mdc` so there is exactly one grounding rule active

Frontmatter (deck §03: "reviewed and versioned like code"):

```markdown
---
description: Grounding guardrail — citation, refusal, and scope discipline for grounded answers
alwaysApply: true
version: 0.1.0-draft
---
```

If your cohort prefers description-based activation over `alwaysApply`, pick one and say in `AGENTS.md` how it is verified to load.

---

## Step 2 — Write the enforceable clauses

Keep it short — a rule, not an essay. Every clause must prevent a named failure:

```markdown
# Grounding guardrail

- Every factual claim cites its source using the format in `agents/knowledge-grounded.retrieval-scope.yaml`
  (`path › section` for docs, `path:line` for code, `DEF-###` for defects).
- Never speculate beyond retrieved context — no filling gaps from general knowledge.
- When nothing in scope supports a claim, respond with the standard refusal phrase:
  "Not found in the provided sources."
- Never present a related fact as the answer to a different question (e.g., operational log retention
  is not a compliance policy).
- Retrieve only from the paths and collections allowed by the retrieval-scope contract.
- Read-only: never edit sources, specs, fixtures, or the corpus.
```

- [ ] Citation clause names the exact format (checkable)
- [ ] Refusal phrase is exact and quoted (so it can be asserted, not interpreted)
- [ ] No related-fact substitution clause present (Module 12's trap, carried forward)
- [ ] Scope clause points at the contract file
- [ ] Rule versioned; no clause is a platitude ("be accurate")

---

## Step 3 — Enforcement test: prove it loads, don't restate it

The review criterion is "the rule is loaded automatically, not manually re-stated." So test it that way.

- [ ] Fresh chat. Do **not** paste or restate the rule. Ask **ST-3** (*"What is the platform team's Q3 roadmap for gateway limits?"*)
- [ ] Response contains the standard refusal phrase; record the transcript as enforcement evidence
- [ ] Fresh chat. Ask **ST-1**; response carries the declared citation format
- [ ] Note in the matrix that neither prompt mentioned the rule — the behavior came from the loaded rule

If the phrase does **not** appear:

- [ ] Diagnose: rule missing from `.cursor/rules/`? frontmatter not activating? wording ambiguous? Fix and re-run
- [ ] Record the failed run and the fixed run (both are evidence of the Module 8 lifecycle: refine rule, retest)

---

## Evidence

- `shared-agent-library/rules/grounded-agent.mdc` (canonical) + `.cursor/rules/grounded-agent.mdc` (loaded)
- `shared-agent-library/AGENTS.md` — sync direction + rule row (version/status/load location)
- Enforcement transcripts: ST-3 refusal with rule not restated; ST-1 with citation format
- Matrix rows for both runs

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Rule works only when pasted into the prompt | It isn't loaded from `.cursor/rules/` | Put the copy in `.cursor/rules/` with activating frontmatter; re-run without pasting |
| Refusal is paraphrased, not the phrase | Phrase not quoted or not mandatory | Quote it exactly in the rule; add "respond with the standard refusal phrase" |
| Rule never triggers | `alwaysApply`/description mismatch for your Cursor build | Use `alwaysApply: true`, or a description that activates on grounded questions; verify with ST-3 and note the mechanism |
| Two grounding rules fight each other | Old `grounding-discipline.mdc` left active | One canonical, one loaded — fold the old one in and delete it |
| Rule is 60 lines and ignored | Essay, not enforceable clauses | Cut to the clauses that name a failure; the stress test only asserts these |
| Citation format drifts between answers | Format defined in two places | Single source: the scope contract file; the rule points at it |

---

## Checkpoint questions

1. Why implement the guardrail as a rule/skill rather than a one-time prompt instruction?
2. Why does the rule prescribe a standard refusal phrase instead of "say you don't know"?
3. What does the enforcement test prove that the stress test (Lab 13.4) alone does not?

<details>
<summary>Answers</summary>

1. A rule loads automatically on every invocation, so the guardrail holds regardless of who asks or how the question is phrased. A one-time instruction holds only for that conversation — and anyone who forgets it gets an unguarded agent.
2. An exact phrase is assertable: a reviewer can grep a transcript for it, and the stress test can mark PASS/FAIL mechanically. "Say you don't know" produces a different paraphrase every time and cannot be checked.
3. The enforcement test isolates the rule mechanism itself: the prompt never mentions the rule, so a compliant response proves the behavior came from automatic loading — not from the user reminding the agent. The stress test then checks the behavior across categories.

</details>

---

## Next

**Lab 13.4 — Stress-Test the Grounding.** The rule is loaded; now try to break it. Adversarial questions across all four categories, predictions before runs, and a diagnose → fix → re-run loop for every FAIL.

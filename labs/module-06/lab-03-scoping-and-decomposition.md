# Lab 6.3 — Scope the Blast Radius & Decompose Before You Start

**Module 6 · Codebase-Aware Editing & Agent Mode | Xebia — Cursor AI Training**
Day 2 · Lab 3 of 3 · ~15–20 minutes · Individual

> **Objective:** prove the scoping lesson with a controlled comparison — open-ended instruction vs. tightly scoped
> instruction — then practice the professional response to an oversized ask: decompose it into commit-sized,
> individually reviewable and reversible steps.

**Guide references:** Module 6, §5 (scoping AI edits safely), §6 (context limits, decomposition, reviewable/reversible changes)
**Learning objectives covered:** 5 — safe scoping; 6 — context limits and decomposition.

---

## Before you start

- Labs 6.1–6.2 complete; still on `module6-agent-lab`
- For the open-ended test, you will **stop before edits are applied** — you're comparing intended scope, not
  shipping the result
- Have Lab 6.1's instruction in front of you (the feature-level, folder-bounded one)

---

## Step 1 — Open-ended vs. tightly scoped: compare intended scope

**Run A — deliberately open-ended.** In a new Agent chat, send:

> "Clean up and improve the error handling across the project."

- Watch the exploration/plan phase and note every file and folder it intends to touch.
- **Stop before applying anything** (stop the run / reject all changes). This is a blast-radius measurement, not a task.
- Record the intended scope: `____________`

**Run B — tightly scoped.** In a new chat, send a bounded version of the same underlying goal:

> "Refactor the error handling in `<target-file>` to use the project's existing error types, and update its direct
> callers in `<feature-folder>`. Change nothing else."

- Again, review the plan/per-file diffs before applying. You may apply and validate this one, or stop after review.

| | Run A (open-ended) | Run B (tight) |
|---|---|---|
| Files intended/edited | | |
| Drift outside the goal? | | |
| Reviewable in one sitting? | | |
| Could you revert it cleanly? | | |
| Time to review | | |

- [ ] Both runs recorded; at least one concrete difference identified
- [ ] No unintended changes left behind from Run A

---

## Step 2 — Decompose an oversized ask

Take something intentionally too big and split it — for example:

> "Implement the whole reporting feature" (data model → aggregation logic → API endpoint → export format → tests)

Write 3–4 commit-sized steps, each with its own review checkpoint. Use the guide's template:

| Step | Scope (files) | Review checkpoint | Reversible how? |
|---|---|---|---|
| 1. Add data model | | tests/lint for the model pass | single commit on the branch |
| 2. Add service logic | | | |
| 3. Add API endpoint | | | |
| 4. Add tests / harden | | | |

- [ ] 3–4 steps defined, each commit-sized and independently reviewable

---

## Step 3 — Run only step 1 (the discipline test)

1. In a new Agent chat, send **only** step 1's instruction, with its scope boundary stated.
2. Review and validate it as in Lab 6.1 (per-file diffs → `<test-command>` → commit on the branch).
3. Resist the urge to let the agent continue into step 2 — the next step starts in a **new chat**, after step 1 is
   reviewed and committed.

- [ ] Step 1 implemented, validated, and committed on the branch
- [ ] Step 2 not started in the same context

---

## Step 4 — Reviewability & reversibility check

For your Lab 6.1 change and this step-1 change, answer honestly:

| Question | Lab 6.1 change | Step-1 change |
|---|---|---|
| Reviewed file-by-file in one sitting? | | |
| One command to revert? (`git revert <hash>` / drop branch) | | |
| Would a teammate understand it from the commit alone? | | |
| If "no" to any — how would you split it further? | | |

Also record the context-limit angle (guide §6): what would happen to quality and review burden if you'd sent all
four steps as one instruction? `____________`

- [ ] Both changes pass the reviewable/reversible bar (or a split plan recorded)
- [ ] Context-budget consequence articulated

---

## Evidence

- Run A vs. Run B comparison table
- Decomposition table (3–4 steps)
- Step-1 commit hash on the branch + validation output
- Reviewability/reversibility check answers

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Run A never shows a plan before editing | Agent starts editing immediately | Stop/reject all; if your flow has no plan preview, ask first: "List the files you would change, in order, without editing yet" |
| Run A touched files before you stopped it | Timing | Reject all changes; confirm `git status`; note it as the exact risk the exercise demonstrates |
| Run B drifted anyway | Boundary stated too softly | Re-instruct: "Only `<paths>`; do not refactor anything else" |
| Decomposition feels artificial for a small sandbox | Small feature | Do the exercise anyway — the skill scales; note where you'd merge steps |
| Step 2 started automatically | Agent continued on its own | Stop it; reviews happen between steps by definition |

---

## Checkpoint questions

1. Give an example of turning an oversized instruction into two or three decomposed, reviewable steps.
2. Why does explicit scope matter *more* as tasks get more agentic?
3. What are the two properties every agent change should have before you trust it?

<details>
<summary>Answers</summary>

1. "Implement the whole reporting feature" → (1) add data model, (2) add service logic, (3) add API endpoint,
   (4) add tests — each reviewed and committed before the next begins.
2. The instruction is the blast radius: open-ended asks invite the agent to touch far more than intended; named
   files/folders and explicit out-of-scope boundaries keep the change verifiable.
3. Reviewable (small enough to inspect file-by-file) and reversible (easy to undo on its own — one commit or one
   branch).

</details>

---

## Next

**Module 7 — Plan, Debug, Refactoring & Testing** builds directly on this agent loop: an explicit plan phase, a diagnostic mode, and AI-assisted tests.

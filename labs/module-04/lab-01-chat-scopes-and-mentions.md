# Lab 4.1 — Chat Scopes & @-Mentions: Same Question, Four Scopes

**Module 4 · AI Chat, Context & Ask Mode | Xebia — Cursor AI Training**
Day 1 · Lab 1 of 3 · ~15–20 minutes · Individual · Read-only

> **Objective:** run the deck's controlled experiment — the identical question at no-context, file, folder, and
> codebase scope, then once more with explicit `@`-mentions — and feel how scope changes answer quality, citation
> behavior, and latency. This is context engineering as a measurable engineering decision.

**Guide references:** Module 4, §1 (Chat at file/folder/codebase scope), §2 (@-mentions), §4 (Context selection and scoping)
**Learning objectives covered:** 1 — Chat at multiple scopes; 2 — `@`-mentions; 4 — deliberate scoping.

---

## Before you start

- Module 3 complete: workspace open, chat panel available, one model confirmed
- **Pin one model** for the whole experiment (not Auto) so scope is the only variable
- Pick your target **before** you start, and don't change it mid-experiment:
  - `<target-function>` — a non-trivial function in `<sandbox-repo>` (non-obvious behavior, some error handling)
  - `<target-file>` — the file that defines it
  - `<target-folder>` — that file's directory
- Write the question **once** and reuse it verbatim — if the wording changes, the experiment is invalid:

  > "What does `<target-function>` do? Describe its inputs, outputs, side effects, and error conditions, and cite the file and line numbers."

- Start every scope in a **fresh chat** (`Cmd/Ctrl+N`) so no history bleeds between runs

---

## Step 1 — Record the control

- [ ] Question written down verbatim (same for all runs)
- [ ] One model pinned for all four runs — model: `____________`

---

## Step 2 — Baseline: no context attached

1. Open a new chat. Ask the question with **nothing attached** and without triggering codebase search — just send it.
2. Observe: did it ask for context, invent a plausible answer, or cite anything at all?

- [ ] Baseline behavior recorded (generic answer / request for context / invention)

---

## Step 3 — File scope

1. Open `<target-file>` in the editor (or attach it with `@<target-file>`).
2. New chat; ask the **identical** question.
3. Observe: specificity, line citations, whether it stayed inside the file.

- [ ] File-scope answer recorded

---

## Step 4 — Folder scope

1. New chat; attach the folder (`@<target-folder>`, or the folder option in the `@` picker).
2. Ask the identical question.
3. Observe: did neighboring files help (call sites, siblings) or dilute the answer?

- [ ] Folder-scope answer recorded

---

## Step 5 — Codebase scope

1. New chat; ask with codebase-wide search (`@Codebase`, or your build's codebase search trigger).
2. Observe: rough latency, whether it found `<target-file>` at all, and whether it cited precisely or hand-waved.
   Remember: whole-codebase search is **best-effort retrieval** — it may miss or mis-rank files (guide §1).
3. Key comparison: how does this answer stack up against the **file-scoped** answer from Step 3?

- [ ] Codebase-scope answer recorded
- [ ] Noted whether codebase search found the same file the explicit scope did

---

## Step 6 — Explicit grounding with @-mentions

1. New chat; attach `@<target-file>` and `@<target-function>` explicitly; ask the identical question.
2. This is the deterministic answer. Which earlier run does it most resemble? Where exactly did codebase search get it slightly wrong?

- [ ] `@`-mention answer recorded and compared to Steps 3–5

---

## Step 7 — The two-step habit: locate, then re-ask scoped

1. Pick a behavior you genuinely don't know the location of. In a new chat, ask a **locator** question:
   > "Where is `<some behavior>` handled? List candidate files with one line each — do not explain them yet."
2. Start a new chat and re-ask the real question with `@`-mentions of the files it surfaced.
3. Record how much tighter (and better-cited) the second answer is compared to a direct unscoped ask.

- [ ] Two-step habit exercised; improvement recorded

---

## Comparison table (fill in as you go)

| # | Run | Rough latency | Cited lines? | Found the right file? | Quality notes |
|---|---|---|---|---|---|
| 1 | No context | | | | |
| 2 | File scope | | | | |
| 3 | Folder scope | | | | |
| 4 | Codebase scope | | | | |
| 5 | `@`-mentions | | | | |

---

## Evidence

- Screenshot of the completed comparison table
- One answer showing file/line citations (from Step 3, 5, or 6)

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Codebase search misses the file entirely | Index not finished, or the file is excluded | Wait for indexing to complete; check `.cursorignore`; use an `@`-mention instead |
| All four answers look the same | Tiny repo, or the model routed differently per request | Confirm the model is pinned; pick a target with non-obvious behavior |
| `@` picker labels don't match the guide's table | UI version drift | Use the picker's own descriptions — the intent (file/folder/symbol/docs/git) is stable |
| Answer says it has no context | Nothing attached and search not triggered | Attach the file, or invoke codebase search explicitly |
| Folder attachment drags in huge context | Folder too broad | Narrow to the package/module, or attach the 2–3 files that matter |

---

## Checkpoint questions

1. What's the difference between codebase search finding a file and `@`-mentioning it directly — and when does each make sense?
2. Name two consequences of scoping a chat query too broadly.
3. When is the two-step habit (locate first, re-ask scoped) worth the extra turn?

<details>
<summary>Answers</summary>

1. Codebase search is best-effort and convenient when you don't know which file matters; `@`-mentioning is explicit
   and deterministic, best once you know the file(s)/docs — it's the grounding element of a well-formed prompt.
2. Any two of: diluted attention/lower reliability, higher token cost, slower responses, higher hallucination risk
   from irrelevant content.
3. When you don't know the relevant file(s): a cheap locator turn, then a scoped re-ask — faster and more reliable
   than repeated broad searches.

</details>

---

## Next

**Lab 4.2** — cross-reference a spec against code with citations, then observe the Ask vs Agent boundary.

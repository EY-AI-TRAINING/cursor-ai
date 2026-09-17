# Lab 5.3 — Context & Interaction Choice: What Feeds a Suggestion

**Module 5 · Inline Code Generation, Tab & Context | Xebia — Cursor AI Training**
Day 2 · Lab 3 of 3 · ~15–20 minutes · Individual

> **Objective:** prove the open-file context lever — same task, different tabs open, different suggestion quality —
> then tune one autocomplete setting and classify tasks by the interaction that fits their size.

**Guide references:** Module 5, §4 (surrounding code and open-file context), §5 (customizing autocomplete & choosing the interaction)
**Learning objectives covered:** 4 — open-file context's effect on quality; 5 — autocomplete settings and interaction choice.

---

## Before you start

- Labs 5.1–5.2 complete; `<scratch-file>` exists
- Pick `<pattern-file>` — a sandbox file containing a convention you want mirrored (an existing fixture, a service
  class, a test style)
- Working tree clean; same model pinned

---

## Step 1 — The open-files experiment (the core exercise)

1. **Run A — target only:** close every editor tab except `<scratch-file>`.
2. Ask for a change that depends on a repo convention, e.g.:
   > "Write a test for `parse_duration` following this project's test style."
3. Record the result: generic or convention-matching? What did it invent?
4. **Run B — with context:** open `<pattern-file>` (the file whose pattern you want mirrored). Keep `<scratch-file>` as the active tab.
5. Re-issue the identical instruction in a new region. Compare against Run A.
6. Record the difference — and the rule: Tab/inline generation read the current file, **open tabs**, recent edits, and
   visible lint errors; they do **not** read the whole repo. Chat (Module 4) + `@`-mentions is the tool for breadth.

| Run | Tabs open | What the suggestion did | Notes |
|---|---|---|---|
| A | `<scratch-file>` only | | |
| B | `<scratch-file>` + `<pattern-file>` | | |

- [ ] Both runs completed and recorded
- [ ] At least one concrete difference between Run A and Run B identified

---

## Step 2 — Boilerplate that reuses patterns

1. With the sandbox's existing test file open (e.g., `test_*.py` / `*.test.ts`), invoke `Cmd/Ctrl+K` in a new area:
   > "Add a pytest fixture that spins up a temp SQLite DB."
2. Check whether it reused the suite's existing fixture patterns or produced a textbook version from scratch.
3. Close the test file and repeat once — note the regression in convention-matching.

- [ ] Boilerplate reused existing patterns with the pattern file open; difference without it recorded

---

## Step 3 — Classify: match the interaction to task size

Using guide §5's decision rule, fill in the interaction you would use and why:

| Task | Tab-to-complete | Inline `Cmd/Ctrl+K` | Chat/Ask first, then inline | Agent (Module 6) | Why |
|---|---|---|---|---|---|
| Finish a line you're mid-way through | | | | | |
| A few lines with clear intent (e.g., null check) | | | | | |
| A class with real design decisions | | | | | |
| A change that spans multiple files | | | | | |

- [ ] All four classified with a one-phrase justification

---

## Step 4 — Tune one autocomplete knob

1. Open Cursor Settings (`Cmd/Ctrl+Shift+J`) → search `Tab` / `autocomplete` / `inline`.
2. Note the controls available in your build — commonly: enable/disable Tab completion, suggestions in comments
   and strings, trigger behavior/aggressiveness, partial-accept behavior.
3. Change **one** setting (e.g., disable suggestions inside comments) and test the effect: does the comment-driven
   generation from Lab 5.1 still fire? Does Tab feel differently paced?
4. Restore the default (or record the personal preference you'll keep).
5. Note for Module 8: these become team standards — project rules — not personal guesses.

- [ ] One setting tuned, effect observed, default restored (or preference recorded)
- [ ] One setting found that you'd recommend discussing as a team standard

---

## Evidence

- The Run A / Run B comparison table
- The interaction-choice table
- Screenshot of the autocomplete setting you tuned (before/after values noted)

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Run A and Run B look identical | The convention is simple enough that one file suffices | Pick a subtler convention (fixture setup, error-handling style, naming) |
| Opening more files doesn't help | Irrelevant tabs dilute the signal | Keep only the 2–3 files whose pattern you actually want mirrored (guide §4) |
| Setting names differ from expected | UI drift between builds | Search the settings for `Tab`, `autocomplete`, `inline` — the intent (aggressiveness, comments/strings) is stable |
| Suggestions stopped entirely after tuning | You disabled Tab completion | Re-enable; re-test with one knob at a time |
| Inline generation ignores the open pattern file | Instruction didn't reference what to mirror | Say it: "follow the pattern in the open test file" — or use Chat with `@`-mentions for explicit grounding |

---

## Checkpoint questions

1. What context do Tab and inline generation actually use — and what do they *not* have access to?
2. Give two levers you control to improve suggestion quality without changing the model.
3. When would you use Chat/Ask mode *before* inline generation rather than instead of it?

<details>
<summary>Answers</summary>

1. They use the current file (especially near the cursor), other open tabs, recent edits, visible lint/type errors,
   and your instruction (inline only). They do not read the whole repository — that's Chat's codebase scope
   (Module 4) and Agent mode (Module 6).
2. Close irrelevant tabs and open the file whose pattern you want mirrored; keep the cursor near the relevant code;
   write a tighter instruction.
3. When the task involves a design decision or unclear approach — reason it through in Chat first, then use inline
   generation to produce the scoped diff once the approach is settled.

</details>

---

## Next

**Module 6 — Codebase-Aware Editing & Agent Mode** takes the same trust and the same gate and scales it across multiple files.

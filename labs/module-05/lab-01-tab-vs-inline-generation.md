# Lab 5.1 — Tab vs Inline Generation: Two Entry Points

**Module 5 · Inline Code Generation, Tab & Context | Xebia — Cursor AI Training**
Day 2 · Lab 1 of 3 · ~15–20 minutes · Individual

> **Objective:** use both of Cursor's cursor-position generation tools on purpose — Tab-to-complete for something
> you're already typing, inline generation (`Cmd/Ctrl+K`) for something you haven't started — and observe what Tab
> infers correctly vs. incorrectly from local context.

**Guide references:** Module 5, §1 (Tab-to-complete vs. inline generation), §2 (functions, classes, boilerplate)
**Learning objectives covered:** 1 — explain the two mechanisms; 2 — generate functions and classes with inline generation.

---

## Before you start

- Modules 3–4 complete; sandbox repo open; `git status` clean
- Create your scratch file in `<sandbox-repo>` root: `module5_practice.<ext>` (e.g., `module5_practice.py`)
- Pin one model for the whole lab
- Language note: examples below are Python — adapt syntax if your sandbox uses another stack

---

## Step 1 — Tab-to-complete: finish what you started

1. In `<scratch-file>`, write a TODO comment describing a function (comment-driven generation):
   ```python
   # TODO: implement parse_duration(s) -> int that converts "1h30m" to seconds
   ```
2. On the next line, type only the signature and stop:
   ```python
   def parse_duration(s):
   ```
3. Wait for **ghost text** to appear. Read it before touching anything:
   - How much did it infer — signature, body, docstring, edge cases?
   - Does it match the naming/style of the rest of the file?
4. Accept with `Tab`. Then trigger it again elsewhere and practice:
   - **partial accept** — accept word-by-word with `Cmd/Ctrl+→`
   - **reject** — `Esc`, or just keep typing

- [ ] Ghost text observed before accepting (read, then accepted)
- [ ] Partial accept and reject both practiced

---

## Step 2 — Record what Tab inferred

Tab reads **local context**: current file near the cursor, other open tabs, recent edits, visible lint errors
(guide §4). Note its strengths and misses:

| Inferred correctly | Inferred incorrectly / missed |
|---|---|
| e.g., matched signature | e.g., ignored the "1h30m" format edge case |
| | |

- [ ] At least one correct inference and one miss recorded

---

## Step 3 — Inline generation: generate what you haven't started

1. Move to an empty region of `<scratch-file>` (or below the existing function).
2. Invoke inline generation: `Cmd/Ctrl+K`.
3. Write a scoped instruction, e.g.:
   > "Write a function `retry_with_backoff(fn, max_attempts=5)` that retries with exponential backoff and re-raises the last error."
4. Review the **proposed diff** inline — this is the review unit (a diff hunk, not ghost text). Accept only what matches the instruction.
5. Repeat for a second shape — a class:
   > "Create a `RetryPolicy` class with exponential backoff, max 5 attempts, and a `delay_for(attempt)` method."

- [ ] Function generated via `Cmd/Ctrl+K` and reviewed as a diff
- [ ] Class generated and reviewed
- [ ] Noted whether the generated code fit the file's existing style or looked like generic boilerplate

---

## Step 4 — Make the scratch file actually run

1. Add a couple of quick calls/assertions at the bottom of `<scratch-file>` (or a tiny `if __name__` block), e.g.:
   ```python
   assert parse_duration("1h30m") == 5400
   ```
2. Run it: `python module5_practice.py` (or your stack's equivalent).
3. Fix what fails — by hand, or by selecting the offending code and re-running `Cmd/Ctrl+K` with a tighter instruction.

- [ ] Scratch file runs without errors
- [ ] Any failure was fixed (hand-edit or regenerate) and re-run

---

## Evidence

- `<scratch-file>` containing accepted Tab completions and inline-generated function/class
- Your inferred-correctly / inferred-incorrectly table from Step 2

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| No ghost text appears | Tab completions disabled, language not recognized, or file excluded | Cursor Settings → search `Tab` / `autocomplete`; confirm the file's language mode; check `.cursorignore` |
| Ghost text is a single word only | Small/simple context | Add a TODO comment above (comment-driven generation gives it intent); write more of the surrounding pattern |
| `Cmd/Ctrl+K` does nothing | Keybinding differs in your build | Command Palette → search `Inline Edit`; remap in Keyboard Shortcuts if needed |
| Instruction produced the wrong thing | Instruction too vague or missing the pattern to mirror | Include signature/behavior explicitly; open a file that shows the convention you want (Lab 5.3) |
| Partial accept keybinding doesn't work | Build/keymap variance | Keyboard Shortcuts → search `accept` and note your binding |

---

## Checkpoint questions

1. What is the key input difference between Tab-to-complete and inline generation?
2. Which one produces ghost text, and which produces a diff for review?
3. Why does a narrower context window make Tab/inline generation faster but less broad than Chat (Module 4)?

<details>
<summary>Answers</summary>

1. Tab is implicit — triggered by cursor position and typing, no authored prompt. Inline generation is explicit —
   you write a natural-language instruction.
2. Tab → ghost text; inline generation (`Cmd/Ctrl+K`) → in-place diff.
3. They lean on local signals (current file, open tabs, recent edits, lint errors) instead of whole-codebase
   retrieval — less noise and lower latency, at the cost of breadth. The trade is deliberate.

</details>

---

## Next

**Lab 5.2** — every suggestion is a decision: accept, edit-then-accept, partial accept, reject — then validate.

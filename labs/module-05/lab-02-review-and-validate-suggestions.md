# Lab 5.2 — Every Suggestion Is a Decision: Accept, Edit, Partial, Reject, Validate

**Module 5 · Inline Code Generation, Tab & Context | Xebia — Cursor AI Training**
Day 2 · Lab 2 of 3 · ~15–20 minutes · Individual

> **Objective:** deliberately practice all four suggestion outcomes on different prompts, then prove the review
> loop on a real targeted change: scoped diff → scope verification → validation → revert. The accept → validate
> discipline you build here is the manual precursor to Module 17's automated quality gates.

**Guide references:** Module 5, §2 (targeted changes), §3 (accepting, rejecting, editing, validating)
**Learning objectives covered:** 3 — deliberate accept/reject/edit behavior; 2 — targeted changes; validation discipline.

---

## Before you start

- Lab 5.1 complete; `<scratch-file>` exists and runs
- Know your sandbox's test/lint command (ask your facilitator; e.g., `pytest -q`, `npm test`, `ruff check`) — you'll use it in Step 5
- Working tree: `git status` clean before starting

---

## Step 1 — Accept as-is (the obvious case)

1. In `<scratch-file>`, start a pattern you'd already write yourself — a simple loop, a print, a repeated line.
2. Let Tab complete it; confirm it is exactly what you intended; accept with `Tab`.

- [ ] Accept-as-is used and justified (boilerplate/obvious completion, pattern already proven in the file)

---

## Step 2 — Edit-then-accept (the 80% case)

1. Trigger an inline generation (`Cmd/Ctrl+K`) with a slightly under-specified instruction, e.g.:
   > "Write a helper that logs and returns the result of a function call."
2. Accept the draft even though it's not perfect (naming, log format, or error handling is off).
3. Hand-fix the remaining 20% directly.
4. Record why editing was faster than re-prompting and regenerating.

- [ ] Edit-then-accept exercise completed; reasoning recorded

---

## Step 3 — Partial accept (take only part)

1. Trigger a long suggestion (multi-line) — e.g., ask for a function plus docstring plus example usage.
2. Use partial accept (`Cmd/Ctrl+→` accepts the next word) to take the part that's correct.
3. Reject the remainder (`Esc`, or keep typing to ignore it).

- [ ] Partial accept used; remainder rejected cleanly

---

## Step 4 — Reject (the discipline case)

1. Deliberately over-scope an instruction on working code — e.g., select a small function and instruct:
   > "Improve this function."
2. Observe the common failure mode: the suggestion rewrites more than you asked and changes behavior you didn't want touched.
3. **Reject it.** Then re-issue a tightly scoped instruction instead.
4. Record: what made the first suggestion unacceptable even if it was "technically fine"?

- [ ] Over-scoped suggestion rejected with reasoning recorded
- [ ] Re-scoped instruction produced an acceptable result

---

## Step 5 — Targeted change on a real file: scope, verify, validate, revert

1. Pick a real function in `<target-file>` (tracked, in the sandbox) that is missing a small guard — for example,
   add a null/None check before a lookup, or handling for an empty list. Choose one with a **clear existing test**
   if the sandbox has tests.
2. Select the relevant lines and invoke `Cmd/Ctrl+K` with a tight instruction, e.g.:
   > "Add a null check before this `.get('user')` call; change nothing else."
3. Review the proposed diff. If it rewrites surrounding code, reject and rephrase until the diff is minimal.
4. Accept, then **verify scope** before anything else:
   ```bash
   git diff <target-file>
   ```
   The hunk must contain only what you asked for — a targeted change is a two-line diff, not a rewritten function.
5. **Validate** — acceptance ≠ correctness. Run your validation command (tests/lint, or execute the affected path).
6. **Revert** the change (this lab leaves no code behind):
   ```bash
   git restore <target-file>
   git status
   ```

- [ ] `git diff` showed only the requested change (screenshot taken)
- [ ] Validation command run and output recorded
- [ ] File reverted; `git status` shows no tracked modifications

---

## Evidence

- Screenshot of the minimal `git diff` before reverting
- Test/lint/execute output proving the accepted change worked
- `git status` clean after revert
- Your reject/edit/partial-accept reasoning notes from Steps 1–4

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Every suggestion is over-broad | Instruction too vague ("improve", "refactor") | Name the exact change and constrain it: "change nothing else" |
| `git diff` shows reformatting noise | Formatting hooks or the model rewrote style | Reject and rephrase; or revert, then apply a minimal hand-edit |
| Tests fail after a correct-looking change | Acceptance ≠ correctness — the gate caught it | Fix manually or regenerate with more context (Module 7 covers Debug mode) |
| Validation command unknown | Sandbox setup variance | Ask your facilitator for the repo's test/lint command; record it for Module 6 |
| No tests exist for the target | Small sandbox | Write a two-line assertion in `<scratch-file>` (or a temp test) to validate behavior, then revert |

---

## Checkpoint questions

1. Name the four outcomes any suggestion can have, and when each is appropriate.
2. Why is a technically correct suggestion still sometimes worth rejecting?
3. What does accepting a diff actually guarantee — and what closes the loop?

<details>
<summary>Answers</summary>

1. Accept as-is (boilerplate/obvious/proven patterns); partial accept (only part is right); edit-then-accept
   (80% draft + hand-fix); reject (off-track, out of scope, or risky) and rephrase or write by hand.
2. It may exceed the requested scope, conflict with file conventions, or introduce a pattern the team doesn't want —
   correctness alone doesn't make it acceptable.
3. Accepting only means the code is in your buffer. Validation — tests, lint, or executing the change — is what
   closes the loop. You are the gate until Module 17's automated gates exist.

</details>

---

## Next

**Lab 5.3** — context and interaction choice: open files change suggestions, and task size picks the tool.

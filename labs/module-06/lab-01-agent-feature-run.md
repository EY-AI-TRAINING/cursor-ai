# Lab 6.1 — Ship a Small Feature Across Files with Agent Mode

**Module 6 · Codebase-Aware Editing & Agent Mode | Xebia — Cursor AI Training**
Day 2 · Lab 1 of 3 · ~20–25 minutes · Individual (work on your own branch)

> **Objective:** drive the full agent loop once, end to end — feature-level instruction → indexed retrieval →
> multi-file edits → per-file review → validation — and finish with a reviewed, reversible change on a branch.

**Guide references:** Module 6, §1 (Agent mode for multi-file changes), §2 (codebase indexing and repository context), §3 (cross-file diffs and review)
**Learning objectives covered:** 1 — feature-spanning Agent mode; 2 — indexing/retrieval; 3 — cross-file diff review.

---

## Before you start

- Modules 3–5 complete; clean working tree on the default branch
- Create your lab branch now — nothing in this module touches the default branch:

  ```bash
  git switch -c module6-agent-lab
  ```

- Confirm the codebase index is ready: Command Palette (`Cmd/Ctrl+Shift+P`) → search `index` / `codebase`.
  Indexing is background and ongoing (guide §2) — a stale index (e.g., right after a branch switch) can make the
  agent reason about code that no longer matches disk, so give it a moment to catch up after branching.
- Know your `<test-command>` (ask your facilitator).
- Pick `<feature>`. Default example from the deck — a CSV export:
  - a new exporter module (e.g., `exporters/to_csv.<ext>`)
  - wiring in an existing route/handler (`<target-file>`)
  - tests alongside the suite

- Keep the same model you used in Module 5 so differences come from the agent loop, not routing.

---

## Step 1 — Write a feature-level instruction (bounded, not open-ended)

Draft one instruction that names the feature and the folder it lives in — feature-level, but with a blast radius
you chose:

> "Add a CSV export for `<feature>`. Create a new exporter module under `<feature-folder>/exporters/` with a
> `to_csv(...)` function, wire a `GET /<feature>/export` route in `<target-file>`, and add tests under `<tests-folder>`.
> Do not modify files outside those paths."

- [ ] Instruction written, with the scope boundary stated explicitly
- [ ] Expected files-to-touch list predicted **before** sending (2–3 files minimum): `____________`

---

## Step 2 — Send it in Agent mode

1. Open a new chat in **Agent mode** and send the instruction.
2. As the agent works, watch the exploration phase: which files does it read/search? Note the plan/sequence it
   announces, if shown.
3. Do **not** interrupt yet — let it produce the aggregated change set, but stop it if it starts touching files
   outside your stated scope (that's a finding, not a failure).

- [ ] Agent run completed (or was stopped for scope drift — recorded)
- [ ] Retrieved/edited file list captured: `____________`

---

## Step 3 — Compare retrieval against your expectations (the indexing lesson)

| | Expected (your prediction) | Actual (agent's retrieval/edits) | Why it differs |
|---|---|---|---|
| Files read | | | |
| Files edited | | | |
| Files missed / extra | | | |

- [ ] Differences explained (index freshness, naming, symbols it couldn't infer, etc.)

---

## Step 4 — Review the aggregated diff, file by file

1. Open the change set and review each file's diff like a pull request — hunk by hunk.
2. Check for the classic multi-file failure: an edit that's individually plausible but collectively inconsistent
   (e.g., a helper renamed in two call sites but missed in a third — guide §3).
3. Where a file is wrong or unnecessary, use selective approve/reject, or ask the agent to address the gap.
4. Record at least one review judgment (inconsistency caught, or a reasoned confirmation of consistency).

- [ ] Every touched file reviewed before approval
- [ ] One inconsistency caught **or** consistency explicitly confirmed with reasoning

---

## Step 5 — Validate independently (you are the final gate)

Acceptance ≠ correctness (Module 5). Run validation yourself — the agent doesn't get the last word:

```bash
<test-command>
```

Manually exercise the feature if the sandbox can run it. Fix or re-prompt for anything that fails.

- [ ] Tests/lint executed; output recorded
- [ ] Feature exercised end to end (or a recorded reason it can't run locally)

---

## Step 6 — Make the change reviewable and reversible

1. Review the final `git diff` once more as a whole.
2. Commit on your lab branch so the change is self-contained and revertible:

   ```bash
   git add -A
   git commit -m "Module 6 lab: <feature> (agent-assisted, reviewed)"
   git log --oneline -1
   ```

3. Record the commit hash — this is the "reviewable, reversible" unit from the guide.

- [ ] Committed on `module6-agent-lab`; hash recorded: `____________`
- [ ] Can state how you'd revert it in one command (`git revert <hash>` or drop the branch)

---

## Evidence

- Files-touched vs. expected table (Step 3)
- Per-file review notes incl. the inconsistency catch/confirmation (Step 4)
- Validation output (Step 5)
- Commit hash + screenshot of the aggregated diff summary

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Agent edits files outside the named paths | Instruction's boundary too soft, or it "helpfully" refactored | Reject those hunks; re-instruct with "change nothing outside `<paths>`" |
| Retrieval misses an obvious file | Stale index after the branch switch, or naming mismatch | Wait for indexing; name the file explicitly in a follow-up instruction |
| Diff is too large to review in one sitting | Task wasn't feature-sized | Stop; decompose per Lab 6.3, then resume |
| Agent claims tests pass but you can't reproduce | Verification is yours, not the agent's | Run the test command yourself; treat unverifiable claims as findings |
| Agent run stalls or loops | Task too vague or context budget exhausted | Provide the missing detail, or split into a smaller instruction |
| Nothing happens — Agent mode unavailable | Plan/seat restrictions | Pair with a neighbor; report to facilitator (Lab 3.1 covers seat checks) |

---

## Checkpoint questions

1. What does Agent mode do that inline generation (Module 5) does not?
2. How does codebase indexing let the agent find files without you `@`-mentioning them?
3. Why should a multi-file agentic diff get **more** scrutiny than a single-file suggestion?

<details>
<summary>Answers</summary>

1. It runs a multi-step loop — exploring the codebase, planning an edit sequence, editing multiple files, executing
   tools/tests, and iterating — instead of producing one diff from one instruction.
2. Cursor pre-builds a searchable (semantic + structural) index; at task time the agent queries it and retrieves
   relevant files/symbols itself — the same retrieval you'd do manually with `@`-mentions in Chat.
3. More files touched means more surface area for edits that are individually plausible but collectively
   inconsistent (e.g., a missed call site) — the aggregate needs checking, not just each piece.

</details>

---

## Next

**Lab 6.2** — gate the agent's terminal commands: approve one, deny one, observe the fallback.

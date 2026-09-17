# Lab 8.1 — Scoped Project Rules: Encode a Real Convention

**Module 8 · Rules, AGENTS.md, Skills & Team Standards | Xebia — Cursor AI Training**
Day 2 · Lab 1 of 3 · ~15–20 minutes · Individual

> **Objective:** write one Project Rule in `.cursor/rules/` that encodes a real convention from the sandbox repo,
> with frontmatter scoped correctly — then prove it changes agent behavior. Also: rescue a vague rule ("Write good
> tests") and make it testable.

**Guide references:** Module 8, §1 (Project Rules), §7 (concise, testable, maintainable)
**Learning objectives covered:** 1 — write Project Rules; 7 — testable, maintainable instructions.

---

## Before you start

- Modules 3–7 complete; create your branch:

  ```bash
  git switch -c module8-lab
  ```

- Pick `<convention>` — something the codebase already does that an agent could plausibly get wrong without
  being told. Good candidates:
  - "All API errors use the project's `ApiError` type, never bare `throw new Error`"
  - "Tests live under `tests/`, mirroring the source path"
  - "Never edit files under `generated/` or migrations by hand"
- Decide `<glob>` — which files the convention applies to (e.g., `src/api/**`, `**/*.test.*`).

---

## Step 1 — Choose the right scope type

Frontmatter has exactly three fields — `description`, `globs`, `alwaysApply` — and their combination picks the
rule type. Choose deliberately:

| Type | Frontmatter | Use when |
|---|---|---|
| Always Apply | `alwaysApply: true` | True for the whole repo, every session — use sparingly |
| Apply to Specific Files | `globs: [...]`, `alwaysApply: false` | Convention only matters for matching files ← **default choice** |
| Apply Intelligently | `description: ...`, no globs | Agent should decide relevance from the description |
| Apply Manually | none of the three | Only when you `@`-mention it in chat |

- [ ] Scope chosen and justified: `____________` (prefer the specific-file scope unless you have a reason)

---

## Step 2 — First, rescue a vague rule (the quality bar, up close)

Rewrite this classic into something concise and testable:

> **Before:** "Write good tests."

A strong revision names the observable behavior and the project's concrete tooling, for example:

> **After:** "Tests use `<test-command>`-discoverable naming; each new behavior gets a test that fails before the
> change and passes after. Place tests per `tests/` mirroring the source path."

- [ ] Rewritten rule is concise (state instruction + brief reason), concrete, and testable by a sample task
- [ ] Can answer: what sample task would verify it? `____________`

---

## Step 3 — Write the rule file

1. Write `.cursor/rules/<rule-name>.mdc` with frontmatter and a short body, e.g.:

   ```markdown
   ---
   description: API error handling conventions for service code
   globs: ["src/api/**"]
   alwaysApply: false
   ---

   - All errors thrown across API boundaries use the project's `ApiError` type.
   - Include an actionable message and the originating status code.
   - Do not leak internal stack traces in responses.
   ```

2. Create it however you prefer: `Cmd/Ctrl+Shift+P` → **New Cursor Rule**, Settings → Rules → **Add Rule**, or
   `/create-rule` in chat (a built-in skill that generates the file). Verify it appears under **Project Rules**
   in Settings → Rules.

- [ ] Rule file created at `.cursor/rules/<rule-name>.mdc`; extension and frontmatter fields valid
- [ ] Visible in Cursor Settings → Rules (screenshot as evidence)

---

## Step 4 — Test it against a real task (testable means tested)

A rule that reads well isn't a rule that works. Verify the trigger, then the behavior:

1. **Trigger test:** open a file matching `<glob>` and, in chat, ask something the rule should govern — e.g.,
   "Add error handling to `<function>` in this file." The rule should be in play because the file matched.
2. **Behavior test:** check the diff/answer uses `ApiError` (or your convention). If not, tighten the rule's
   wording or scope — that's the refine loop from §7.
3. **Boundary test:** open a file *outside* `<glob>` and repeat. The rule should **not** apply — if it still
   leaks in, your scoping is wrong (or the rule should be always-applied; decide consciously).
4. Note: rules load automatically — you don't need to `@`-mention a scoped rule; you can reference it to inspect
   it (`@<rule-name>`).

- [ ] Trigger + behavior confirmed on a matching file (transcript saved)
- [ ] Boundary confirmed on a non-matching file
- [ ] One refinement iteration made if needed

---

## Step 5 — Commit the rule

```bash
git add .cursor/rules/
git commit -m "Module 8 lab: add <rule-name> project rule"
```

- [ ] Committed on `module8-lab`; hash `____________` (more files join this kit in Labs 8.2–8.3; a single kit commit at the end is also fine — follow your facilitator)

---

## Evidence

- Rule file + screenshot from Settings → Rules
- Vague-rule rewrite (before/after)
- Trigger/behavior/boundary test transcript (or notes)

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Rule doesn't appear in Settings → Rules | Wrong extension (plain `.md` without frontmatter is ignored) or wrong folder | Use `.mdc` in `.cursor/rules/`; confirm frontmatter is the first thing in the file |
| Rule never activates | Scope mismatch — glob doesn't match the open file | Check the pattern against the actual paths; use the boundary test to debug |
| Rule applies everywhere | `alwaysApply: true` accidentally, or too-broad glob | Narrow the glob or set `alwaysApply: false` |
| Agent follows the rule in chat but not in Agent mode | Rule wasn't in context during exploration | Name the scoped files in the instruction; re-test in Agent mode |
| Rule body growing long | You're documenting instead of instructing | Keep instruction + brief reason; move reference material to `AGENTS.md` or docs |

---

## Checkpoint questions

1. What's the difference between an always-applied rule and a glob-scoped rule?
2. Which three frontmatter fields control when a rule is loaded, and how do they combine?
3. What does it mean for a rule to be "testable," and why does that matter?

<details>
<summary>Answers</summary>

1. Always-applied loads in every request regardless of context; glob-scoped loads only when files matching the pattern are in play — it stays silent otherwise.
2. `description`, `globs`, `alwaysApply`: `true` = always; `globs` + `alwaysApply: false` = auto-attach on matching files; description only = agent decides relevance; none = manual `@`-mention only.
3. You can run a concrete sample task and check the rule produced the intended behavior — without that, you're assuming it works because it reads well.

</details>

---

## Next

**Lab 8.2** — the repository-wide onboarding doc for agents: `AGENTS.md`, plus instruction precedence.

# Lab 8.2 — AGENTS.md & Instruction Precedence

**Module 8 · Rules, AGENTS.md, Skills & Team Standards | Xebia — Cursor AI Training**
Day 2 · Lab 2 of 3 · ~15–20 minutes · Individual

> **Objective:** draft a short `AGENTS.md` — the repository's onboarding document *for agents* — with build/test
> commands, conventions, and at least one explicit guardrail. Then demonstrate the precedence rule live: on
> conflict, the most specific scope wins.

**Guide references:** Module 8, §2 (`AGENTS.md` and persistent guidance), §3 (user/team/project precedence)
**Learning objectives covered:** 2 — persistent repository guidance; 3 — precedence.

---

## Before you start

- Lab 8.1 complete, still on `module8-lab`
- `AGENTS.md` lives at the repo root as plain markdown — no frontmatter, no Cursor-specific syntax (that's the
  point: it's a tool-agnostic convention any capable agent can read)
- Have your `<test-command>` and one guardrail ready (e.g., "never edit `generated/` or migration files by hand")

---

## Step 1 — Split README vs. AGENTS.md (audience check)

Skim the sandbox `README.md` and note what belongs where:

| Content | README.md (humans) | AGENTS.md (agents) |
|---|---|---|
| Project purpose / setup | | |
| Exact build/test/lint commands | | |
| Code conventions an agent must follow | | |
| Guardrails: what *not* to touch | | |

- [ ] One-line rule of thumb written: "README explains **why/how for humans**; AGENTS.md tells **agents what to do and avoid**." Fine-tune: `____________`

---

## Step 2 — Draft AGENTS.md

Keep it short enough to read in one pass. Required elements:

1. **What the project is** — one or two sentences.
2. **Commands** — exact build/test/lint invocations (copy-pasteable, e.g., `<test-command>`).
3. **Conventions** — the ones an agent would otherwise guess wrong (naming, error types, test layout, imports).
4. **At least one guardrail** — an explicit "do not touch" / "never do" instruction.

```markdown
# AGENTS.md

<project one-liner>

## Commands
- Test: `<test-command>`
- Lint: `<lint-command>`
- Build: `<build-command>`

## Conventions
- <convention 1, e.g., API errors use ApiError>
- <convention 2, e.g., tests mirror the source path under tests/>

## Guardrails
- Never edit files under `generated/` by hand — regenerate with `<command>` instead.
- Do not add dependencies without asking.
```

- [ ] All four elements present; the file is one readable pass
- [ ] Commands verified: actually run `<test-command>` and confirm AGENTS.md matches reality

---

## Step 3 — Test AGENTS.md with a fresh agent

Open a **new chat** (no prior context) and ask questions whose answers should come only from `AGENTS.md`:

1. "How do I run this project's tests?"
2. "What conventions must you follow when editing this repo?"
3. "Is there anything you must not touch? Why?"

The agent should answer from the file without you pasting its contents.

- [ ] Transcript captured showing the agent using `AGENTS.md` unprompted
- [ ] Any gap patched into the file (then re-tested if behavior misses)

---

## Step 4 — Precedence, live: more specific scope wins

The hierarchy: **User → Team → Project**; on conflict, the project-level instruction wins because it reflects
what's actually true for this codebase.

1. **Prediction:** Lab 8.1's rule encodes `<convention>`. If a personal (User-level) preference contradicted it,
   which should win? Write your prediction: `____________`
2. **Live conflict (reverted at the end):** in Cursor Settings → Rules, add a *temporary* User Rule that
   contradicts a project rule. Example: if the project mandates `pytest`, add "When writing tests, prefer
   unittest" as a User Rule.
3. In a new chat, ask: "Which test framework should new tests in this repo use?" Record the answer — it should
   follow the project-level rule/`AGENTS.md`, not your personal preference.
4. **Revert immediately:** delete the temporary User Rule. Confirm it's gone from Settings.

- [ ] Prediction written before the test
- [ ] Outcome recorded: project won / did not win
- [ ] Temporary user rule deleted (evidence: settings screenshot after revert)
- [ ] If your seat has team rules available: note any that exist and how they'd participate: `____________`

---

## Step 5 — Commit

```bash
git add AGENTS.md
git commit -m "Module 8 lab: add AGENTS.md for agent guidance"
```

- [ ] Committed on `module8-lab`; hash `____________`

---

## Evidence

- README vs. AGENTS.md split table
- `AGENTS.md` + verified commands
- Fresh-chat transcript (Step 3)
- Precedence prediction + outcome + revert screenshot (Step 4)

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Agent ignores `AGENTS.md` in a new chat | File not at repo root, or chat opened outside the repo workspace | Move to repo root; confirm the workspace root is `<sandbox-repo>` |
| `AGENTS.md` commands don't work | Drifted from reality | Run them; fix the file — an agent-facing doc must be executable truth |
| Precedence test shows the user rule winning | Build-specific behavior or ambiguity in the conflict | Don't fight it: record the observed behavior, note it as a finding, and rely on explicit phrasing in the project artifact; escalate to facilitator |
| File growing past one pass | You're duplicating docs | Move detail to linked docs; keep AGENTS.md to commands, conventions, guardrails |
| Monorepo confusion | Multiple `AGENTS.md` files | In a monorepo, nested files scope to their package and the closest file to the edited code wins — call out your layout |

---

## Checkpoint questions

1. How is `AGENTS.md` different from `README.md` in purpose and audience?
2. If a user-level preference conflicts with a project-level rule, which wins, and why?
3. Why can the same conventions live in both `AGENTS.md` and `.cursor/rules/` — and when would you choose which?

<details>
<summary>Answers</summary>

1. README is written for human contributors (purpose, setup, usage); AGENTS.md is written for AI agents — build/test commands, conventions, and guardrails an agent needs to work correctly in the repo (any capable agent can read it, not just Cursor).
2. The project-level rule wins — more specific scope takes precedence, because it reflects what's actually true and required for that particular codebase.
3. `AGENTS.md` is universal, plain-text, and read by any agent; `.cursor/rules/` gives Cursor granular scoping (globs, always/intelligent/manual). Choose AGENTS.md for repo-wide essentials; rules for file-scoped or conditionally-loaded instructions.

</details>

---

## Next

**Lab 8.3** — package a reusable capability as a Skill, add a parameterized prompt template, and commit the starter kit.

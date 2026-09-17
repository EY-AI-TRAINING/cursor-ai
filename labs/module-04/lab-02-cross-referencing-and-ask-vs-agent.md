# Lab 4.2 — Cross-Referencing Specs & Choosing Ask vs Agent

**Module 4 · AI Chat, Context & Ask Mode | Xebia — Cursor AI Training**
Day 1 · Lab 2 of 3 · ~15–20 minutes · Individual · Read-only (observe Agent, discard changes)

> **Objective:** use `@`-mentions for the analysis pattern that requires evidence — cross-referencing a spec against
> its implementation with verifiable citations — then classify scenarios and watch the Ask vs Agent boundary: one
> reads, the other acts.

**Guide references:** Module 4, §2 (@-mentions), §3 (Chat/Ask vs Agent modes)
**Learning objectives covered:** 2 — `@`-mentions for files/docs/symbols; 3 — choosing correctly between Ask and Agent.

---

## Before you start

- Module 3 complete; chat and Agent panels available
- Choose your cross-reference pair from the sandbox:
  - `<spec-doc>` — a requirement source: the sandbox SRS/SDS, a coding standard, or the repo's documented conventions
  - `<target-file>` — the code that implements (or should implement) that requirement
- Mention note: local spec files are attached as `@`-**file** mentions. `@docs` is for **connected documentation
  sources** (Cursor's Docs feature) — if your team has one connected, use it; otherwise attach the file.

---

## Step 1 — Cross-reference: spec vs implementation

1. Open a new chat and attach both files: `@<target-file> @<spec-doc>`.
2. Use the analysis-prompt template from guide §6 (adapted to your pair):

   > "@`<target-file>` @`<spec-doc>` — Check `<the behavior>` against sections `<X.Y–X.Z>` of `<the standard/spec>`.
   > For each requirement, cite the line(s) that satisfy or violate it, or state 'not addressed' if you find no
   > evidence either way."

3. Send it. Then **verify every citation**: open each cited line and confirm it says what the answer claims.
   An unchecked citation is just a more convincing guess.

- [ ] At least one requirement checked with verified line citations
- [ ] At least one "not addressed" or gap identified (or a recorded explanation of why none exists)

---

## Step 2 — Force the honesty check

1. Ask a follow-up the evidence cannot support:

   > "And does it also comply with section `<N>`? If you find no evidence, say 'not addressed' rather than assuming."

2. Record whether the model declines or guesses. This is the seed of the "no unsupported facts" guardrail
   formalized in Modules 12–13.

- [ ] Behavior recorded: declined / guessed / needed a re-anchor

---

## Step 3 — Classify: which mode would you use?

Using the decision flow from guide §3 — answer only → **Ask/Chat**; multi-file edits or tools → **Agent**;
complex/ambiguous → **Plan** — fill in the table before you test it in Step 4:

| Scenario | Ask / Chat | Agent | Plan | Why |
|---|---|---|---|---|
| Explain what `generate_invoice()` does | | | | |
| Rename a function used across 40 files | | | | |
| Why is the checkout flow slow? | | | | |
| Add input validation to the signup form (well-scoped) | | | | |

- [ ] All four scenarios classified with a one-phrase justification

---

## Step 4 — Watch the boundary: same request, Ask vs Agent

1. **Ask mode:** open a new chat in Ask and request a small change — for example, *"Add input validation to the
   signup form"* (or a sandbox-appropriate equivalent). Observe: it explains and may propose a diff for you to
   apply, but it does not go edit files or run tools on its own. Record what actually happened.
2. **Agent mode:** send the **identical** request in a new chat in Agent mode. Observe: it proposes multi-file
   changes, shows a diff review, and may trigger terminal/tool approval prompts (Module 3's gates). Record what
   actually happened — including any approval prompt and what it asked for.

- [ ] Ask behavior recorded (explanation / suggested diff only)
- [ ] Agent behavior recorded (multi-file diff, review UI, any approval gates)

---

## Step 5 — Discard and confirm the sandbox is untouched

1. Reject all proposed changes from the Agent run — use the reject-all affordance in the diff review, or
   `Cmd/Ctrl+Backspace` in the chat panel (reject all changes).
2. Verify in the terminal:

   ```bash
   git status
   ```

3. It must match the state from Module 3 — nothing applied, nothing staged.

- [ ] All proposed changes rejected/discarded
- [ ] `git status` clean (or unchanged from the pre-lab state)

---

## Evidence

- Citation verification notes (claim → cited line → verified yes/no)
- The completed scenario classification table
- Your Ask vs Agent behavior notes
- Screenshot: clean `git status` after discarding the Agent proposal

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Ask mode suggests a big apply-able diff | Some builds surface "apply" affordances in chat | Treat it as read-only; don't apply |
| Agent edits files immediately without a diff prompt | Agent may write workspace files without approval (config files excepted) | Reject all changes (`Cmd/Ctrl+Backspace`), then verify `git status` |
| `@docs` shows nothing | No connected docs source | Use `@`-file for local spec docs; `@docs` connects in Modules 12–13 |
| Agent asks to run a terminal command | Module 3's approval gates working as designed | Deny — this lab needs no execution |
| Citations look plausible but don't match | Model approximation | That's why you verify; note it as a finding, not a failure |

---

## Checkpoint questions

1. In one sentence, when should you reach for Agent mode instead of Chat/Ask mode?
2. Why is defaulting to Agent mode "just in case" a bad trade?
3. What did the cross-reference prompt force the model to expose, and why does that matter for analysis tasks?

<details>
<summary>Answers</summary>

1. When the task requires editing multiple files or executing tools/commands — not merely explaining or answering.
2. It trades away the read-only, low-risk guarantee of Ask for no reason — Agent carries higher risk and needs
   diff review discipline; pick the mode that matches the actual need.
3. Evidence: per-requirement citations (or an explicit "not addressed"). Analysis failures produce confident wrong
   opinions with no built-in check — citations make the answer verifiable.

</details>

---

## Next

**Lab 4.3** — build a strong analysis prompt, test its honesty clause, and manage context limits in long threads.

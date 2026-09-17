# Lab 3.3 — Trust, Permissions, Model Selection & Your First Agent Command

**Module 3 · Cursor Interface & Setup | Xebia — Cursor AI Training**
Day 1 · Lab 3 of 3 · ~15–20 minutes · Individual, facilitator-supervised (real approval prompts are triggered)

> **Objective:** exercise the safety machinery *before* you ever let an agent run something — workspace trust →
> permission scoping → the approval prompt itself — then validate the entire chain with one deliberately trivial
> agent command. This is the module's "setup and workspace validation" in action.

**Guide references:** Module 3, §4 (Model Selection & Basic Agent Configuration), §5 (MCP at workspace level), §6 (Workspace Trust, Permissions, Safe Tool Execution)
**Learning objectives covered:** 4 — model selection and basic agent configuration; 5 — MCP at workspace level, conceptually; 6 — workspace trust, permissions, and safe tool execution.

---

## Step 1 — Workspace trust (the outer gate)

Two independent checks gate any agent tool execution (guide §6):

1. **Workspace trust** — is this folder trusted at all?
2. **Permission scoping** — does this specific command match an auto-run allowlist, or does it need your explicit approval?

Cursor inherits VS Code's Workspace Trust. Depending on your install and org policy, one of these applies:

- **Trust prompts appear** (enabled locally, or enforced by IT/MDM): opening a new folder asks Normal vs Restricted.
  Choose **Normal / "Yes, I trust the authors"** for the training repo. Restricted mode limits AI features and blocks
  agentic execution — the protective boundary the guide describes.
- **Trust is disabled** (Cursor's default unless enabled or MDM-enforced): your active guardrails are the approval
  prompts and command sandboxing you'll exercise in Step 6. Record that, because the two-layer *concept* still
  governs how you reason about safety.

Check your posture: Command Palette → search `Workspace Trust`.

> **Trust boundary rule:** only trust repos you'd already run code from. Trusting a folder means the agent's blast
> radius now includes that folder.

- [ ] Training workspace is in trusted/normal mode — or trust is disabled by policy and that is recorded
- [ ] Can explain what changes for agent execution between trusted and restricted

---

## Step 2 — Locate the permission controls (do NOT change anything)

1. Open Cursor Settings → search `Run Mode` or `auto-run`. In current builds this is
   **Settings → Agents → Approvals & Execution**.
2. Read the available Run Modes (Cursor ~3.6):
   - **Auto-review** — default. Allowlisted calls run immediately; supported shell commands run sandboxed when possible;
     everything else goes through a safety classifier or asks you.
   - **Allowlist** — only commands you've listed run without approval.
   - **Run Everything** — no prompts at all. **Do not use in this course.**
3. Note the defaults: terminal commands require approval by default; workspace file edits generally don't; config
   files do.
4. Know where the allowlist can live as code (this is the workspace-asset angle from the guide):
   - `<repo>/.cursor/permissions.json` — project-shared; commit it so the team gets the same behavior.
   - `~/.cursor/permissions.json` — personal; applies to all projects on your machine.
   - Relevant fields: `terminalAllowlist`, `mcpAllowlist`, `autoRun`.
5. Sandboxing: shell commands may run sandboxed — workspace + `/tmp` access, no arbitrary network. That is different
   from approving raw execution on your machine.

> **Security note (Cursor docs):** Run Modes and allowlists are best-effort guardrails, **not a hard security
> boundary** — which is why rules, hooks, and quality gates exist (Modules 14 and 17).

- [ ] Located the Approvals & Execution / Run Mode screen — screenshot for reference
- [ ] Recorded the active Run Mode (without changing it): `____________`
- [ ] Know both `permissions.json` locations
- [ ] Changed nothing

---

## Step 3 — Locate MCP management (awareness only — connect nothing)

Per the module guide (§5, §7), connecting MCP servers is **not** part of this exercise — the sandbox MCP instance
(repository, docs, ticketing) is pre-staged before Half-Day 4, and full configuration is Modules 12–13.

1. Cursor Settings → search `MCP` (may appear under Tools / Customize / MCP depending on build). Note any servers
   already present — there may be none.
2. Know the configuration locations: `.cursor/mcp.json` (project-specific) and `~/.cursor/mcp.json` (global).
3. Know the approval rule: MCP connections and every MCP tool call require approval unless explicitly allowlisted.

- [ ] Can find the MCP screen and both `mcp.json` locations
- [ ] Connected nothing — noted that the sandbox instance arrives Half-Day 4

---

## Step 4 — Model selection (a real engineering trade-off)

1. Open the Chat/Agent Panel. Find the model selector; cycle models with `Cmd/Ctrl+/` or click the picker directly.
2. Confirm at least one model is available. Short or locked list? That's org model policy, not a bug (Lab 3.1).
3. Run a read-only comparison in **Ask** mode. Ask the same question twice — once with a fast/light model, once with
   a frontier model:
   > "In one sentence, what does this repository do?"
4. Compare latency and depth. Then record when you'd pick each (guide §4 trade-off table: quick scoped questions vs
   complex multi-file reasoning vs high-volume repetitive work).

- [ ] Model selector shows at least one available model
- [ ] Same question asked with two different models; one sentence recorded on when to pick each

---

## Step 5 — Mode selector (read-only vs execute)

1. Open the mode menu (`Cmd/Ctrl+.`) or rotate with `Shift+Tab`. Switch through **Ask → Chat → Agent**.
   (Plan and Debug exist too — Modules 7 and 9 give them their own treatment.)
2. Observe the panel change: Ask answers read-only; Chat converses and suggests edits; Agent proposes multi-file
   edits and tool execution. The mode selector is the single most important control in the interface (guide §2).

- [ ] Switched through Ask/Chat/Agent
- [ ] Can state which mode is read-only and which one executes

---

## Step 6 — First agent command: validate the chain, watch the gates

The course validates setup with one deliberately trivial agent command. Do 6a and 6b in order — facilitator watching.

**6a — Read-only validation (Ask mode).** Ask:
> "What is the purpose of this repository? Cite the files you read."

Confirm the answer is grounded in actual repo files — that's context grounding working end to end.

**6b — Executing validation (Agent mode).**

1. Ask the agent: *"Run `git status` in the terminal and tell me the current branch."*
2. An **approval prompt** for the terminal command should appear (unless the command is allowlisted or
   sandbox-auto-run under your Run Mode). Read the command before approving. Approve it.
3. Confirm the agent reports the current branch.
4. Now exercise the **deny path**: ask for a second trivial command and **deny** the prompt when it appears
   (for example: *"Fetch `https://example.com` and show me the first lines."* — network access is blocked by the
   sandbox by default, and you will deny it). Observe: the agent must not execute; it should revise its approach or
   stop and ask again — the denial branch of the guide's decision flow.
5. Narrate the two layers you just exercised: **workspace trust** (outer) → **allowlist / approval** (inner) →
   execute or deny.

- [ ] Grounded answer in Ask mode, with file citations
- [ ] Approval prompt appeared for a terminal command; command was read before approving
- [ ] Approved path executed and produced the expected output
- [ ] Denial path observed — no execution, agent revised or re-asked
- [ ] Can narrate: trust → allowlist/approval → execute or deny

---

## Evidence (for your own record — no submission)

- Screenshot of the approval prompt (or the recorded auto-run reason if no prompt appeared)
- Screenshot of the Run Mode screen you located in Step 2
- Your one-sentence notes from Steps 1, 2, and 4

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| No approval prompt for the terminal command | The command matched the allowlist or was auto-run in the sandbox | Record the Run Mode; still attempt the deny-path command; do **not** disable guardrails to force a prompt |
| Agent can't execute or edit anything | Workspace restricted (untrusted) or you're in Ask mode | Recheck Step 1; ensure Agent mode (Step 5) |
| Prompt appears for network access | Expected — sandbox blocks arbitrary network by default | Deny it (that's Step 6b); note the guardrail |
| Model picker grayed out or list locked | Team policy (enforced Auto/model access) | Note it in your lab notes; skip the comparison |
| MCP server list is empty | Expected — MCP arrives Half-Day 4 | No action |
| Second command ran without a prompt | It matched the allowlist/sandbox behavior | Fine — record it; the gate behavior is the lesson |

---

## Checkpoint questions

1. Trace the agent's decision flow for running a command (guide §6): trusted? → allowlisted? → execute / approve / deny.
2. Why is the approval prompt a feature rather than friction?
3. Which layer of configuration — user or workspace — would carry a team's `terminalAllowlist`, and how would it be shared?
4. Where will you return to change Run Mode behavior later in the course?

<details>
<summary>Answers</summary>

1. Workspace must be trusted → the specific command either matches the auto-run allowlist (executes) or prompts →
   you approve (executes) or deny (agent must revise). Two independent checks, in that order.
2. It is the human-in-the-loop checkpoint made concrete at tool-execution level — probabilistic systems can take a
   wrong action confidently, and the prompt is where you catch it.
3. Workspace: `<repo>/.cursor/permissions.json`, committed to the repo so the whole team shares the behavior.
4. Modules 14 (governance/security) and 17 (hooks, quality gates) revisit Run Modes and approvals.

</details>

---

## Next

**Module 4 — AI Chat, Context & Ask Mode** puts this validated workspace to work: chat, `@`-mentions, and context scoping.

# Lab 6.2 — Gate the Agent's Terminal Commands: Approve, Deny, Observe

**Module 6 · Codebase-Aware Editing & Agent Mode | Xebia — Cursor AI Training**
Day 2 · Lab 2 of 3 · ~10–15 minutes · Individual, facilitator-supervised

> **Objective:** make Module 3's trust boundary operational. Watch the agent propose terminal commands, record how
> each one is gated, approve a safe execution, deny an unnecessary one, and observe what the agent does when
> it's told no.

**Guide reference:** Module 6, §4 (terminal/tool execution safely during agentic changes)
**Learning objectives covered:** 4 — explain how terminal/tool execution is gated and reviewed.

---

## Before you start

- Lab 6.1 in progress or complete (agent run available to observe) — or start a small new agent task for this lab
- Module 3's Run Mode screen located (you do **not** change it)
- Keep the same branch (`module6-agent-lab`); there's nothing new to commit here

---

## Step 1 — Set up the observation

1. If you're starting a fresh task, use a small agent instruction that requires verification, e.g.:

   > "Run the test suite and report which tests fail, if any. Make no code changes."

   The agent will want to execute `<test-command>` — exactly what this lab needs.
2. Open the Run Mode screen in another pane as a reference: Cursor Settings → search `Run Mode` / `auto-run`
   (current builds: **Settings → Agents → Approvals & Execution**).

- [ ] A task is queued that requires at least one terminal command
- [ ] Run Mode screen located (unchanged) — active mode: `____________`

---

## Step 2 — Record every command against the gate (the core exercise)

For each command the agent proposes, fill in one row **before** deciding:

| # | Command proposed | Purpose | Gated how? (auto / prompt / sandboxed) | Your decision | Outcome |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

Gate rules you're applying (Module 3 §6 and Module 6 §4):

- **Trusted workspace** is the outer gate — no agentic execution without it.
- **Auto-run allowlist / sandbox / classifier** decide whether a command runs without asking.
- Anything not allowlisted prompts; anything destructive, network-sensitive, or outside the workspace should stay
  behind an explicit approval.

- [ ] At least two commands recorded with their gate path
- [ ] Noted whether your build auto-ran, sandboxed, or prompted for each

---

## Step 3 — Approve one safe execution

1. When a safe, expected command appears (e.g., running the existing test suite), **read it first**, then approve.
2. Confirm the output was fed back into the agent's context and it used the result (e.g., reported failing tests).

- [ ] One command read, approved, and its output observed feeding the agent's next step

---

## Step 4 — Deny one unnecessary execution

1. Trigger a command the task doesn't need — most reliably, ask for something whose obvious implementation
   requires installing a package:
   > "Add human-readable date formatting to the exporter and install whatever library you need."
2. When the install command (`pip install ...` / `npm install ...` / equivalent) is proposed, **deny it**.
3. Observe the fallback (guide §4): the agent should proceed without running it, choose a no-dependency approach,
   or ask you to run it manually. Record what it actually did.
4. If your Run Mode never prompts (everything auto-runs or sandboxed), record that policy behavior and still deny
   via the stop/cancel affordance — do **not** change Run Modes to force a prompt.

- [ ] Deny path exercised; fallback behavior recorded
- [ ] No package was actually installed

---

## Step 5 — Close the loop

1. Verify the sandbox is unchanged by the denied action (e.g., no new dependency in the manifest):

   ```bash
   git status
   git diff <manifest-file>
   ```

2. Write your one-sentence rule of thumb for this project: which commands would you allowlist without thinking,
   and which should always prompt? `____________`

- [ ] Denied action left no trace; rule of thumb recorded

---

## Evidence

- The completed command gate table (Step 2)
- Screenshot of the approval prompt you approved **or** denied
- Recorded fallback behavior after the denial (Step 4)

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| No prompt ever appears | Run Mode auto-runs/sandboxes the commands (by design) | Record that; still exercise the deny path via stop/cancel; don't change Run Modes |
| Agent doesn't propose any command | Task doesn't need one | Use the Step 1 instruction (run tests and report) |
| Install command was allowlisted and ran | Project allowlist includes package managers | Revert the manifest change, note the allowlist behavior, and raise it for the team (Module 14/17 topic) |
| Agent ignores the denial and retries the same command | It was told to install | Re-instruct: "Do not install anything; use only what's available" |
| Prompt shows a command you don't recognize | Exactly why the gate exists | Deny; ask the agent to explain the command and its purpose first |

---

## Checkpoint questions

1. What determines whether an agent's terminal command runs automatically or waits for your approval?
2. Why is the approval prompt a *feature* of agentic workflows rather than friction (Module 3 §6)?
3. Where do allowlists and Run Modes become team-wide policy, and where do hooks re-enter the picture?

<details>
<summary>Answers</summary>

1. Whether the command matches the workspace's auto-run allowlist / sandbox behavior configured under
   Settings → Agents → Approvals & Execution; anything else prompts for explicit approval.
2. Probabilistic systems can take a wrong action confidently — the prompt is the human-in-the-loop checkpoint at
   the exact moment an action leaves the editor and touches the system.
3. Run Modes can be enforced centrally at the team level (Module 14 governance); hooks and automated quality
   gates build on this gate in Module 17.

</details>

---

## Next

**Lab 6.3** — contain the blast radius: open-ended vs. tightly scoped instructions, and decomposition into reviewable steps.

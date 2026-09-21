# Lab 14.2 — Gate the Risky Call and Log It

**Module 14 · Governance, Security & Observability | Xebia — Cursor AI Training**
Day 4 · Lab 2 of 3 · ~10 minutes · Individual or pairs

> **Objective:** apply the safe-execution stack to real tool calls. Classify nine requests as retrieval or
> execution, run the riskiest execution call through **controlled tool access → permission → sandboxing →
> approval**, define its approval checkpoint, and design the audit-log entry that proves — after the fact —
> what was granted and what actually happened.

**Guide references:** Module 14, §2 (admin controls and audit logs), §3 (safe execution); Module 12 §7 (retrieval vs. execution)
**Learning objectives covered:** 2 — audit logs and access scoping for tool use; 3 — approvals, permissions, sandboxing, controlled tool access.

---

## Before you start

- Lab 14.1 complete: `governance/access-policy.md` written, approval boundary stated
- Open [`samples/tool-call-requests.md`](samples/tool-call-requests.md)
- No runner needed — this is a design exercise on the Module 13 agent's tool surface

---

## Step 1 — Classify: retrieval or execution?

Fill the table for all nine calls:

| # | Tool call | Retrieval / execution | Why | Gate needed? |
|---|---|---|---|---|

- [ ] All nine classified; every execution call is identified
- [ ] You can state the rule you used (state-changing or external side effect = execution)

---

## Step 2 — Gate the riskiest execution call

Pick the riskiest execution call and walk it through the stack. Record the decision at each layer — including layers that don't apply:

| Layer | Applies? | Decision + why |
|---|---|---|
| Controlled tool access — is this tool approved to exist for this agent at all? | | |
| Permission — is this action reachable for this agent/team? | | |
| Sandboxing — does it need isolation to bound the blast radius? | | |
| Approval — does risk require a human before execution? | | |

- [ ] Every layer answered, including "not applicable" with a reason
- [ ] You can explain why the layers are independent (a gap in one still leaves the others standing)

---

## Step 3 — Define the approval checkpoint

Create `shared-agent-library/governance/approval-checkpoint.md` for the chosen call:

- [ ] **Who approves** — a named role (not "the team")
- [ ] **What they see before approving** — tool, arguments summary, intended effect, sources the agent used, and how to roll back
- [ ] **Denial path** — what the agent does instead (stop, report, propose an alternative — never retry silently)
- [ ] **Failure path** — what happens if the call fails halfway (state left behind, who is told)
- [ ] One line: why this call is gated while retrieval calls are not

---

## Step 4 — Design the audit-log entry

Create `shared-agent-library/governance/audit-log-schema.md` and fill one real example entry for the chosen call:

```text
timestamp:        <ISO-8601>
actor:            <who asked / which team>
agent:            <agent name + version>
tool:             <tool name>
args_summary:     <redacted summary — never secrets or full payloads>
sources_used:     <citations the agent relied on (Module 14 §5)>
permission:       granted | denied
sandbox:          used | not-needed
approval:         approved-by <role> | denied | not-required
outcome:          success | failure | reverted
cost:             <tokens + tool calls + $ for this call>
trace_id:         <links to the task trace (Lab 14.3)>
```

- [ ] Schema has every field above — including the §5 fields (sources used, cost); `args_summary` is explicitly a summary (no secrets, no full payloads)
- [ ] One filled example for the riskiest call
- [ ] A sentence distinguishing a **grant** entry (admin gave access) from a **use** entry (the agent actually used it) — the audit log needs both
- [ ] The destination is the observability location named in `access-policy.md`

---

## Evidence

- Classification table (nine calls)
- Gating table (four layers) for the riskiest call
- `shared-agent-library/governance/approval-checkpoint.md`
- `shared-agent-library/governance/audit-log-schema.md` + one filled entry

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Everything treated as execution | Retrieval/execution boundary blurred | Reads (file, search, defect fetch) are retrieval — low-risk, no approval gate |
| Approval placed on the read calls | Wrong side of the boundary | Gate the state-changing/external calls; retrieval stays frictionless |
| "The team approves" | No accountability | Name a role; the audit log needs a specific actor |
| Log entry stores full arguments | Convenience over exposure | `args_summary` only — full payloads can carry secrets or personal data |
| Only use entries logged | Grant history skipped | Log grants too: the review question is "who could reach this, and when did it actually" |
| Sandbox marked n/a for a code edit | Blast radius ignored | A permitted edit still runs somewhere — worktree/scratch isolation bounds it |

---

## Checkpoint questions

1. What does a permission check decide that a sandbox does not?
2. Why do grant entries and use entries both belong in the audit log?
3. Why does the approval checkpoint need a denial path, not just an approval path?

<details>
<summary>Answers</summary>

1. Permission decides *whether* a call is allowed at all; sandboxing decides *how* it runs — isolated so a permitted-but-wrong action has a bounded blast radius instead of touching production directly.
2. A grant entry records who could reach what; a use entry records what actually happened. Security review needs both to answer "was this access justified, and was it exercised?"
3. Without one, a denied approval leaves the agent to improvise — silently retrying or working around the gate. The denial path makes stopping and reporting the defined behavior.

</details>

---

## Next

**Lab 14.3 — Trace the Handoffs and Cost.** One call is logged; a task is a chain of them. You'll repair a flawed handoff log, define the fields every stage must emit, and put a number on what the task cost.

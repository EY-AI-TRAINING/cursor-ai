# Lab 19.1 — Connect the Ticket Source Without Losing Control

**Xebia — Cursor AI Training | AI-Assisted Software Engineering**
Day 6 · Module 19 · Lab 19.1 of 8 · ~8 min · Concept demo + hands-on (individual or pairs)

> **Objective:** connect the pipeline to its system of record without giving an agent more access than
> the work needs. Review a draft MCP configuration that violates every least-privilege decision, then
> write a sandbox-scoped, secret-free `.cursor/mcp.json` and a `beforeMCPExecution` policy hook that
> allows read tools, asks for writes, denies the rest — and fails closed.

**Guide reference:** §1 Connecting Cursor AI/Agents to Jira or Azure DevOps via MCP · §9 task 1
**Learning objectives covered:** 1 (MCP with least-privilege, sandboxed access)

## Before you start

| Need | Notes |
|---|---|
| Module 18 complete on `module18-lab` | The pipeline, `gates.yaml` v1.1.0, hash-bound approval |
| Ticketing path | **Path A** — sandbox Jira/ADO project; **Path B** — the [mock-ticket kit](samples/mock-ticket-kit/README.md) (stdlib, offline) |
| Draft to critique | [`samples/mcp-config-draft.json`](samples/mcp-config-draft.json) |
| Files you will create | `<pipeline-root>/.cursor/mcp.json`, `.cursor/hooks/mcp-policy.sh`, and a `beforeMCPExecution` entry in `.cursor/hooks.json` |
| Field-name warning | Hook payloads and tool names differ by vendor and Cursor release — **check the current docs**; the patterns below are the shape, not the contract |

---

## Steps

### Step 1 — Critique the draft configuration (≥6 problems)

Read the draft and list every problem: *problem → why it fails → corrected decision*. Record it in
`notes/module19/mcp-review.md`. Review it against the four connection decisions:

| Decision | The safe default |
|---|---|
| **Which project** | A sandbox project with synthetic tickets — never production |
| **Which identity** | A dedicated service/bot account or a scoped OAuth session — audit logs say "agent via MCP", not a colleague's name |
| **Which tools** | Read-only by default; writes (comment, transition) behind a hook that asks a human |
| **Which credential** | OAuth or a scoped token with minimal scopes and short expiry, from the OS keychain or env — **never** in `mcp.json` committed to Git |

### Step 2 — Write the real `.cursor/mcp.json`

Start from the mock entry (Path B) or your sandbox server (Path A); drop everything else:

```json
{
  "mcpServers": {
    "tickets-mock": {
      "command": "python3",
      "args": ["tools/mock_ticket_mcp.py", "--fixtures", "tickets/"]
    }
  }
}
```

- [ ] If Path A: the URL/org is the **sandbox**, the identity is a dedicated bot/OAuth session, and any
      token is referenced as `${env:JIRA_TOKEN}` or from the keychain — **no literals anywhere**
- [ ] The file is safe to commit: `grep -nE "pat_|token.*[A-Za-z0-9]{12}|password" .cursor/mcp.json`
      returns nothing
- [ ] No write authority is implied by a comment or notes field — writes are controlled by the hook, not by prose

### Step 3 — Build the policy hook: allow reads, ask writes, deny the rest, fail closed

Create `.cursor/hooks/mcp-policy.sh` (guide §1 shape; adapt tool names to your server):

```bash
#!/usr/bin/env bash
# Allow read tools; ask for writes; deny everything else. Fail-safe: deny.
set -euo pipefail
trap 'echo "{\"permission\":\"deny\",\"userMessage\":\"mcp-policy error — denied (fail-safe)\"}"; exit 0' ERR
tool="$(python3 -c 'import json,sys; print(json.load(sys.stdin).get("tool_name",""))')"
case "$tool" in
  *get_ticket*|*search_tickets*|*getJiraIssue*|*searchJiraIssuesUsingJql*|*wit_get_work_item*)
    echo '{"permission":"allow"}' ;;
  *add_comment*|*addCommentToJiraIssue*|*wit_add_work_item_comment*|*transition*)
    echo '{"permission":"ask","userMessage":"Agent wants to write to a ticket — review the text first."}' ;;
  *)
    echo '{"permission":"deny","agentMessage":"Ticket tool not allowed in this pipeline."}' ;;
esac
```

- [ ] Register it in `.cursor/hooks.json` under `beforeMCPExecution` (the Module 17 hook file gains a fifth event)
- [ ] Every decision appends to `runs/hook_log.jsonl` — the script above echoes decisions; add the log
      line as in Module 18's `shell-policy.sh` (a write tool that was *asked* or *denied* must be visible)
- [ ] Unknown or missing tool names fall to **deny**, and an error in the script itself also denies

### Step 4 — Prove it

```bash
chmod +x .cursor/hooks/mcp-policy.sh
echo '{"tool_name": "get_ticket"}'          | .cursor/hooks/mcp-policy.sh   # allow
echo '{"tool_name": "add_comment"}'         | .cursor/hooks/mcp-policy.sh   # ask
echo '{"tool_name": "transition_issue"}'    | .cursor/hooks/mcp-policy.sh   # deny
echo 'not-json'                             | .cursor/hooks/mcp-policy.sh   # deny (fail-safe)

# pull the ticket the pipeline will use (Path B)
python3 tools/mock_ticket_mcp.py --fixtures tickets/ --call get_ticket --arg id=REQ-2481 > /dev/null \
  && echo "ticket pulled"
```

- [ ] Four decisions observed and logged: allow / ask / deny / deny-on-error
- [ ] The write attempt is **not** performed silently; the ask message tells the human what to review
- [ ] REQ-2481's payload arrives (summary, status, comments) — the raw ticket is now available to the
      bundle builder in Lab 19.2

---

## Evidence

- `.cursor/mcp.json` (sandbox-scoped, no secrets) + `notes/module19/mcp-review.md` with the draft's ≥6 problems
- `.cursor/hooks/mcp-policy.sh` + its `beforeMCPExecution` registration
- `runs/hook_log.jsonl` lines for allow / ask / deny / error
- The pulled REQ-2481 payload (or a one-line note that the sandbox ticket was fetched)

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Hook never fires | `beforeMCPExecution` not registered, or your Cursor version names the event differently | Check current docs; the terminal proofs above work regardless |
| Every tool is denied | Payload field is not `tool_name` in your version | Print the raw payload once and adapt the parser |
| Script denies on valid input | `set -euo pipefail` plus a failing `python3` parse | The trap should deny — fix the parser, not the trap |
| Mock server exits immediately | Run from the wrong directory | `--fixtures tickets/` is relative to `<pipeline-root>`; copy the kit first |
| Tool names don't match the patterns | Vendor naming differs | Add your server's actual names to the allow/ask arms — never widen the catch-all |

## Checkpoint questions

<details>
<summary>Why read-only by default, and how do you enforce it without trusting the agent?</summary>

Writes to the system of record are outward-facing and hard to retract, and the pipeline has no business
changing ticket state mid-run. Enforce it with the `beforeMCPExecution` allow-list (read → allow,
write → ask, rest → deny, error → deny) plus a token/OAuth scope that limits the account to the sandbox
project. The agent's good behaviour is not a control.
</details>

<details>
<summary>What does a dedicated bot identity buy you that your own account does not?</summary>

Attributable audit logs ("agent via MCP", not a colleague's name), blast-radius isolation (revoking the
bot does not lock out a person), and scoped credentials that can expire without disrupting humans. It
also keeps the agent out of any personal access the account might carry.
</details>

<details>
<summary>Why does the hook fail closed on a parse error instead of allowing?</summary>

An unparseable payload means the policy layer is broken, not that the tool is safe. Fail-safe defaults
are Module 17's rule: when the checker fails, the answer is not "allow". The deny is logged so the
control-plane failure is visible.
</details>

---

*Next: Lab 19.2 — Ticket → Requirement Bundle, where the raw issue becomes schema-valid structured input with provenance and quarantined untrusted text.*

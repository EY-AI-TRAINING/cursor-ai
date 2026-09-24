# Mock ticket kit — Jira/ADO-shaped fixtures with zero infrastructure

> **Path B for Module 19.** Use this when no sandbox Jira/ADO project is available, or when you want
> every proof to run from the terminal. It is the guide's §1 **Option C** — enough to complete every
> exercise in this module and the capstone. Python standard library only; no installs.

## What is in the kit

| Path | What it is |
|---|---|
| `tools/mock_ticket_mcp.py` | An MCP stdio server (JSON-RPC 2.0) plus a `--call` terminal client |
| `tickets/REQ-2481.json` | Order cancellation — structured ACs, **a planted injection comment**, status `Ready for Dev` |
| `tickets/REQ-2482.json` | Refund lookup for unknown orders — **prose ACs** (exercises the LLM-assisted split), status `Ready for Dev` |
| `tickets/REQ-2490.json` | Bulk cancellation — status `In Progress` (exercises the not-ready stop) |

Tools exposed: `get_ticket`, `search_tickets` (read) · `add_comment` (write; fixture mode never persists).

## Set up your pipeline repo

From your lab pack folder, with `<pipeline-root>` set to your `requirement-to-test/` workspace:

```bash
mkdir -p <pipeline-root>/tools <pipeline-root>/tickets
cp samples/mock-ticket-kit/tools/mock_ticket_mcp.py <pipeline-root>/tools/
cp samples/mock-ticket-kit/tickets/*.json          <pipeline-root>/tickets/
```

Wire it into `.cursor/mcp.json` (Option C from the guide):

```json
{
  "mcpServers": {
    "tickets-mock": { "command": "python3", "args": ["tools/mock_ticket_mcp.py", "--fixtures", "tickets/"] }
  }
}
```

## Terminal proofs (no Cursor needed)

```bash
# list the tools the server exposes
python3 tools/mock_ticket_mcp.py --fixtures tickets/ --list-tools

# pull the ticket — the lab's first proof
python3 tools/mock_ticket_mcp.py --fixtures tickets/ --call get_ticket --arg id=REQ-2481

# search
python3 tools/mock_ticket_mcp.py --fixtures tickets/ --call search_tickets --arg query=cancel

# a write tool (the policy hook should ask; the fixture never persists)
python3 tools/mock_ticket_mcp.py --fixtures tickets/ --call add_comment \
  --arg id=REQ-2481 --arg text="pipeline opened PR #57"

# raw MCP handshake (what Cursor does on connect)
printf '%s\n' \
  '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"lab"}}}' \
  '{"jsonrpc":"2.0","method":"notifications/initialized"}' \
  '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' \
  | python3 tools/mock_ticket_mcp.py --fixtures tickets/
```

## What each fixture exercises

| Fixture | Exercises |
|---|---|
| `REQ-2481` | Structured AC field (`customfield_10044`) → deterministic parse; the injection comment → `warnings[]` + `untrusted_text`; links/attachments → `spec_refs`; revision (`updated`/`rev`) |
| `REQ-2482` | No structured AC field → LLM-assisted split marked `extracted_by: llm`, to be confirmed by the ticket owner |
| `REQ-2490` | `status: In Progress` → the pipeline must stop before any run starts |

## Rules

1. **Copy, don't edit the pack.** Files under `labs/module-19/samples/` are read-only fixtures.
2. **The injection comment stays in the fixture.** Do not delete it to make parsing easy — detecting it
   is the exercise.
3. **Fixture mode never persists writes.** The real control is the `beforeMCPExecution` policy hook plus
   the scoped identity; the mock simply proves the plumbing.

---

*Fixture for Module 19 — read-only in the lab pack. The ticket is the system of record; the bundle is the pipeline's structured view of it.*

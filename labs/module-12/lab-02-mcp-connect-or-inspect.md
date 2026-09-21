# Lab 12.2 — MCP: Connect or Inspect

**Module 12 · Context Engineering, Knowledge Grounding & MCP | Xebia — Cursor AI Training**
Day 4 · Lab 2 of 3 · ~20 minutes · Individual or pairs

> **Objective:** do walkthrough steps 2 and 5 — connect to (or inspect) an MCP server, identify its **Resources**
> and **Tools**, classify each capability on the retrieval/execution boundary, and match **retrieval strategies**
> to question shapes. Two paths: a live connection over your `knowledge/` corpus, or a guided inspection if the
> environment can't run a server.

**Guide references:** Module 12, §3 (MCP anatomy), §4 (retrieval strategies), §7 (retrieval vs. execution; mechanism choice); hands-on walkthrough steps 2 and 5
**Learning objectives covered:** 3 — MCP resources/tools/connections; 4 — retrieval strategy selection; 7 — retrieval vs. execution separation.

---

## Before you start

- Lab 12.1 complete: `knowledge/` populated, `notes/module12/grounding-setup.md` current
- Pick a path:
  - **Path A — Live connection** (needs `npx`/Node and network on first run): you'll configure the official **filesystem reference server** scoped to `knowledge/` only.
  - **Path B — Inspection** (no install, works offline): you'll inspect [`samples/mcp-config-example.json`](samples/mcp-config-example.json) and [`samples/mcp-capabilities-docs-server.md`](samples/mcp-capabilities-docs-server.md).
- **Safety rules for this lab:** the server is scoped to `knowledge/`; you will approve **read-only** tool calls only. Never approve write/delete/move calls. **No secrets in any config file** — remote servers use `${env:...}` interpolation.
- Create `notes/module12/mcp-notes.md`.

> Current Cursor configuration reference: project config `.cursor/mcp.json` (committable, shared with the team) and
> global `~/.cursor/mcp.json` (personal). Both are merged; on a name clash the project entry wins. Transports:
> `stdio`, SSE, Streamable HTTP. Manage servers from **Customize → MCP** (older builds: **Settings → MCP**).

---

## Step 1 — Configure the connection (Path A) or read the config (Path B)

**Path A:** create `<sandbox-repo>/.cursor/mcp.json` with the `knowledge-files` entry from the example (drop the
illustrative `docs-remote` entry, or keep it with a `${env:...}` token if your facilitator provided one):

```json
{
  "mcpServers": {
    "knowledge-files": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "${workspaceFolder}/knowledge"]
    }
  }
}
```

- [ ] Config written; JSON validates (no trailing commas); scope argument points at `${workspaceFolder}/knowledge` — nothing broader
- [ ] No literal secrets anywhere in the file

**Path B:** open both sample files and note the same points: where the config lives, the two transport styles, how scope is bounded, and how secrets are referenced.

- [ ] Config fields and scope boundary understood; capability sheet open for Step 3

---

## Step 2 — Verify the connection

- [ ] Restart or reload Cursor, then open **Customize → MCP** (older builds: Settings → MCP)
- [ ] Server shows **connected** (Path A) or "inspection mode — no live server" is recorded in `mcp-notes.md` (Path B)
- [ ] Note how tool approval works: Cursor asks before using MCP tools by default, and Run Modes apply to MCP tools like terminal commands

---

## Step 3 — Identify Resources and Tools; classify retrieval vs. execution

Build this table in `mcp-notes.md` (Path A: from the server's actual tool list; Path B: from the capability sheet):

| Capability | MCP kind (Resource / Tool) | Side: retrieval / execution | Allowed in this lab? |
|---|---|---|---|

- [ ] At least one **read-only Tool** identified (e.g., `read_file`, `search_files`) — a Tool can still be retrieval-side
- [ ] At least one **execution-capable Tool** identified (e.g., `create_ticket`, `write_file`) — recorded as **out of bounds** for this lab
- [ ] At least one **Resource** identified (from the capability sheet or your server) and distinguished from Tools
- [ ] One sentence in your notes: why retrieval and execution are different risk categories (Module 14 governs the execution side)

---

## Step 4 — Match retrieval strategies to question shapes

Choose **semantic search**, **structured lookup**, or **graph traversal** for each — and say why in one line:

| # | Question | Strategy | Why |
|---|---|---|---|
| 1 | "Find prior defects related to session timeout handling." | | |
| 2 | "Get the root cause recorded for defect DEF-118." | | |
| 3 | "Which services call the rate-limit middleware, and which tests cover them?" | | |
| 4 | "What does the gateway runbook say about `Retry-After`?" | | |
| 5 | "What value is `RATE_LIMIT_PER_MINUTE` set to in the production config?" | | |

- [ ] All five answered; #4 or #5 is a deliberate hybrid (two strategies could work) — state what tips your choice
- [ ] One row where using the *wrong* strategy would retrieve "confidently wrong" context — note the failure

---

## Step 5 — Mechanism check for a live lookup

- [ ] Name one question from Step 4 that genuinely needs **MCP** (external system or live lookup) and one that does not (already in-session or standing instruction)
- [ ] For the non-MCP one, state what you'd use instead and what maintaining an MCP server for it would cost (deck §08)

---

## Evidence

- `<sandbox-repo>/.cursor/mcp.json` (Path A) or inspection notes referencing the two sample files (Path B)
- `notes/module12/mcp-notes.md` — connection status, capability table with retrieval/execution classification, strategy table, mechanism check
- No write/delete tool call approved at any point

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Server won't start | `npx`/network unavailable, bad JSON, or path doesn't exist | Check JSON syntax (trailing commas break it), verify `knowledge/` exists, restart Cursor; if blocked, switch to Path B |
| Server connects but no Resources appear | Filesystem reference server exposes mostly **Tools** | Expected — classify its read tools as retrieval-side Tools and use the capability sheet for Resource examples |
| Write/delete tool prompt appears | Server is write-capable by design | Decline; this lab uses read-only calls only. Note the prompt itself as the governance hook Module 14 formalizes |
| `docs-remote` fails to connect | It's illustrative (`mcp.example.internal`) | Ignore or remove it; the live path only needs `knowledge-files` |
| Same server name in project and global config | Both files are merged | Project entry wins — remove the duplicate from one file to avoid confusion |
| Run Mode blocks tool execution | Run Modes apply to MCP tools | Approve the read-only call, or record the block and continue in Path B |

---

## Checkpoint questions

1. What is the difference between an MCP Resource and an MCP Tool?
2. When is graph traversal the right retrieval strategy?
3. Why keep retrieval and execution separate, even inside one task?

<details>
<summary>Answers</summary>

1. A Resource is readable content the agent can pull into context (no side effects); a Tool is a callable action that can change state or trigger something external.
2. When the question is about relationships, dependencies, or impact/lineage between connected entities — e.g., "what calls this API and what tests cover it" — rather than a fuzzy text match or an exact field lookup.
3. They carry different risk profiles: read-only retrieval is low-risk to allow broadly, while state-changing execution needs approval and audit controls (Module 14). Conflating them makes both harder to govern — and a read-only *Tool* being retrieval-side is exactly why the protocol kind and the risk side are different axes.

</details>

---

## Next

**Lab 12.3 — Grounded Answer & Refusal Test.** With the sources connected, you'll write the "no unsupported facts" rule, get a cited answer to GQ-1, spot-check the citations, and confirm the agent declines GQ-3 instead of fabricating a policy.

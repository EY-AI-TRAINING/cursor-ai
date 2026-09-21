# MCP server capability sheet — "docs" server (representative)

> **Fixture for Module 12 (Lab 12.2).** Use this when you take the **inspection path** (no live MCP server
> connected). It models the capability listing a docs/knowledge server would expose after connecting.

**Server:** `docs` · **Transport:** Streamable HTTP (`https://mcp.example.internal/docs`) · **Owner:** Platform team

## Resources (readable content the agent can pull into context)

| Resource URI | Content |
|---|---|
| `docs://sds/rate-limiting` | Approved SDS excerpt for rate limiting |
| `docs://standards/api-conventions` | Team API/interface standards (Module 8 rules) |
| `docs://runbooks/api-gateway` | Platform runbook for the API gateway |
| `defects://entries/{id}` | Historical defect entries, addressable by ID |
| `wiki://services/{service}/overview` | Internal wiki service overviews |

## Tools (callable actions)

| Tool | What it does | Read-only or state-changing? |
|---|---|---|
| `search_docs(query)` | Semantic search over indexed docs | |
| `get_page(uri)` | Fetch one page by URI | |
| `query_defects(component, since)` | Structured lookup over defect records | |
| `create_ticket(project, title, body)` | Create a tracker ticket | |
| `update_ticket(id, fields)` | Update tracker ticket fields | |
| `trigger_pipeline(pipeline, ref)` | Start a CI/CD pipeline run | |

**Classify each row** in Lab 12.2 Step 3: MCP protocol kind (Resource vs Tool) **and** whether it sits on the
retrieval (no side effects) or execution (changes state) side of the Module 12 §7 boundary. They are not the
same axis — a read-only *tool* is still a Tool, and an execution-capable tool is where governance (Module 14)
applies.

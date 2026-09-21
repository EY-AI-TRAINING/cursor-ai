# Agent access policy — DRAFT v0.1

> **Fixture for Module 14 (Lab 14.1).** A first draft, written in a hurry. Review it against the guide's four
> policy decisions (§7) and the control-plane model (deck §01–§08) — it has **at least six problems**. Do not
> edit the fixture; produce a corrected policy at `shared-agent-library/governance/access-policy.md`.

**Agent:** knowledge-grounded (Module 13) · **Owner:** API platform · **Status:** draft

## 1. Sources

- Sources are permitted unless someone objects during review. If a team is unsure about a source, they can
  raise it later.
- The knowledge-grounded agent may search anything under the repository root and the `knowledge/` directory.

## 2. File and folder access

- Team members are asked not to point the agent at `/legal`, `/hr`, or personal data stores.
- Restricted paths are handled case by case if they come up.

## 3. Secrets

- If a connector needs a token, paste it into `.cursor/mcp.json` so it works immediately; move it to a vault in
  a later iteration.

## 4. Approvals

- Any retrieval that touches more than one source requires a human approval before it runs.
- Tool execution is fine to allow by default; developers can revoke it afterward if something goes wrong.

## 5. Admin controls

- Each developer may add MCP servers and connect new sources for their own use — access is a local setting.

## 6. Observability

- Each team keeps its own logs wherever it prefers; traces are nice to have.
- Audit entries record that "the agent ran".

## 7. Data classification

- Sources are labeled **internal** by default. The defect log is internal and contains reporter email
  addresses — keep as is.

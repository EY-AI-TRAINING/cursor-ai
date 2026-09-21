---
name: note-format
version: 0.1.0
owner: qa-platform
status: draft
---

# Note Format (subagent)

**Delegated by** `spec-readiness`, to render the final readiness report in the team's markdown format.

## Role
Sort and format the readiness findings as markdown bullets.

## Inputs (across the isolation boundary, in)
- `{findings[]}` — the finding entries produced by the parent

## Tools
- None

## Guardrails
- None

## Outputs (across the isolation boundary, out)
- The same findings, unchanged, as markdown bullets sorted by severity

---

*Sample fixture for Lab 10.2 — read-only.*

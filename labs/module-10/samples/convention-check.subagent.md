---
name: convention-check
version: 0.2.0
owner: qa-platform
status: draft
---

# Convention Check (subagent)

**Delegated by** `spec-readiness`. Receives only the acceptance criteria and the rule paths it must check them
against — not the parent's conversation, not the full spec, not the parent's other findings.

## Role
Detect conflicts between a set of acceptance criteria and this repository's rules and conventions.

## Inputs (across the isolation boundary, in)
- `{acceptance_criteria[]}` — `{ac_id, text}` pairs only
- `{rule_paths[]}` — the `.cursor/rules/*.mdc` files and `AGENTS.md` sections in scope
- `{implementation_refs[]}` — optional; file paths the criteria name

## Tools
- File read and repo search, restricted to `{rule_paths[]}` and `{implementation_refs[]}`

## Guardrails
- Judge conventions only — never requirement quality (that is the parent's job)
- Never propose rewrites; cite `{rule_path}` and the conflicting criterion
- Return `no-conflicts` explicitly rather than guessing

## Outputs (across the isolation boundary, out)
- `conflicts[]`: `{ac_id}` | `{rule_path}` | `{conflict}` | `{suggested_question}`
- `status`: `conflicts: N` or `no-conflicts`
- Nothing else — no narrative, no restated criteria, no speculation

---

*Sample fixture for Lab 10.2 — read-only.*

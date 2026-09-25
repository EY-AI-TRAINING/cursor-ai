# Lab 20.2 — Stage 1: Pull REQ-2502 and Build the Requirement Bundle (CP1)

**Xebia — Cursor AI Training | AI-Assisted Software Engineering**
Day 7 · Module 20 · Lab 20.2 of 10 · ~25 min · Team (3–4)

> **Objective:** turn an unseen ticket into a schema-valid requirement bundle: deterministic
> mapping for the structured criteria, an **LLM-proposed, human-confirmed** AC for the prose
> sentence, untrusted text quarantined, and the injection warning recorded. No generation starts
> from a bundle that is not ready.

**Guide reference:** §1 Stage 1 — Pull the Ticket and Extract the Requirement Bundle
**Learning objectives covered:** 1 (unseen ticket → schema-valid bundle, clarifications raised and resolved)

## Before you start

| Need | Notes |
|---|---|
| Kickoff done | Lab 20.1: manifest, branch, sandbox reachable |
| Ticket source | Path A: sandbox Jira MCP · Path B: `tools/mock_ticket_mcp.py --fixtures tickets/` |
| Bundle tooling | Your Module 19 `tools/ticket_to_bundle.py` + schema, or hand-build against the kit's reference bundle |
| Clarification channel | Ticket owner available, or the kit fixture `tickets/REQ-2502-clarifications.md` |

---

## Steps

### Step 1 — Pull the ticket (read-only) and save the raw evidence

- [ ] `get_ticket REQ-2502` through the read-only MCP path (policy hook logs `allow`)
- [ ] Confirm: status `Ready for Dev`, revision `2026-09-26T07:58:00Z`, components `orders-api`
- [ ] Save the raw pull as `runs/req-2502-run-01/raw_ticket.json` — the report will link it

### Step 2 — Map the structured criteria deterministically

- [ ] AC-1…AC-3 extracted from `customfield_10044` with `source` + `extracted_by: parser`
- [ ] Ticket block carries `id`, `revision`, `url`, `status` (a mid-run edit must be detectable)
- [ ] `spec_refs` point at real locations in `specs/openapi.yaml` (`CancelRequest`, `AuditEntry`)
- [ ] If a reference cannot be resolved: **NEEDS_HUMAN**, never "infer it"

### Step 3 — Handle the prose criterion: propose, ask, confirm

"Cancellations should be auditable." is not a criterion yet.

| Step | What you produce |
|---|---|
| Propose | AC-4 with `extracted_by: llm`, `status: proposed` — the model's *claim* |
| Ask | Clarification questions CL-1…CL-n to the ticket owner (visibility, fields, ordering) |
| Confirm | Owner's answers recorded; AC-4 `status: confirmed`, `confirmed_by: human:<owner>`, `clarifications: [CL-1, CL-2]` |
| Park if needed | No answer in time → open issue, excluded from scope, listed in the report — never silently dropped |

- [ ] Prove G1 fails while AC-4 is `proposed`: run
      `python3 tools/sequence_gate.py --run req-2502-run-01` (it fails `G1_requirement_ready`)
- [ ] After confirmation, G1 passes — record both outputs

### Step 4 — Quarantine the untrusted text and finish the bundle

- [ ] The comment addressed to "AI agents" sits under `untrusted_text.comments_md` **and nowhere else**
- [ ] `warnings[]` names it: imperative text addressed to AI agents, ignored as instructions
- [ ] The comment changed nothing: no test was skipped, no ticket transition attempted
      (the MCP policy logs the denied `transition_issue` if you tried)
- [ ] Bundle validates against the schema; CP1 evidence recorded

---

## Evidence

- `runs/req-2502-run-01/raw_ticket.json` + `00_requirement_bundle.json`
- Clarification log (CL-1/CL-2) with the owner's confirmation and timestamp
- G1 output: FAIL while `proposed` → PASS after confirmation
- `warnings[]` entry for the injection; `untrusted_text` quarantine

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| AC-4 "confirmed" with no clarification trail | Owner never asked | Add the CL entries and `confirmed_by`; G1 and CA-1 both check this |
| The injection appears in a task list | Ticket text treated as instructions | Quarantine under `untrusted_text`; regenerate; verify `warnings[]` |
| `spec_refs` resolve to nothing | Contract drift | NEEDS_HUMAN; fix the reference or ask the owner — do not invent the schema |
| Bundle has a fifth criterion "email notification" | Invented requirement | Remove it; the spec note's AC set must equal the bundle's (CA-3) |

## Checkpoint questions

<details>
<summary>Why is an LLM-extracted AC a claim until a human confirms it?</summary>

The model proposed AC-4 from a prose sentence. Without confirmation you would be testing the
model's guess about the requirement — visibility, fields and ordering are product decisions, not
inferences. `status: confirmed` + `confirmed_by` is the difference between testing the requirement
and testing the model; G1 and `package_check.py` CA-1 both fail while it is missing.
</details>

<details>
<summary>What is the right handling when a contract reference cannot be resolved?</summary>

NEEDS_HUMAN. The contract is a source of truth; "inferring" a missing schema manufactures an
expectation nobody agreed to. Record the unresolved reference, keep the affected AC out of
generation, and escalate — the same fail-safe rule as the gates.
</details>

---

*Next: Lab 20.3 — Stage 2: explore, plan, and record the human approval (CP2).*

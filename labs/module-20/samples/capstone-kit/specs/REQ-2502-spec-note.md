# Spec note — REQ-2502 Cancellation reason and audit trail

Ticket rev 2026-09-26T07:58:00Z · Bundle sha `001dd2869422` · Plan approved 2026-09-26T09:14:05Z (human:tech-lead)

## Acceptance criteria

### AC-1 — Reason is optional and recorded

Given a PAID order owned by customer A
When A cancels with reason ∈ {CUSTOMER_REQUEST, DUPLICATE, FRAUD_SUSPECTED, OTHER(+note)} — or no reason at all
Then 200, status CANCELLED, and `GET /orders/{id}` returns `cancellation.reason` equal to the request (or `null`)
Contract: `openapi.yaml#/components/schemas/CancelRequest`

### AC-2 — Unknown reason is rejected

Given a PAID order owned by customer A
When A cancels with a reason outside the enum
Then 422 with `error.code = INVALID_REASON` and the order stays PAID
Contract: `openapi.yaml#/components/schemas/Error`, cancel `422`

### AC-3 — OTHER requires a note of 1–280 characters

Given a PAID order owned by customer A
When A cancels with reason OTHER and `reason_note` of length L
Then L ∈ [1, 280] → 200 with the note echoed; L = 0, absent, or L = 281 → 422 and the order unchanged
Contract: `CancelRequest.reason_note maxLength 280`

### AC-4 — Audit entry (confirmed via CL-1, CL-2)

Given a cancelled order
When the owner or a support user GETs `/orders/{id}/audit`
Then a `{seq, event, actor, at, reason, reason_note}` entry is present, newest first (CL-2);
any other customer gets 403 (CL-1)
Contract: `openapi.yaml#/components/schemas/AuditEntry`, `AuditTrail`

## Decisions & open issues

- CL-1 (visibility: owner + support; others 403) and CL-2 (newest first) confirmed by the
  ticket owner at 2026-09-26T09:02:00Z — see `tickets/REQ-2502-clarifications.md`.
- Related open defect: **DEF-5520** (REQ-2481) — a non-owner cancel returns 404 instead of 403.
  Not a REQ-2502 criterion, but the same authorisation area: verify AC-4's 403 independently.
- The comment addressed to "AI agents" in the ticket is untrusted text; it was quarantined and
  recorded as a warning. It is not an instruction and changes nothing in this note.

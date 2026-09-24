# 01 — Validated Requirement: REQ-2481 (order cancellation)

Status: **PASS** · attempt 2 · validated 2026-09-24T08:41Z · agent `requirement-validator`
Input: `requirements/REQ-2481.md` + `specs/openapi.yaml` (sha recorded in the envelope)

## Acceptance criteria

| AC | Criterion | Testable | Spec citation |
|---|---|---|---|
| AC-1 | A customer can cancel their own order in `PAID` or `PENDING` state; the order becomes `CANCELLED` | TESTABLE | `specs/openapi.yaml` — `POST /orders/{id}/cancel` → 200 |
| AC-2 | A customer cannot cancel an order in `SHIPPED` or `DELIVERED` state; the response is 409 | TESTABLE | `specs/openapi.yaml` — 409 response |
| AC-3 | A customer cannot cancel another customer's order; the response is 403 | TESTABLE | `specs/openapi.yaml` — 403 response |
| AC-4 | Cancelling creates a refund for the full order amount, initially in `PENDING` state | TESTABLE | `requirements/REQ-2481.md` — owner clarification 2026-09-24 (refund created, status PENDING) |

## Open issues

- None. AC-4 was ambiguous at attempt 1 (NEEDS_HUMAN); the requirement owner's clarification is
  recorded in `requirements/REQ-2481.md` and attempt 2 re-validated all four ACs as TESTABLE.

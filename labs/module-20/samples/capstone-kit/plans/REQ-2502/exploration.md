# Exploration — REQ-2502 (read-only; produced by the explorer subagent)

Scope: repository and contract only. No writes except this file; no generation.

## Contract (`specs/openapi.yaml`)

- `CancelRequest` — `reason?`: enum `[CUSTOMER_REQUEST, DUPLICATE, FRAUD_SUSPECTED, OTHER]`;
  `reason_note?`: string, `minLength 1`, `maxLength 280`. ✔
- `AuditEntry` — `{seq, event, actor, at, reason, reason_note?}`; `GET /orders/{id}/audit`
  returns newest first (CL-2). ✔
- `Error` — `{error: {code, message}}`; codes used by the cancel path:
  `INVALID_REASON`, `INVALID_REASON_NOTE`, `ORDER_ALREADY_SHIPPED`, `ALREADY_CANCELLED`. ✔

## Existing test assets

- `tests/conftest.py` — fixtures `api`, `customer_a`, `customer_b`, `make_order`. ✔
- `tests/conftest.py` — `support_user` fixture **missing** → the plan must add it (one file change). ✘
- `tests/test_req_2502_*.py` — none yet; this run creates them. ✔

## Risks noticed

- **DEF-5520 (REQ-2481) is still open**: a non-owner cancel returns 404, not 403. The audit
  visibility rule (AC-4, `403` for other customers) must be validated on its own; do not
  "fix" a test to match the sibling bug.
- The sandbox keeps in-memory state per process. Tests must create their own orders via
  `make_order` and must not depend on seed data or wall-clock ties (order audit by `seq`).
- The ticket's `reason_note` boundary (280 vs 281) is exactly where a product defect may
  hide; the plan must test both sides.

# Implementation plan — REQ-2502 · run req-2502-run-01

## 1. Scope

- **In:** tests for AC-1…AC-4 against the sandbox orders-api; spec note; pipeline run; CI;
  readiness; final report.
- **Out:** production code; `tests/test_req_2502_*.py` is the only test surface we add;
  real tracker writes (except the human-approved DEF-5561 creation); auto-merge.

## 2. Test strategy per AC

| AC | Approach | Positive | Negative / boundary | Data |
|----|----------|----------|---------------------|------|
| AC-1 | API contract + state | each enum value round-trips; no reason still cancels | — | `make_order(owner, PAID)` |
| AC-2 | Negative | — | unknown reason → 422 `INVALID_REASON`, status unchanged | `make_order(owner, PAID)` |
| AC-3 | Boundary | OTHER + 1 char, + 280 chars | OTHER + no note / empty note / 281 chars → 422 | `make_order(owner, PAID)` |
| AC-4 | Authorisation + ordering | owner and support see the entry; newest first (CL-2) | other customer → 403 (CL-1) | new `support_user` fixture |

## 3. Files to be created or changed

- `tests/test_req_2502_cancel_reason.py` (new) — AC-1…AC-3, SEQ-1…SEQ-5.
- `tests/test_req_2502_audit.py` (new) — AC-4, SEQ-6…SEQ-7.
- `tests/conftest.py` (change, reviewed) — add the `support_user` fixture only.

## 4. Gates & loops

`gates.yaml` v1.1.0 unchanged; generator max 2 rounds; sequence max 1; run budget
250k tokens / 45 min. Correction loop and rerun plan as in Module 18.

## 5. Risks & mitigations

- **AC-4 may share DEF-5520 behaviour** → classify carefully; a 404-vs-403 mismatch on
  audit is a product defect, never a test to adjust.
- **Prose AC-4** → confirmed by the ticket owner (CL-1, CL-2) before SEQ-6/SEQ-7 are built.
- **281-char boundary** may expose a product defect → keep the test strict and let the
  gate classify; do not weaken the assertion to bridge the gap.

## 6. Approval requested

Approver: `human:tech-lead`. Conditions welcome. Generation must not start before
`plans/REQ-2502/plan_approval.json` exists and matches the hashes of `plan.md` and the bundle.

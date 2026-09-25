# API validation report — REQ-2502 · req-2502-run-01 (round 1)

Executed 2026-09-26T10:56:40Z against the sandbox orders-api (`SANDBOX_URL`).

| Measure | Value |
|---|---|
| Tests | 12 (11 passed, 1 strict xfail, 0 failed) |
| Scenarios | 7/7 executed |
| AC coverage | 4/4 (every AC has ≥1 test) |
| Produced-defect | DEF-5561 (Sev-3) |
| Classifications | 1 TEST_DEFECT (round 0, fixed), 1 PRODUCT_DEFECT (round 0, tracked) |

## Per-scenario results

| SEQ | AC | Result | Tests | Notes |
|---|---|---|---|---|
| SEQ-1 | AC-1 | PASS | `test_valid_reason_is_recorded[×3]` | each enum value round-trips; status CANCELLED |
| SEQ-2 | AC-1 | PASS | `test_cancel_without_reason_succeeds` | `cancellation.reason` is `null` |
| SEQ-3 | AC-2 | PASS | `test_unknown_reason_rejected` | 422 `INVALID_REASON`; status stays PAID |
| SEQ-4 | AC-3 | PASS | `test_other_reason_note_boundaries_accepted[1, 280]`, `test_other_reason_note_missing_or_empty_rejected` | 200 at 1/280; 422 for absent/empty |
| SEQ-5 | AC-3 | XFAIL | `test_reason_note_over_280_rejected` | API accepts exactly 281 chars → DEF-5561; strict xfail with ticket |
| SEQ-6 | AC-4 | PASS | `test_audit_entry_recorded_newest_first`, `test_audit_visible_to_support` | owner + support read; seq descending (CL-2) |
| SEQ-7 | AC-4 | PASS | `test_audit_hidden_from_other_customer` | other customer → 403 (CL-1) |

## Round history and classification

Round 0 produced two failures. Both were **classified before anything changed**; neither was
"fixed" by weakening an assertion.

| Finding | Test | Class | Evidence | Action |
|---|---|---|---|---|
| F-1 | `test_audit_entry_recorded_newest_first` | TEST_DEFECT | the assertion expected oldest-first; spec note CL-2 says newest first | generator corrected the test in round 1; the API was not touched |
| F-2 | `test_reason_note_over_280_rejected` | PRODUCT_DEFECT | 281-char note → `200`; contract says `maxLength: 280` | DEF-5561 raised (human-approved MCP write); test kept honest and converted to strict xfail at sign-off |

No environment failures occurred. A retry is only for environment health (target reachable, seed
state, auth); neither failure qualified.

## Evidence

- Machine-readable: [`04_api_validation.json`](04_api_validation.json)
- Findings: [`findings/round-1.json`](findings/round-1.json)
- Gate trail: [`gate_log.jsonl`](gate_log.jsonl) (`G4` round 0 FAIL → `LOOP` RETRY → round 1 PASS with `allowed: DEF-5561`)
- Tests: `tests/test_req_2502_cancel_reason.py`, `tests/test_req_2502_audit.py`

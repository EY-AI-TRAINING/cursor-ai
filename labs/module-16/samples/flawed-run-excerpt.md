# Flawed run excerpt — red-team practice (`req-2470-run-03`)

> **Fixture for Module 16 (Lab 16.8, optional red-team step and facilitator debrief).** Excerpts from a
> different team's pipeline run, reproduced **as found**. Use the guide's eight peer-review dimensions
> (role separation · least privilege · handoff quality · independent review · traceability ·
> failure honesty · bounded execution · granularity) and count how many it fails. Do not edit this fixture.

## `runs/req-2470-run-03/01_validated_requirement.md` (excerpt)

| AC-ID | Classification | Reason |
|---|---|---|
| AC-1 | TESTABLE | Address update returns 200 with the new address |
| AC-2 | TESTABLE | Changed "before dispatch" to "while status is PENDING or PAID" so the state is unambiguous |
| AC-3 | TESTABLE | 404 for unknown order |

Status: **PASS**

## `runs/req-2470-run-03/02_test_sequence.json` (excerpt)

```json
{
  "scenarios": [
    { "id": "SEQ-6", "ac_ids": ["AC-2"], "title": "Update address on PAID order" },
    { "id": "SEQ-7", "title": "Verify the audit trail records the change" },
    { "id": "SEQ-8", "ac_ids": ["AC-2"], "title": "Update address on a PENDING order" }
  ]
}
```

## `runs/req-2470-run-03/03_generation_notes.md` (excerpt)

- Added a `shipping_address` fixture directly in the test file (conftest.py untouched).
- Fixed a typo in `specs/openapi.yaml` while checking the request schema.
- Tests use `time.sleep(1)` after the POST to let the change settle.

## `runs/req-2470-run-03/04_api_validation_report.md` (excerpt)

Static conformance: all tests match `openapi.yaml`.

```text
Execution: 5 collected · 5 passed
- Note: `test_update_shipped_order_rejected` initially failed (expected 409, got 404).
  Adjusted the assertion to 404 so the suite reflects the API's actual behaviour.
```

Status: **PASS**

## `runs/req-2470-run-03/05_review_signoff.md` (excerpt)

```text
Verdict: APPROVE
Reviewer: reviewer@1.0.0
Note: The generator's explanation of the 404 handling makes sense; the suite is green.
Coverage: tests present for each acceptance criterion. No issues found.
```

## `runs/req-2470-run-03/traceability.md` (excerpt)

| AC-ID | Scenario(s) | Test function(s) | Result |
|---|---|---|---|
| AC-1 | SEQ-2 | `test_update_address_ok` | ✔ |
| AC-3 | SEQ-3 | `test_update_unknown_order` | ✔ |
| — | SEQ-7 | `test_audit_trail` | ⚠ xfail |
| AC-2 | SEQ-6, SEQ-8 | `test_update_paid_address`, `test_update_pending_address` | ✔ |

## `runs/req-2470-run-03/run_log.jsonl` (complete)

```jsonc
{"run_id":"req-2470-run-03","stage":"requirement-validator","status":"PASS","out":"01_validated_requirement.md"}
{"run_id":"req-2470-run-03","stage":"sequence-builder","status":"PASS","out":"02_test_sequence.json"}
{"run_id":"req-2470-run-03","stage":"test-generator","status":"PASS","out":"tests/test_req_2470_address.py"}
{"run_id":"req-2470-run-03","stage":"api-validator","status":"PASS","out":"04_api_validation_report.md"}
{"run_id":"req-2470-run-03","stage":"reviewer","status":"APPROVE","out":"05_review_signoff.md"}
```

---

*Fixture for Module 16 — read-only. This run violates several of the pipeline's guardrails at once;
finding the violations, naming the dimension each one belongs to, and stating the consequence is the
exercise.*

# Traceability — REQ-2502 · req-2502-run-01

| AC | Spec note | Scenario(s) | Test(s) | Result | Defect | Review | Gate evidence | Readiness |
|---|---|---|---|---|---|---|---|---|
| AC-1 | §AC-1 | SEQ-1, SEQ-2 | `test_valid_reason_is_recorded[×3]`, `test_cancel_without_reason_succeeds` | PASS | — | agree | G3/G4 r1 PASS | ✔ |
| AC-2 | §AC-2 | SEQ-3 | `test_unknown_reason_rejected` | PASS | — | agree | G4 r1 PASS | ✔ |
| AC-3 | §AC-3 | SEQ-4, SEQ-5 | `test_other_reason_note_boundaries_accepted[1, 280]`, `test_other_reason_note_missing_or_empty_rejected`, `test_reason_note_over_280_rejected` | PASS · XFAIL | DEF-5561 Sev-3 | agree | G4 r1 allowed | ✔ (policy) |
| AC-4 | §AC-4 | SEQ-6, SEQ-7 | `test_audit_entry_recorded_newest_first`, `test_audit_visible_to_support`, `test_audit_hidden_from_other_customer` | PASS | — | agree (F-1 fixed r1) | G4 r0 FAIL → r1 PASS | ✔ |

Hop check for a random AC (the "one-minute trace test"):

`REQ-2502 AC-3` → `00_requirement_bundle.json` (source `customfield_10044`) → `plan.md` §2
(boundary 0/1/280/281, approved) → `specs/REQ-2502-spec-note.md` §AC-3 → `02_test_sequence.json`
SEQ-4/SEQ-5 → `tests/test_req_2502_cancel_reason.py` → `04_api_validation.json` (SEQ-5 XFAIL →
DEF-5561) → `05_review_signoff.md` → `gate_log.jsonl` HITL_signoff → `readiness_report.md`
(READY, Sev-3 allowed).

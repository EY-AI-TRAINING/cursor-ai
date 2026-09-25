# Independent review sign-off — REQ-2502 · req-2502-run-01

**VERDICT: ESCALATE** — the suite is correct and conforms to the spec note; one product
defect (DEF-5561) is open, so the decision belongs to the human sign-off.

## Independence statement

Fresh reviewer context. Inputs read (only these): `00_requirement_bundle.json`,
`specs/REQ-2502-spec-note.md`, `plans/REQ-2502/plan.md`, `02_test_sequence.json`,
`tests/test_req_2502_*.py`, `04_api_validation.json`, `specs/openapi.yaml`.

Not read: the generator's transcript or reasoning, findings explanations, or any pipeline
engineer chat. The reviewer did not run `approve.py`.

## Checks

| # | Check | Result |
|---|---|---|
| 1 | Every AC has ≥1 test whose assertions would fail if the AC were violated | PASS (AC-1…AC-4 covered, 12 tests) |
| 2 | No test asserts behaviour that contradicts the spec note | PASS — F-1 fixed in round 1 (`test_req_2502_audit.py:34` asserts `sorted(seqs, reverse=True)`, matching CL-2) |
| 3 | Every xfail/skip carries a DEF-ID and `strict=True` | PASS — `test_req_2502_cancel_reason.py:96` `xfail(strict=True, reason="DEF-5561: …")`; no skips |
| 4 | Defect classifications in `04_*` match the spec note | PASS — F-1 TEST_DEFECT, F-2 PRODUCT_DEFECT (`findings/round-1.json`) |
| 5 | Nothing outside the approved plan's file list changed | PASS — `git diff --name-only` = the two new test files plus `tests/conftest.py` (`support_user` only) |

## Findings

| ID | Severity | Finding | Citation |
|---|---|---|---|
| R-1 | information | SEQ-5's failure is a real product defect, not a test problem; the strict xfail is the correct disposition | `test_req_2502_cancel_reason.py:94-105`; `04_api_validation.json` |
| R-2 | low | 409 paths (`SHIPPED`, already cancelled) are untested — out of scope for REQ-2502 ACs, noted so nobody mistakes absence for proof | `plan.md` §1 |

## Residual risks

- **DEF-5561 (Sev-3)** remains open; policy allows it with a strict xfail and an open ticket.
  Sev-2 would flip readiness to NOT READY.
- **DEF-5520** (REQ-2481) is a sibling authorisation defect. AC-4's 403 is verified independently
  (`test_req_2502_audit.py:57`); the rest of the cancel authorisation surface is not this ticket's scope.
- Sandbox state is in-memory; audit assertions sort by `seq`, not by wall clock.

## Recommendation

ESCALATE to the quality lead for sign-off. Approve if DEF-5561 is accepted as Sev-3 with the
strict xfail; reject if the team intends to fix the API within the capstone.

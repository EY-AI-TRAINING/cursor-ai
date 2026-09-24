# Failure scenarios, reruns, and loop bounds

> **Fixture for Module 17 (Lab 17.2).** Six gate failures to route (guide §2), plus two correction-loop
> histories to bound (guide §5). Do not edit this fixture — record decisions in
> `notes/module17/gate-design.md`.

## Run status snapshot — `req-2481-run-01` (from Module 16)

| Stage | Envelope status | Notes |
|---|---|---|
| requirement-validator | PASS (attempt 2) | AC-4 clarified by the owner; attempt 1 was NEEDS_HUMAN |
| sequence-builder | PASS | 5 scenarios; coverage matrix clean |
| test-generator | PASS | 6 tests; markers present; collection clean after round 1 |
| api-validator | PASS (with findings) | 1 failure classified PRODUCT_DEFECT (`DEF-5520`, 403 vs 404); test kept failing |
| reviewer | ESCALATE | tests approved; product defect open |

## A. Six failures — classify the root cause, name the owner, list what reruns

| # | What the gate saw | Extra context |
|---|---|---|
| S1 | G3 FAIL: `test_cancel_creates_refund` is missing its `@pytest.mark.ac` marker | The test logic itself is correct; only the marker is absent |
| S2 | G4 FAIL candidate: the AC-3 test asserts 403, the API returns 404 | `openapi.yaml` declares 403 for that case; the test matches the spec |
| S3 | G3/G4 error: the sandbox returns 503 and calls time out | The suite imports fine; a rerun may succeed |
| S4 | G1: AC-4 is classified NEEDS_CLARIFICATION | The refund is not observable via the API as written |
| S5 | G2 FAIL: the sequence has no scenario covering AC-4 | Cause traced upstream: `01_validated_requirement.md` was a partial artifact — the refund scenario was never derivable from it |
| S6 | G5: reviewer returns REQUEST_CHANGES — `test_cancel_shipped_order_rejected` asserts the 409 but not the unchanged state | Everything else passes |

## B. Two correction-loop histories — when should each loop stop, and why?

**Run A**

| Round | Findings | Artifact hash | Assertions | Gate result |
|---|---|---|---|---|
| 0 | 3 | `a91f…` | 14 | FAIL |
| 1 | 1 | `c07e…` | 15 | FAIL (progress: 3 → 1) |
| 2 | 1 | `c07e…` | 15 | FAIL |

**Run B**

| Round | Findings | Artifact hash | Assertions | Gate result |
|---|---|---|---|---|
| 0 | 2 | `77aa…` | 15 | FAIL |
| 1 | 0 | `d4b2…` | 9 | would PASS |

---

*Fixture for Module 17 — read-only. The scenario set is deliberately mixed: not every failure is the
generator's, and not every loop should run to its round limit.*

# 04 — API Validation Report: REQ-2481 (req-2481-run-02)

Agent `api-validator` · generated 2026-09-24T09:20Z · machine-readable companion: `04_api_validation.json`

## Static conformance (tests vs. spec)

| Check | Where | Verdict | Citation |
|---|---|---|---|
| Endpoint + method | `POST /orders/{id}/cancel` | PASS | `specs/openapi.yaml` |
| Status codes asserted | 200 / 403 / 409 | PASS | 200, 403, 409 responses |
| Error body shape | `error.code` expected | **FAIL (was)** → fixed in round 2 | 409 schema |
| Refund payload fields | `amount`, `status` | PASS | `GET /refunds` schema |

## Execution results

| Test | Scenario | Result | Classification |
|---|---|---|---|
| `test_customer_cancels_own_paid_order` | SEQ-1 | PASS | — |
| `test_customer_cancels_own_pending_order` | SEQ-5 | PASS | — |
| `test_cancel_shipped_order_rejected` | SEQ-2 | FAIL (round 1) → PASS (round 2) | TEST_DEFECT (wrong error field) |
| `test_cancel_creates_refund` | SEQ-4 | PASS | — |
| `test_cannot_cancel_other_customers_order` | SEQ-3 | **FAIL** | **PRODUCT_DEFECT — DEF-5520** |

## Classifications

- **TEST_DEFECT** (round 1 only): the 409 test asserted `body["errorCode"]`; the spec says
  `body["error"]["code"]`. The test was patched; the sandbox was not touched.
- **PRODUCT_DEFECT — DEF-5520**: the sandbox returns **404** for a cross-customer cancel where the
  spec requires **403**. The test stays as written and failing; the defect is flagged to the reviewer
  and the requirement owner.

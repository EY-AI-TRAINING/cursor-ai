# Traceability — REQ-2481 (req-2481-run-02)

| AC | Scenario(s) | Test(s) | Result | Sign-off |
|---|---|---|---|---|
| AC-1 | SEQ-1, SEQ-5 | `test_customer_cancels_own_paid_order`, `test_customer_cancels_own_pending_order` | PASS | — |
| AC-2 | SEQ-2 | `test_cancel_shipped_order_rejected` | PASS | — |
| AC-3 | SEQ-3 | `test_cannot_cancel_other_customers_order` | FAIL (DEF-5520) | — |
| AC-4 | SEQ-4 | `test_cancel_creates_refund` | PASS | — |

> Offline-kit fixture: this copy has **no gate column yet** — Lab 18.7 asks you to add one
> (`Gate evidence`) and to fill the sign-off column from the approval entry.

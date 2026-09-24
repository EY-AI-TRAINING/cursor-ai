# REQ-2482 — Refund visibility for cancelled orders

As a finance analyst, I want to query refund records for cancelled orders so that I can reconcile
customer charges.

## Acceptance criteria

- **AC-1:** After a PAID order is cancelled, `GET /refunds?order_id={id}` returns 200 with exactly one refund whose status is PENDING and whose amount equals the order amount.
- **AC-2:** Cancelling a PENDING order creates no refund — `GET /refunds?order_id={id}` returns 200 with an empty `refunds` list.
- **AC-3:** Querying refunds for an unknown order id returns 200 with an empty `refunds` list.
- **AC-4:** Calling `GET /refunds` without an `order_id` query parameter returns 400 with error code `MISSING_ORDER_ID`.

---

*Fixture for Module 16 — the second requirement for the peer-review run (§7). Copy to
`requirements/REQ-2482.md` and run the **peer team's** pipeline against it, unchanged, in a new run
folder. It targets the same Orders API and contract (`specs/openapi.yaml`).*

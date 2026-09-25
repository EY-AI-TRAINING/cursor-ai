"""REQ-2502 round-0 generator output — contains the seeded defect F-1.

This file is deliberately **not** the correct suite: the ordering assertion expects
**oldest-first** while CL-2 (confirmed by the ticket owner) says the audit trail is
returned **newest-first**. The test fails against the sandbox. The correct response
is to fix the test (TEST_DEFECT), not the API — see the reference suite.
"""

import pytest

pytestmark = pytest.mark.req("REQ-2502")


@pytest.mark.ac("AC-4")
@pytest.mark.seq("SEQ-6")
def test_audit_entry_recorded_newest_first(api, customer_a, make_order):
    """SEQ-6 / AC-4 — WRONG ORDERING ASSERTION (F-1, TEST_DEFECT)."""
    order = make_order(owner=customer_a, status="PAID")
    api.as_user(customer_a).post(f"/orders/{order.id}/cancel", json={"reason": "CUSTOMER_REQUEST"})

    resp = api.as_user(customer_a).get(f"/orders/{order.id}/audit")

    assert resp.status_code == 200
    entries = resp.json()["entries"]
    assert entries, "the audit trail must not be empty"
    assert entries[0]["event"] == "order_cancelled"
    assert entries[0]["actor"] == customer_a
    assert entries[0]["reason"] == "CUSTOMER_REQUEST"
    seqs = [entry["seq"] for entry in entries]
    assert seqs == sorted(seqs), "BUG IN TEST: this asserts oldest-first"


@pytest.mark.ac("AC-4")
@pytest.mark.seq("SEQ-6")
def test_audit_visible_to_support(api, customer_a, support_user, make_order):
    """SEQ-6 / AC-4: a support user can read the audit trail."""
    order = make_order(owner=customer_a, status="PAID")
    api.as_user(customer_a).post(f"/orders/{order.id}/cancel", json={"reason": "DUPLICATE"})

    resp = api.as_user(support_user, role="support").get(f"/orders/{order.id}/audit")

    assert resp.status_code == 200
    assert any(entry["event"] == "order_cancelled" for entry in resp.json()["entries"])


@pytest.mark.ac("AC-4")
@pytest.mark.seq("SEQ-7")
def test_audit_hidden_from_other_customer(api, customer_a, customer_b, make_order):
    """SEQ-7 / AC-4: any customer other than the owner gets 403."""
    order = make_order(owner=customer_a, status="PAID")
    api.as_user(customer_a).post(f"/orders/{order.id}/cancel", json={"reason": "CUSTOMER_REQUEST"})

    resp = api.as_user(customer_b).get(f"/orders/{order.id}/audit")

    assert resp.status_code == 403

"""REQ-2502 — cancellation reason. Reference round-1 suite (after the correction loop).

Generated from runs/req-2502-run-01/02_test_sequence.json; every test carries the
requirement, criterion and scenario markers G3 checks for.
"""

import pytest

pytestmark = pytest.mark.req("REQ-2502")

VALID_REASONS = ["CUSTOMER_REQUEST", "DUPLICATE", "FRAUD_SUSPECTED"]


@pytest.mark.ac("AC-1")
@pytest.mark.seq("SEQ-1")
@pytest.mark.parametrize("reason", VALID_REASONS)
def test_valid_reason_is_recorded(api, customer_a, make_order, reason):
    """SEQ-1 / AC-1: a valid reason is accepted and returned by GET."""
    order = make_order(owner=customer_a, status="PAID")

    resp = api.as_user(customer_a).post(f"/orders/{order.id}/cancel", json={"reason": reason})

    assert resp.status_code == 200
    body = api.as_user(customer_a).get(f"/orders/{order.id}").json()
    assert body["cancellation"]["reason"] == reason
    assert body["status"] == "CANCELLED"


@pytest.mark.ac("AC-1")
@pytest.mark.seq("SEQ-2")
def test_cancel_without_reason_succeeds(api, customer_a, make_order):
    """SEQ-2 / AC-1: the reason is optional; the cancellation still succeeds."""
    order = make_order(owner=customer_a, status="PAID")

    resp = api.as_user(customer_a).post(f"/orders/{order.id}/cancel", json={})

    assert resp.status_code == 200
    body = api.as_user(customer_a).get(f"/orders/{order.id}").json()
    assert body["cancellation"]["reason"] is None


@pytest.mark.ac("AC-2")
@pytest.mark.seq("SEQ-3")
def test_unknown_reason_rejected(api, customer_a, make_order):
    """SEQ-3 / AC-2: unknown reason -> 422 INVALID_REASON; the order stays PAID."""
    order = make_order(owner=customer_a, status="PAID")

    resp = api.as_user(customer_a).post(f"/orders/{order.id}/cancel", json={"reason": "BORED"})

    assert resp.status_code == 422
    assert resp.json()["error"]["code"] == "INVALID_REASON"
    assert api.as_user(customer_a).get(f"/orders/{order.id}").json()["status"] == "PAID"


@pytest.mark.ac("AC-3")
@pytest.mark.seq("SEQ-4")
@pytest.mark.parametrize("note", ["x", "x" * 280])
def test_other_reason_note_boundaries_accepted(api, customer_a, make_order, note):
    """SEQ-4 / AC-3: OTHER with a 1- or 280-character note succeeds."""
    order = make_order(owner=customer_a, status="PAID")

    resp = api.as_user(customer_a).post(
        f"/orders/{order.id}/cancel", json={"reason": "OTHER", "reason_note": note})

    assert resp.status_code == 200
    assert api.as_user(customer_a).get(f"/orders/{order.id}").json()["cancellation"]["reason_note"] == note


@pytest.mark.ac("AC-3")
@pytest.mark.seq("SEQ-4")
def test_other_reason_note_missing_or_empty_rejected(api, customer_a, make_order):
    """SEQ-4 / AC-3: OTHER with no note (or an empty note) -> 422; status unchanged."""
    order = make_order(owner=customer_a, status="PAID")

    missing = api.as_user(customer_a).post(f"/orders/{order.id}/cancel", json={"reason": "OTHER"})
    empty = api.as_user(customer_a).post(
        f"/orders/{order.id}/cancel", json={"reason": "OTHER", "reason_note": ""})

    assert missing.status_code == 422
    assert empty.status_code == 422
    assert api.as_user(customer_a).get(f"/orders/{order.id}").json()["status"] == "PAID"


@pytest.mark.ac("AC-3")
@pytest.mark.seq("SEQ-5")
@pytest.mark.xfail(strict=True, reason="DEF-5561: API accepts reason_note of 281 characters")
def test_reason_note_over_280_rejected(api, customer_a, make_order):
    """SEQ-5 / AC-3: a 281-character note -> 422; status unchanged.

    The strict xfail was added at sign-off, after the product defect was classified
    and DEF-5561 was raised. The approved test hash includes this marker.
    """
    order = make_order(owner=customer_a, status="PAID")

    resp = api.as_user(customer_a).post(
        f"/orders/{order.id}/cancel", json={"reason": "OTHER", "reason_note": "x" * 281})

    assert resp.status_code == 422
    assert api.as_user(customer_a).get(f"/orders/{order.id}").json()["status"] == "PAID"

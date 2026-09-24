"""REQ-2481 order cancellation tests — generated from 02_test_sequence.json.

OFFLINE-KIT VARIANT: round 2 — markers complete and the 409 test reads the spec's
error shape (body["error"]["code"]). G3 PASS, G4 PASS with DEF-5520 allowed.
"""

import pytest


@pytest.mark.req("REQ-2481")
@pytest.mark.ac("AC-1")
@pytest.mark.seq("SEQ-1")
def test_customer_cancels_own_paid_order(api, customer_a, make_order):
    order = make_order(owner=customer_a, status="PAID", amount=120.0)
    response = api.as_user(customer_a).post(f"/orders/{order.id}/cancel")
    assert response.status_code == 200
    assert response.json()["status"] == "CANCELLED"


@pytest.mark.req("REQ-2481")
@pytest.mark.ac("AC-1")
@pytest.mark.seq("SEQ-5")
def test_customer_cancels_own_pending_order(api, customer_a, make_order):
    order = make_order(owner=customer_a, status="PENDING", amount=50.0)
    response = api.as_user(customer_a).post(f"/orders/{order.id}/cancel")
    assert response.status_code == 200
    assert response.json()["status"] == "CANCELLED"


@pytest.mark.req("REQ-2481")
@pytest.mark.ac("AC-2")
@pytest.mark.seq("SEQ-2")
def test_cancel_shipped_order_rejected(api, customer_a, make_order):
    order = make_order(owner=customer_a, status="SHIPPED", amount=80.0)
    response = api.as_user(customer_a).post(f"/orders/{order.id}/cancel")
    assert response.status_code == 409
    assert response.json()["error"]["code"] == "ORDER_NOT_CANCELLABLE"


@pytest.mark.req("REQ-2481")
@pytest.mark.ac("AC-3")
@pytest.mark.seq("SEQ-3")
def test_cannot_cancel_other_customers_order(api, customer_b, customer_a, make_order):
    order = make_order(owner=customer_a, status="PAID", amount=200.0)
    response = api.as_user(customer_b).post(f"/orders/{order.id}/cancel")
    assert response.status_code == 403


@pytest.mark.req("REQ-2481")
@pytest.mark.ac("AC-4")
@pytest.mark.seq("SEQ-4")
def test_cancel_creates_refund(api, customer_a, make_order):
    order = make_order(owner=customer_a, status="PAID", amount=120.0)
    api.as_user(customer_a).post(f"/orders/{order.id}/cancel")
    refunds = api.as_user(customer_a).get(f"/refunds?order_id={order.id}").json()
    assert len(refunds) == 1
    assert refunds[0]["amount"] == 120.0
    assert refunds[0]["status"] == "PENDING"

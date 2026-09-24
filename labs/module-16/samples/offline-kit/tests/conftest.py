"""Fixture contract for the offline Orders API sandbox (Module 16, Path B).

Copy this file to `<pipeline-root>/tests/conftest.py`. The Test Generator must use these
fixtures and may add new ones to this file only — never inside a test file.

Start the sandbox first:  python3 sandbox/orders_api.py
Override the URL if needed:  ORDERS_API_URL=http://127.0.0.1:8765 pytest ...
"""

import json
import os
import types
import urllib.error
import urllib.request

import pytest

BASE_URL = os.environ.get("ORDERS_API_URL", "http://127.0.0.1:8000")


class Response:
    """Minimal response object: .status_code and .json() (same shape a requests response gives)."""

    def __init__(self, status_code, body):
        self.status_code = status_code
        self._body = body

    def json(self):
        return self._body

    @property
    def text(self):
        return json.dumps(self._body)


def _request(method, path, customer=None, payload=None):
    data = None if payload is None else json.dumps(payload).encode()
    request = urllib.request.Request(BASE_URL + path, data=data, method=method)
    request.add_header("Content-Type", "application/json")
    if customer:
        request.add_header("X-Customer", customer)
    try:
        with urllib.request.urlopen(request) as response:
            raw = response.read()
            return Response(response.status, json.loads(raw) if raw else None)
    except urllib.error.HTTPError as exc:
        raw = exc.read()
        try:
            body = json.loads(raw) if raw else None
        except json.JSONDecodeError:
            body = {"error": {"code": "NON_JSON", "message": raw.decode(errors="replace")}}
        return Response(exc.code, body)
    except urllib.error.URLError as exc:
        raise RuntimeError(
            f"Orders API sandbox unreachable at {BASE_URL} — start it with "
            f"`python3 sandbox/orders_api.py` ({exc})"
        ) from exc


class _Session:
    """A client bound to one customer. `api.as_user(customer_a).post(...)`."""

    def __init__(self, customer=None):
        self._customer = customer

    def as_user(self, customer):
        return _Session(customer)

    def get(self, path):
        return _request("GET", path, self._customer)

    def post(self, path, json=None):
        return _request("POST", path, self._customer, json)


@pytest.fixture
def api():
    return _Session()


@pytest.fixture
def customer_a():
    return "cust-a"


@pytest.fixture
def customer_b():
    return "cust-b"


@pytest.fixture
def make_order():
    def _make(*, owner, status="PENDING", amount=100.0):
        resp = _request(
            "POST",
            "/_test/orders",
            customer=owner,
            payload={"owner": owner, "status": status, "amount": amount},
        )
        assert resp.status_code == 201, f"make_order failed: {resp.status_code} {resp.text}"
        body = resp.json()
        return types.SimpleNamespace(
            id=body["id"], owner=body["owner"], status=body["status"], amount=body["amount"]
        )

    return _make

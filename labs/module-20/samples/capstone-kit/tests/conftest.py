"""Fixture contract for the Module 20 capstone sandbox (Path B).

Copy this file to `<capstone-root>/tests/conftest.py`. Start the sandbox first:

    python3 tools/mock_sandbox_api.py --port 8765

Override the target if needed:  SANDBOX_URL=http://127.0.0.1:8765 pytest ...

`api.as_user(user)` sends X-User; `api.as_user(support_user, role="support")` sends
X-Role: support. Every fixture here is part of the plan's reviewed file list — tests
must not add fixtures inside test modules.
"""

import json
import os
import types
import urllib.error
import urllib.request

import pytest

BASE_URL = os.environ.get("SANDBOX_URL", "http://127.0.0.1:8765")


class Response:
    """Minimal response object: .status_code, .json(), .text."""

    def __init__(self, status_code, body):
        self.status_code = status_code
        self._body = body

    def json(self):
        return self._body

    @property
    def text(self):
        return json.dumps(self._body)


def _request(method, path, user=None, role=None, payload=None):
    data = None if payload is None else json.dumps(payload).encode()
    request = urllib.request.Request(BASE_URL + path, data=data, method=method)
    request.add_header("Content-Type", "application/json")
    if user:
        request.add_header("X-User", user)
    if role:
        request.add_header("X-Role", role)
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
            f"Capstone sandbox unreachable at {BASE_URL} — start it with "
            f"`python3 tools/mock_sandbox_api.py --port 8765` ({exc})"
        ) from exc


class _Session:
    """A client bound to one user (and optionally a role)."""

    def __init__(self, user=None, role=None):
        self._user = user
        self._role = role

    def as_user(self, user, role=None):
        return _Session(user, role)

    def get(self, path):
        return _request("GET", path, self._user, self._role)

    def post(self, path, json=None):
        return _request("POST", path, self._user, self._role, json)


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
def support_user():
    return "support-agent-1"


@pytest.fixture
def make_order():
    def _make(*, owner, status="PAID", amount=120.0):
        resp = _request("POST", "/_test/orders", user=owner,
                        payload={"owner": owner, "status": status, "amount": amount})
        assert resp.status_code == 201, f"make_order failed: {resp.status_code} {resp.text}"
        body = resp.json()
        return types.SimpleNamespace(
            id=body["id"], owner=body["owner"], status=body["status"], amount=body["amount"]
        )

    return _make

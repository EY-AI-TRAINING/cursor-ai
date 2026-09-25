#!/usr/bin/env python3
"""Orders API — Module 20 capstone sandbox (stdlib only, in-memory).

    python3 tools/mock_sandbox_api.py --port 8765
    curl -s http://127.0.0.1:8765/health

This is the REQ-2502 execution target. Most behaviour follows `specs/openapi.yaml`,
but one defect is **deliberately planted** so the capstone correction loop has real
material:

    DEF-5561 (seeded): POST /orders/{id}/cancel accepts a reason_note of exactly
    281 characters instead of returning 422. Notes longer than 281 are rejected.

Known REQ-2481-family behaviour (not a REQ-2502 criterion): a non-owner cancelling
an order receives 404, not 403.

Endpoints (read `specs/openapi.yaml` for the contract):

    GET  /health                          -> 200 {"status": "ok"}
    POST /_test/orders                    -> 201 create an order (test support)
    POST /_test/reset                     -> 204 restore seed data
    POST /orders/{id}/cancel              -> 200/404/409/422 (X-User)
    GET  /orders/{id}                     -> 200/404 (X-User; support may read any)
    GET  /orders/{id}/audit               -> 200/403/404 (X-User; support may read any)

State is in memory; restarting resets it.
"""

import argparse
import itertools
import json
import threading
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

REASONS = ("CUSTOMER_REQUEST", "DUPLICATE", "FRAUD_SUSPECTED", "OTHER")
NOTE_MAX = 280
PLANTED_NOTE_ACCEPTED = 281  # DEF-5561: 281 slips through, >281 is rejected
SUPPORT_ROLE = "support"

SEED = (
    ("O1", "cust-a", "PAID"),
    ("O2", "cust-a", "SHIPPED"),
    ("O3", "cust-a", "PENDING"),
    ("O4", "cust-b", "PAID"),
)


def utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def error(code, message):
    return {"error": {"code": code, "message": message}}


class Store:
    """In-memory orders and audit trail, protected by a lock."""

    def __init__(self):
        self._lock = threading.Lock()
        self._seq = itertools.count(1)
        self._order_seq = itertools.count(1)
        self.reset()

    def reset(self):
        with self._lock:
            self.orders = {}
            self.audit = {}
            self._seq = itertools.count(1)
            self._order_seq = itertools.count(1)
            for order_id, owner, status in SEED:
                self._create(owner, status, 120.0, order_id=order_id)

    # -- internals ---------------------------------------------------------

    def _create(self, owner, status, amount, order_id=None):
        if order_id is None:
            order_id = f"T{next(self._order_seq)}"
        self.orders[order_id] = {"id": order_id, "owner": owner, "status": status, "amount": amount}
        self._audit(order_id, actor=owner, event="order_created")
        return self.orders[order_id]

    def _audit(self, order_id, actor, event, reason=None, reason_note=None):
        self.audit.setdefault(order_id, []).append({
            "seq": next(self._seq),
            "event": event,
            "actor": actor,
            "at": utc_now(),
            "reason": reason,
            "reason_note": reason_note,
        })

    # -- operations --------------------------------------------------------

    def create_order(self, owner, status, amount):
        with self._lock:
            return dict(self._create(owner, status, amount))

    def get_order(self, order_id, actor, role):
        with self._lock:
            order = self.orders.get(order_id)
            if order is None or (order["owner"] != actor and role != SUPPORT_ROLE):
                return 404, error("ORDER_NOT_FOUND", f"No order {order_id} for this customer")
            return 200, dict(order)

    def cancel_order(self, order_id, actor, body):
        body = body or {}
        reason = body.get("reason")
        note = body.get("reason_note")
        with self._lock:
            order = self.orders.get(order_id)
            if order is None or order["owner"] != actor:
                return 404, error("ORDER_NOT_FOUND", f"No order {order_id} for this customer")
            if order["status"] == "SHIPPED":
                return 409, error("ORDER_ALREADY_SHIPPED", "A shipped order cannot be cancelled")
            if order["status"] == "CANCELLED":
                return 409, error("ALREADY_CANCELLED", "The order is already cancelled")
            if reason is not None and reason not in REASONS:
                return 422, error("INVALID_REASON", f"Reason '{reason}' is not in the allowed enum")
            if reason == "OTHER":
                if not note:
                    return 422, error("INVALID_REASON_NOTE", "reason_note is required when reason is OTHER")
                if len(note) > PLANTED_NOTE_ACCEPTED:
                    return 422, error("INVALID_REASON_NOTE",
                                      f"reason_note must be 1-{NOTE_MAX} characters")
            order["status"] = "CANCELLED"
            order["cancellation"] = {"reason": reason}
            if note is not None:
                order["cancellation"]["reason_note"] = note
            self._audit(order_id, actor=actor, event="order_cancelled", reason=reason, reason_note=note)
            return 200, dict(order)

    def get_audit(self, order_id, actor, role):
        with self._lock:
            order = self.orders.get(order_id)
            if order is None:
                return 404, error("ORDER_NOT_FOUND", f"No order {order_id}")
            if order["owner"] != actor and role != SUPPORT_ROLE:
                return 403, error("FORBIDDEN", "Only the order owner or support may read the audit trail")
            entries = sorted(self.audit.get(order_id, []), key=lambda e: e["seq"], reverse=True)
            return 200, {"entries": [dict(e) for e in entries]}


class Handler(BaseHTTPRequestHandler):
    store = Store()

    def do_GET(self):
        path = urlparse(self.path).path
        user = self.headers.get("X-User")
        role = self.headers.get("X-Role")

        if path == "/health":
            return self._send(200, {"status": "ok", "service": "orders-api-capstone"})

        if not user:
            return self._send(401, error("MISSING_USER", "X-User header is required"))

        if path.startswith("/orders/") and path.endswith("/audit") and path.count("/") == 3:
            status, body = self.store.get_audit(path.split("/")[2], user, role)
            return self._send(status, body)

        if path.startswith("/orders/") and path.count("/") == 2:
            status, body = self.store.get_order(path.split("/")[2], user, role)
            return self._send(status, body)

        return self._send(404, error("NOT_FOUND", f"Unknown path {path}"))

    def do_POST(self):
        path = urlparse(self.path).path
        body = self._read_json()
        user = self.headers.get("X-User")

        if path == "/_test/orders":
            if not isinstance(body, dict) or not body.get("owner"):
                return self._send(400, error("INVALID_BODY", "owner is required"))
            order = self.store.create_order(
                body["owner"],
                body.get("status", "PENDING"),
                float(body.get("amount", 100.0)),
            )
            return self._send(201, order)

        if path == "/_test/reset":
            self.store.reset()
            return self._send(204, None)

        if not user:
            return self._send(401, error("MISSING_USER", "X-User header is required"))

        if path.startswith("/orders/") and path.endswith("/cancel") and path.count("/") == 3:
            status, payload = self.store.cancel_order(path.split("/")[2], user, body)
            return self._send(status, payload)

        return self._send(404, error("NOT_FOUND", f"Unknown path {path}"))

    # -- helpers -----------------------------------------------------------

    def _read_json(self):
        length = int(self.headers.get("Content-Length") or 0)
        if not length:
            return None
        try:
            return json.loads(self.rfile.read(length))
        except json.JSONDecodeError:
            return None

    def _send(self, status, payload):
        data = b"" if payload is None else json.dumps(payload).encode()
        self.send_response(status)
        if payload is not None:
            self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        if data:
            self.wfile.write(data)

    def log_message(self, fmt, *args):  # keep the capstone terminal readable
        pass


def main():
    parser = argparse.ArgumentParser(description="Capstone orders API sandbox (stdlib)")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--host", default="127.0.0.1")
    opts = parser.parse_args()
    server = ThreadingHTTPServer((opts.host, opts.port), Handler)
    print(f"orders-api sandbox listening on http://{opts.host}:{opts.port}")
    print("Seed: O1 cust-a PAID · O2 cust-a SHIPPED · O3 cust-a PENDING · O4 cust-b PAID")
    print(f"Seeded defect: DEF-5561 — reason_note of {PLANTED_NOTE_ACCEPTED} chars is accepted")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Orders API — training sandbox for the Module 16 requirement-to-test pipeline.

Zero third-party dependencies. Run it in a terminal:

    python3 sandbox/orders_api.py          # http://127.0.0.1:8000
    python3 sandbox/orders_api.py 8765     # custom port

State is in memory; restarting resets it. Test-support endpoints:

    POST /_test/orders    create an order   -> 201 {id, owner, status, amount}
    POST /_test/reset     restore seed data -> 204

Read-only fixture: copy this file into your pipeline repo before editing.
"""

import json
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

SEED_ORDERS = (
    {"id": "O1", "owner": "cust-a", "status": "PAID", "amount": 120.0},
    {"id": "O2", "owner": "cust-a", "status": "SHIPPED", "amount": 80.0},
    {"id": "O3", "owner": "cust-a", "status": "PENDING", "amount": 50.0},
    {"id": "O4", "owner": "cust-b", "status": "PAID", "amount": 200.0},
)


def error(code, message):
    return {"error": {"code": code, "message": message}}


class Store:
    """In-memory order and refund state, protected by a lock."""

    def __init__(self):
        self._lock = threading.Lock()
        self.orders = {}
        self.refunds = []
        self._next_test_id = 1
        self.reset()

    def reset(self):
        with self._lock:
            self.orders = {o["id"]: dict(o) for o in SEED_ORDERS}
            self.refunds = []
            self._next_test_id = 1

    def create_order(self, owner, status, amount):
        with self._lock:
            order = {
                "id": f"T{self._next_test_id}",
                "owner": owner,
                "status": status,
                "amount": amount,
            }
            self._next_test_id += 1
            self.orders[order["id"]] = order
            return dict(order)

    def get_order(self, order_id):
        with self._lock:
            order = self.orders.get(order_id)
            if order is None:
                return 404, error("ORDER_NOT_FOUND", f"No order {order_id}")
            return 200, dict(order)

    def cancel_order(self, order_id, customer):
        with self._lock:
            order = self.orders.get(order_id)
            if order is None or order["owner"] != customer:
                return 404, error("ORDER_NOT_FOUND", f"No order {order_id} for this customer")
            if order["status"] == "SHIPPED":
                return 409, error("ORDER_ALREADY_SHIPPED", "A shipped order cannot be cancelled")
            previous = order["status"]
            order["status"] = "CANCELLED"
            if previous == "PAID":
                self.refunds.append(
                    {"order_id": order_id, "status": "PENDING", "amount": order["amount"]}
                )
            return 200, dict(order)

    def list_refunds(self, order_id):
        with self._lock:
            if order_id not in self.orders:
                return 404, error("ORDER_NOT_FOUND", f"No order {order_id}")
            return 200, {
                "refunds": [dict(r) for r in self.refunds if r["order_id"] == order_id]
            }


class Handler(BaseHTTPRequestHandler):
    store = Store()

    # -- routing -----------------------------------------------------------

    def do_GET(self):
        route = urlparse(self.path)
        path, query = route.path, parse_qs(route.query)

        if path == "/health":
            return self._send(200, {"status": "ok"})

        if path.startswith("/orders/") and path.count("/") == 2:
            status, body = self.store.get_order(path.split("/")[2])
            return self._send(status, body)

        if path == "/refunds":
            order_id = (query.get("order_id") or [None])[0]
            if not order_id:
                return self._send(
                    400, error("MISSING_ORDER_ID", "order_id query parameter is required")
                )
            status, body = self.store.list_refunds(order_id)
            return self._send(status, body)

        return self._send(404, error("NOT_FOUND", f"Unknown path {path}"))

    def do_POST(self):
        path = urlparse(self.path).path
        body = self._read_json()
        customer = self.headers.get("X-Customer")

        if path.startswith("/orders/") and path.endswith("/cancel"):
            order_id = path.split("/")[2]
            if not customer:
                return self._send(401, error("MISSING_CUSTOMER", "X-Customer header is required"))
            status, payload = self.store.cancel_order(order_id, customer)
            return self._send(status, payload)

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

    def log_message(self, fmt, *args):  # keep the terminal readable during lab runs
        pass


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"Orders API sandbox listening on http://127.0.0.1:{port}")
    print("Seed: O1 PAID cust-a · O2 SHIPPED cust-a · O3 PENDING cust-a · O4 PAID cust-b")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()

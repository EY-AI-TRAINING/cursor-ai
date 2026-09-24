# Offline kit — run the Module 16 pipeline with zero infrastructure

> **Path B fallback.** Use this only if your facilitator's sandbox API is not available. The lab itself
> (agents, pipeline, artifacts, review) is identical — only the target API changes. Everything here uses
> the Python standard library: no `pip install` required.

## What is in the kit

| File | What it is |
|---|---|
| `sandbox/orders_api.py` | The target API under test — in-memory orders and refunds, stdlib only |
| `tests/conftest.py` | The fixture contract (`api`, `customer_a`, `customer_b`, `make_order`) |
| `pytest.ini` | Registers the `req` / `ac` / `seq` markers |

The source requirement and API contract are shipped one level up in this pack (copy them too):

- [`../REQ-2481.md`](../REQ-2481.md) → `requirements/REQ-2481.md`
- [`../openapi-excerpt.yaml`](../openapi-excerpt.yaml) → `specs/openapi.yaml`

## Set up your pipeline repo

From your lab pack folder, with `<pipeline-root>` set to your `requirement-to-test/` workspace:

```bash
mkdir -p <pipeline-root>/{requirements,specs,tests,sandbox,runs}

cp samples/REQ-2481.md                 <pipeline-root>/requirements/REQ-2481.md
cp samples/openapi-excerpt.yaml        <pipeline-root>/specs/openapi.yaml
cp samples/offline-kit/tests/conftest.py <pipeline-root>/tests/conftest.py
cp samples/offline-kit/pytest.ini      <pipeline-root>/pytest.ini
cp -r samples/offline-kit/sandbox      <pipeline-root>/sandbox
```

## Run it

```bash
# terminal 1 — keep it running for the whole lab
python3 <pipeline-root>/sandbox/orders_api.py

# terminal 2 — smoke check
curl -s http://127.0.0.1:8000/health
curl -s http://127.0.0.1:8000/orders/O1 -H 'X-Customer: cust-a'
curl -s -X POST http://127.0.0.1:8000/orders/O4/cancel -H 'X-Customer: cust-a'
```

If port 8000 is taken, run `python3 sandbox/orders_api.py 8765` and export
`ORDERS_API_URL=http://127.0.0.1:8765` before running PyTest.

## Seed data

| Order | Owner | Status | Amount |
|---|---|---|---|
| O1 | `cust-a` | PAID | 120.00 |
| O2 | `cust-a` | SHIPPED | 80.00 |
| O3 | `cust-a` | PENDING | 50.00 |
| O4 | `cust-b` | PAID | 200.00 |

Creating an order for a test (`make_order`) returns a fresh id (`T1`, `T2`, …); `POST /_test/reset`
restores the seed if a manual rerun needs a clean slate.

## Endpoints

| Method | Path | Notes |
|---|---|---|
| `POST` | `/orders/{id}/cancel` | Header `X-Customer` required; 200 / 400 / 401 / 403 / 404 / 409 per `specs/openapi.yaml` |
| `GET` | `/orders/{id}` | Order status and owner |
| `GET` | `/refunds?order_id={id}` | Refund records for one order |
| `POST` | `/_test/orders` | Test support: create an order (`{"owner": …, "status": …, "amount": …}`) |
| `POST` | `/_test/reset` | Test support: restore seed data |
| `GET` | `/health` | Liveness check |

## Rules

1. **Copy, don't edit the pack.** Files under `labs/module-16/samples/` are read-only fixtures.
2. **The sandbox is the product under test, not your code.** If a test and the sandbox disagree, the
   API Validator classifies the failure — a "fix" to the test that only makes the suite green is a hiding
   move, not a fix (Module 16, §4).
3. **The fixture contract is `tests/conftest.py`.** Generated tests use `api` / `customer_a` /
   `customer_b` / `make_order`; new fixtures go into `conftest.py`, never into a test file.

---

*Fixture for Module 16 — read-only in the lab pack. The sandbox's behaviour is the point: run tests
against it, classify what you find, and let the pipeline's stages report honestly.*

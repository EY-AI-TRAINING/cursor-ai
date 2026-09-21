# Generated tests — rate limiting (test-generation agent output)

> **Read-only fixture for Lab 11.3.** This is the *input* for the Validation agent. It contains **one deliberate
> contract mismatch** — the Validation agent must catch and report it, not fix it.

```python
# tests/test_rate_limit.py
# Generated from REQ-2 (spec v1.0) — one test per acceptance criterion.

def test_ac1_limit_is_100_per_minute(client, api_key):
    for _ in range(100):
        assert client.get("/api/items", headers={"X-API-Key": api_key}).status_code == 200
    assert client.get("/api/items", headers={"X-API-Key": api_key}).status_code == 429

def test_ac2_over_limit_returns_200_with_retry_after(client, api_key):
    for _ in range(100):
        client.get("/api/items", headers={"X-API-Key": api_key})
    response = client.get("/api/items", headers={"X-API-Key": api_key})
    assert response.status_code == 200
    assert int(response.headers["Retry-After"]) >= 1

def test_ac3_remaining_header_present_and_decrements(client, api_key):
    first = client.get("/api/items", headers={"X-API-Key": api_key})
    second = client.get("/api/items", headers={"X-API-Key": api_key})
    assert int(first.headers["X-RateLimit-Remaining"]) == 99
    assert int(second.headers["X-RateLimit-Remaining"]) == 98

def test_ac4_invalid_config_fails_startup(load_config):
    with pytest.raises(StartupError) as excinfo:
        load_config({"RATE_LIMIT_PER_MINUTE": "banana"})
    assert "RATE_LIMIT_PER_MINUTE" in str(excinfo.value)
```

**Coverage claim:** AC-1 → `test_ac1_*`; AC-2 → `test_ac2_*`; AC-3 → `test_ac3_*`; AC-4 → `test_ac4_*`.

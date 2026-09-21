# rate_limit_middleware.py — request path excerpt

> **Fixture for Module 12.** Stands in for repository code when a cohort has no Module 9 implementation of
> rate limiting. Copy into `<sandbox-repo>/knowledge/` (or ask about your own repo's file instead — better).

**Source class:** Repository code · **Path:** `src/middleware/rate_limit_middleware.py` · **Commit:** `<hash>`

```python
def rate_limit_middleware(request, call_next):
    """Enforce the per-API-key limit before the handler runs."""
    decision = check_rate_limit(request.headers["X-API-Key"])

    if not decision.allowed:
        return Response(
            status_code=429,
            headers={"Retry-After": str(decision.retry_after_seconds)},
            body={"error": "rate_limit_exceeded", "retry_after": decision.retry_after_seconds},
        )

    response = call_next(request)
    response.headers["X-RateLimit-Remaining"] = str(decision.remaining)
    return response
```

The check is invoked in the middleware chain **before handler dispatch**; over-limit requests short-circuit with
`429` and never reach the handler. Successful responses are annotated with the remaining count.

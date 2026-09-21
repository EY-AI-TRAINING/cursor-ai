# SDS excerpt — Rate limiting (spec v1.0)

> **Fixture for Module 12.** Part of the grounding corpus. Copy [`samples/knowledge-base/`](.) into
> `<sandbox-repo>/knowledge/` for the MCP walkthrough (Lab 12.2). Do not edit the fixture originals.

**Source class:** SRS/SDS document (Module 9 artifact) · **Owner:** API platform · **Status:** approved

## Design intent

- Enforcement point: application middleware inside the API service, before handler dispatch.
- Limiting key: **API key** (not source IP, not user).
- Default limit: **100 requests / 60 s**; test environment 1000/min; configured via `RATE_LIMIT_PER_MINUTE`.
- Over-limit response: **HTTP 429** with `Retry-After` and JSON body `{"error": "rate_limit_exceeded", "retry_after": <s>}`.
- Successful responses carry `X-RateLimit-Remaining` (remaining count for the current window).
- Storage: **in-memory sliding window per instance**; no shared store in this iteration.

## Explicit non-goals

- No distributed/global limiting across service instances (noted as future work).
- **No gateway-level enforcement changes** — gateway configuration is owned by the platform team.

## Open issue

- Gateway-level limits are out of scope for this design. Before raising any per-key limit above 100/min,
  check the platform runbook and the historical defect log — see `runbook-api-gateway.md` and `defect-log.md`.

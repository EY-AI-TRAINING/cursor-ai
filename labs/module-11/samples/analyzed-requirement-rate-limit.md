# Analyzed requirement — REQ-2 (rate limiting)

> **Read-only fixture for Lab 11.3.** This is the *input* for the Test Generation agent and part of the input for
> the Documentation agent. It models the output shape the Requirement Analysis agent must produce:
> `{complete, testable, gaps[]}`.

```yaml
req_id: REQ-2
source: ticket "<id> — Add rate limiting to the API"
spec: specs/rate-limit/spec.md v1.0
complete: true
testable: true
gaps: []
```

## Scope

Rate limiting applies to all public API endpoints, keyed by API key.

## Acceptance criteria

| ID | Criterion |
|---|---|
| AC-1 | Each API key is limited to **100 requests per 60-second window** across all endpoints (default; test environment 1000/min). |
| AC-2 | A request over the limit returns **HTTP 429** with a `Retry-After` header containing the number of seconds until the window resets. |
| AC-3 | Every successful response includes an `X-RateLimit-Remaining` header with the remaining request count for the current window. |
| AC-4 | The limit is configurable per environment via the `RATE_LIMIT_PER_MINUTE` setting; an invalid value fails startup with a clear error. |

## Explicit exclusions

- No per-endpoint quotas in this iteration.
- No burst allowance or token-bucket smoothing.

## Non-functional constraints

- Rate-limit check adds ≤ 5 ms p95 to request handling.
- Existing clients that stay under the limit see no behavioural change.

## Gap resolution notes (from clarification)

- Limit values, window size, and error behaviour were underspecified in the raw ticket; resolved with the spec owner on <date>.
- "Fast" was replaced with the measurable p95 budget above.

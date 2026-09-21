# Interface contract — rate limiting (spec v1.0)

> **Read-only fixture for Lab 11.3.** This is the *input* for the Validation agent, together with the generated
> test suite. The contract is the authority: the agent flags mismatches and never edits this file.

## Endpoints and headers

| Clause | Contract |
|---|---|
| C-1 | All public API responses include `X-RateLimit-Remaining`: integer ≥ 0. |
| C-2 | A request over the limit returns **HTTP 429**; the body is `{"error": "rate_limit_exceeded", "retry_after": <seconds>}`. |
| C-3 | A 429 response **MUST** include the `Retry-After` header with the same `<seconds>` value as the body. |
| C-4 | Config key `RATE_LIMIT_PER_MINUTE` (default `100`) sets the per-minute limit; invalid values abort startup with exit code 2 and a message naming the setting. |
| C-5 | Successful (2xx) responses decrement `X-RateLimit-Remaining` by exactly 1 per request. |

## Traceability

- C-1, C-5 → AC-3
- C-2, C-3 → AC-2
- C-4 → AC-4

# Historical defect log (excerpt)

> **Fixture for Module 12.** Part of the grounding corpus — a source class introduced in this module.
> Copy into `<sandbox-repo>/knowledge/` for the MCP walkthrough. Do not edit the fixture original.

**Source class:** Historical defect log · **Owner:** Quality engineering · **Export date:** <date>

| ID | Component | Summary | Root cause | Resolution |
|---|---|---|---|---|
| **DEF-097** | session | Retry storm after session timeout | Client retried on 401 without backoff or jitter | Client retry policy updated with exponential backoff |
| **DEF-118** | api-gateway | Clients saw `429`s with **no** `Retry-After` header, and the app's rate-limit dashboard showed no limiting at all | App limit was raised to **150/min per API key** while the gateway enforces **200/min per source IP**; the gateway rejected requests first, so the app never counted them | App limits aligned below the gateway limit; gateway limits documented in the runbook; alert added for gateway `429`s |
| **DEF-131** | rate-limiter | `X-RateLimit-Remaining` occasionally jumped between requests | In-memory per-instance windows + clock skew across instances | Per-instance semantics documented; clients told not to treat the header as a global count |
| **DEF-140** | invoices | Duplicate invoice submissions under retry | Missing idempotency-key check on `POST /invoices` | Idempotency-key validation added |

**Known failure pattern:** limits configured above the gateway's per-source-IP ceiling cause gateway rejections that
are invisible to application-level metrics (see DEF-118).

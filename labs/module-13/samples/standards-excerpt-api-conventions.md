# Standards excerpt — API conventions (v2.1)

> **Fixture for Module 13.** Source class: **Standards** — the category the guide reaches via a Project Rule
> (Module 8). Promote this into `<sandbox-repo>/.cursor/rules/api-conventions.mdc` (canonical copy in
> `shared-agent-library/rules/`), or use your own Module 8 standards rule instead. Do not edit the fixture original.

**Source class:** Standards · **Owner:** API platform · **Status:** active

## Error responses

- A `429` response MUST include `Retry-After` (seconds).
- Rate-limit error bodies MUST follow `{"error": "<code>", "retry_after": <seconds>}`.

## Rate-limit headers

- Successful responses SHOULD include `X-RateLimit-Remaining` (remaining count for the current window).

## Limits

- A change to any published limit MUST be recorded in the service runbook before release.
- Where a platform constraint prevents a standard, the exception MUST be documented in the runbook and cited
  when the standard is discussed.

## Secrets

- No credentials in code, logs, or configuration files.

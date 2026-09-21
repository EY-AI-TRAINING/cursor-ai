# Runbook — API gateway (excerpt)

> **Fixture for Module 12.** Part of the grounding corpus — enterprise knowledge (org-specific behaviour no
> generic model would know). Copy into `<sandbox-repo>/knowledge/` for the MCP walkthrough.

**Source class:** Enterprise knowledge (runbook) · **Owner:** Platform team · **Last reviewed:** <date>

## Limits

- The gateway enforces **200 requests/min per source IP** (platform-managed; **not** per API key).
- Gateway `429` responses include `Retry-After` but **do not** include `X-RateLimit-Remaining`.
- The gateway **strips `X-Forwarded-For`** before forwarding requests to services.
- Multiple clients behind one NAT/egress IP share the same gateway limit.

## Routing

- All public traffic passes through the gateway; direct-to-service access is blocked.

## Log retention

- Gateway access logs are retained **30 days** for operational debugging only.

## Escalation

- Changing gateway limits requires a platform-team ticket; lead time is **5 business days**.

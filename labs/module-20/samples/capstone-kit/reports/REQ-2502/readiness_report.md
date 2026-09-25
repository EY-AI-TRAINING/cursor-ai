# Deployment readiness — REQ-2502 · req-2502-run-01 · policy readiness.yaml v1.0.0

Decision: **READY** (staging)

| Criterion | Result | Evidence |
|---|---|---|
| CI checks (gates) | PASS | Actions run #1931 (or labelled local simulation — see report §11) |
| Pipeline gates G1–G5 | PASS / ESCALATE→signed | `gate_log.jsonl` lines 2–11 |
| Human sign-off (hash-bound) | APPROVE `human:qa-lead`, tests hash = current | `gate_log.jsonl` HITL_signoff |
| AC coverage | 4/4 ACs, ≥1 test each | `traceability.md` |
| Known defects | DEF-5561 Sev-3, strict xfail, ticket open → allowed | readiness policy §known_defects |
| Security | secret scan clean; dependency review: 0 high; hook denies/reverts explained | `security.md` |
| Unknown criteria | none | — |

Policy notes:

- `on_unknown: NOT_READY` — nothing above was evaluated as unknown. The dependency review was
  executed (simulated locally where no GitHub sandbox was available, labelled as such).
- The policy file was **not modified** for this ticket. A new ticket must not get a new rule book.
- Promotion is a separate human act (environment required reviewer); READY ≠ deployed.

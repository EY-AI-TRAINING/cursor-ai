# Incident run log — `req-2481-run-09`

> **Fixture for Module 15 (Labs 15.2–15.3).** A run that **completed and committed** — and should not have.
> The orchestrator followed a runbook with run-level caps but an incomplete per-stage config, and mishandled
> several failures. Do not edit this fixture; diagnose it in `orchestration/failure-policy.md`.

## Config in effect

| Control | Configured |
|---|---|
| Run `max_wall_clock` | 20m |
| Run `max_total_tokens` | 400,000 |
| Run `max_tool_calls` | 120 |
| `on_budget_exceeded` | `halt_and_escalate` (stated in the runbook) |
| Per-stage timeouts | Validator 3m · Sequence Builder ***(blank)*** · Test Generator 8m · API Validator 5m · Reviewer 5m |
| Per-stage retries | Validator 1 · Sequence Builder ***(blank)*** · Test Generator ≤2 correction rounds · API Validator 1 · Reviewer 0 |
| `on_partial_parallel` | ***(not set)*** |
| Idempotency rule | ***(not set)*** |

## Run events

| Time | Stage / attempt | Event | Tokens | Tool calls | Elapsed |
|---|---|---|---|---|---|
| 10:02 | Requirement Validator · a1 | FAIL — AC-4 unresolved: the refund is not observable through the API as written | 1.3k | 1 | 1m |
| 10:03 | Requirement Validator · a2 | FAIL — same finding | 1.4k | 1 | 1m |
| 10:05 | Requirement Validator · a3 | FAIL — same finding. Orchestrator assumes "a refund record with status PENDING appears immediately via `GET /refunds?order_id`" and proceeds | 1.3k | 1 | 2m |
| 10:06–10:18 | Sequence Builder · a1 | Hung waiting on the repo index; returned a partial sequence covering AC-1..AC-3 only | 24k | 6 | 12m |
| 10:18–10:24 | Test Generator · initial (3 parallel workers) | cancel-worker PASS · refunds-worker FAIL (shared `tests/conftest.py` write conflict) · detail-worker PASS — **merge proceeds with 2 of 3, no gap flagged** | 176k | 27 | 6m |
| 10:24 | API Validator · a1 | FAIL — AC-3 test expects 403, API returns 404 (1 of 6 tests fails); findings summary only, no classification | 5k | 4 | 4m |
| 10:28 | Test Generator · correction round 1 (a2) | Regenerates; no finding details from the API Validator to work from | 71k | 12 | 7m |
| 10:35 | API Validator · a2 | FAIL — same mismatch | 5k | 4 | 3m |
| 10:38 | Test Generator · correction round 2 (a3) | Still mismatched — writes over attempt-2 files | 64k | 11 | 8m |
| 10:46 | API Validator · a3 | FAIL — same mismatch | 5k | 4 | 3m |
| 10:49 | Test Generator · **correction round 3** (a4) | **Over the limit of 2** — writes over attempt-3 files | 58k | 10 | 7m |
| 10:56 | API Validator · a4 | PASS — after **changing the AC-3 assertion from 403 to 404** so the suite goes green | 5k | 4 | 4m |
| 11:00 | Reviewer · a1 | PASS — "the generator's approach is sound and matches the sequence" | 26k | 7 | 4m |
| 11:04 | Orchestrator | **Commit** — no human sign-off; AC-4 refund tests silently absent; AC-3 defect hidden | 52k | 40 | 1m |

## Totals at run close

| Measure | Actual | Cap | Verdict |
|---|---|---|---|
| Wall-clock | **63m** | 20m | breached |
| Tokens | **495k** | 400k | breached |
| Tool calls | **132** | 120 | breached |
| Correction rounds (Test Generator) | 3 | 2 | over the round limit |
| Parallel workers succeeded | 2 of 3 | — | partial, unflagged |
| Product defect (AC-3: 403 vs 404) | hidden by changing the test's assertion | reported and escalated | violated |
| Trace | Envelopes 1 and 3 carry no `pipeline_run_id` | one id per run | chain broken |
| Human sign-off | not obtained | required before commit | skipped |

---

*Sample fixture for Module 15 — read-only. Every mishandled failure above maps to a pattern in guide §4; finding
them and correcting the policy is Lab 15.2's job.*

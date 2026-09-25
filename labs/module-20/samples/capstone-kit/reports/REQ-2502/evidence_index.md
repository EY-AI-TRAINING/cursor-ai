# Evidence index — REQ-2502 · req-2502-run-01

Every claim in the final report resolves to a row here. Hashes are sha256[:12].

| Path | sha256[:12] | Produced by |
|---|---|---|
| `runs/req-2502-run-01/00_requirement_bundle.json` | `001dd2869422` | tool: ticket_to_bundle.py (read via MCP) |
| `plans/REQ-2502/exploration.md` | `333e27713b28` | agent: explorer subagent (read-only) |
| `plans/REQ-2502/plan.md` | `b922c47295f3` | agent: planner; reviewed by humans |
| `plans/REQ-2502/plan_approval.json` | `a0c2d2989b38` | human: plan approver (approve.py --checkpoint plan) |
| `specs/REQ-2502-spec-note.md` | `d0dd5d2afa4f` | agent: planner; confirmed by human:ticket-owner |
| `runs/req-2502-run-01/02_test_sequence.json` | `5b79339914af` | agent: sequence-builder |
| `tests/test_req_2502_cancel_reason.py` | `5da0cf32e478` | agent: test-generator |
| `tests/test_req_2502_audit.py` | `ca126fd29db4` | agent: test-generator |
| `runs/req-2502-run-01/04_api_validation.json` | `0c5cdbe39bd7` | tool: api-validator |
| `runs/req-2502-run-01/04_api_validation_report.md` | `e222d11fdb10` | tool: api-validator |
| `runs/req-2502-run-01/05_review_signoff.md` | `c91ab0e7fad6` | agent: reviewer (separate context) |
| `runs/req-2502-run-01/gate_log.jsonl` | `af09b25899d2` | tool: gate engine |
| `runs/req-2502-run-01/run_log.jsonl` | `676b722bf225` | tool: pipeline stages |
| `runs/req-2502-run-01/decision_packet.md` | `b6219f2219a1` | tool: decision_packet.py (from the logs) |
| `runs/req-2502-run-01/traceability.md` | `4c4a285c69b3` | tool: traceability builder |
| `defects/DEF-5561.json` | `3f25c47087d3` | human-approved MCP write (DEF raised) |
| `reports/REQ-2502/readiness_report.md` | `d5c1d5c5920d` | tool: readiness.py (policy v1.0.0) |
| `reports/REQ-2502/final_engineering_report.md` | `78a2331c0477` | human: report owner (links the chain) |
| `reports/REQ-2502/checklist.md` | `8b85b615ad42` | human: report owner |
| `reports/REQ-2502/cost_summary.md` | `2addb8876f5a` | tool: cost_summary.py |
| `reports/REQ-2502/security.md` | `fcb9e5c3574a` | tool: scans + hook-log summary |
| `notes/capstone/delegation.md` | `926a5978db67` | human: delegation owner |


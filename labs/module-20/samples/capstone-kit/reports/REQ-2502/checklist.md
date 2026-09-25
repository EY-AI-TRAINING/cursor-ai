# Engineering checklist — REQ-2502 · req-2502-run-01

| # | Item | Evidence | ✔ |
|---|---|---|---|
| CA-1 | Ticket pulled via MCP (or mock); bundle schema-valid; injection warning recorded | `runs/req-2502-run-01/00_requirement_bundle.json`, `raw_ticket.json`, `warnings[]` | ☑ |
| CA-2 | Plan approved (hash-bound) **before** generation | `plans/REQ-2502/plan_approval.json` ts 09:14:05Z < first `test-generator` ts 09:31:00Z | ☑ |
| CA-3 | Spec note AC-IDs = bundle AC-IDs; owner confirmed | `specs/REQ-2502-spec-note.md` (AC-1…AC-4); CL-1/CL-2 | ☑ |
| CA-4 | Sequence + suite; every test has `req` + `ac` markers | `02_test_sequence.json`; `tests/test_req_2502_*.py`; G3 `markers_present` | ☑ |
| CA-5 | Executed vs. sandbox; failures classified | `04_api_validation.json`, `findings/round-1.json` | ☑ |
| CA-6 | Independent reviewer verdict (separate context) | `05_review_signoff.md` | ☑ |
| CA-7 | ≥1 correction round + hash-bound sign-off | `gate_log.jsonl` LOOP + `HITL_signoff` | ☑ |
| CA-8 | CI green (or **labelled** simulation) + readiness from versioned policy | CI run #1931 / local simulation note; `readiness_report.md` | ☑ |
| CA-9 | Final report links the whole chain + cost summary | `final_engineering_report.md`, `cost_summary.md` | ☑ |
| CA-10 | *(optional)* Delegated task + checklist | `notes/capstone/delegation.md` | ☑ (simulated, labelled) |

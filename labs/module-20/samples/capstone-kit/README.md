# Capstone kit — Module 20 (Path B)

> **A complete, runnable REQ-2502 package.** Use it when you do not have a live Jira, a GitHub
> sandbox, or your own Modules 18–19 repository available: the kit contains the unseen ticket,
> the contract, a mock sandbox with one planted product defect, a reference test suite and a
> reference report package that passes `tools/package_check.py`. Every lab in this pack can be
> completed against it.

```bash
# 1. copy the kit into a working directory (never edit the pack in place)
cp -r labs/module-20/samples/capstone-kit /tmp/req-2502-capstone
cd /tmp/req-2502-capstone

# 2. run the whole reference story (needs Python 3.11+ with pytest and pyyaml)
PYTHON=/path/to/python3 ./run_reference.sh
```

`run_reference.sh` starts the sandbox and proves, in order:

| Step | Expect |
|---|---|
| Round-0 variants | **2 failed, 10 passed** — F-1 (audit ordering, TEST_DEFECT) and F-2 (281-char note, PRODUCT_DEFECT) |
| Reference suite (round 1) | **11 passed, 1 xfailed** — the xfail is `strict=True`, bound to DEF-5561 |
| G1/G2 sequence gate | PASS — 4 ACs, 7 scenarios, error criteria have negative/boundary coverage |
| `package_check.py` | all required CA rows PASS |
| `cost_summary.py` | 173,000 tokens, 20.6 min, ~USD 1.04 at 6.0 USD/MTok |

## What is in the kit

| Path | What it is |
|---|---|
| `capstone.yaml` | The run manifest from §0 — the single identity source every tool reads |
| `tickets/REQ-2502.json` | The unseen ticket: AC-1…AC-3 structured, AC-4 as prose, one injection comment |
| `tickets/REQ-2502-clarifications.md` | The ticket owner's CL-1/CL-2 answers (the human confirmation AC-4 needs) |
| `specs/openapi.yaml` | The contract: `CancelRequest`, `AuditEntry`, error codes, `maxLength: 280` |
| `specs/REQ-2502-spec-note.md` | Reference one-page SDD note with Given/When/Then and decisions |
| `tools/mock_ticket_mcp.py` | The Module 19 mock ticketing MCP server (unchanged; point `--fixtures` at `tickets/`) |
| `tools/mock_sandbox_api.py` | The REQ-2502 execution target — **contains planted DEF-5561** |
| `tools/sequence_gate.py` | Reference G1/G2 check over bundle + sequence |
| `tools/package_check.py` | Reference CA-1…CA-10 check (a floor, not a verdict) |
| `tools/cost_summary.py` | Reference observability/cost table from `run_log.jsonl` + `gate_log.jsonl` |
| `tools/summarise_hooks.py` | Hook-log counts + every deny/revert, for the report (no `jq` needed) |
| `tools/evidence_index.py` | Generates `evidence_index.md` with real sha256[:12] per artifact |
| `tests/conftest.py` | Fixtures: `api`, `customer_a`, `customer_b`, `support_user`, `make_order` |
| `tests/test_req_2502_cancel_reason.py` | Reference round-1 tests for AC-1…AC-3 |
| `tests/test_req_2502_audit.py` | Reference round-1 tests for AC-4 |
| `tests/variants/round0/` | Generator output with the two seeded test defects (`F-1`, `F-2`) |
| `plans/REQ-2502/` | Reference `exploration.md`, `plan.md`, `plan_approval.json` (hash-bound) |
| `runs/req-2502-run-01/` | Reference artifacts `00`, `02`, `04`, `05`, findings, gate/run logs, decision packet, traceability |
| `runs/hook_log.jsonl` | Hook events incl. the denied injection, denied force-push, reverted control-plane edit |
| `reports/REQ-2502/` | Reference final report, checklist, readiness report, security, cost, evidence index |
| `notes/capstone/` | Delegation (simulated + labelled), seeded faults, retro |
| `defects/DEF-5561.json` | The raised product defect fixture |

## The planted defect (do not "fix" the test)

`POST /orders/{id}/cancel` accepts `reason_note` of **exactly 281 characters** (returns 200) while
the contract says `maxLength: 280` and notes above 281 are rejected. The correct capstone handling
is: classify as `PRODUCT_DEFECT` → raise `DEF-5561` → keep the test strict → convert to
`xfail(strict=True, reason="DEF-5561…")` at sign-off → readiness allows Sev-3 with the ticket open.

Other sandbox behaviour worth knowing: a non-owner cancel returns **404** (the DEF-5520 family,
outside REQ-2502's ACs); `GET /orders/{id}/audit` returns **403** for other customers and
**newest first** for the owner/support (CL-1, CL-2).

## Rules

1. **Copy, don't edit the pack.** Everything under `labs/module-20/samples/` is a read-only fixture.
2. **The reference is one valid answer, not the answer.** Your package is graded on its own
   evidence, honesty and traceability — reuse the shapes, not the strings.
3. **Label every simulation.** No GitHub sandbox, no cloud agent, no MCP runtime is fine as long as
   the report says exactly which steps were simulated. Hidden simulation fails CA-8 in spirit.
4. **Hashes are earned.** `plan_approval.json` and the `HITL_signoff` hash were computed from the
   reference files; in your run they come from your own `approve.py`.

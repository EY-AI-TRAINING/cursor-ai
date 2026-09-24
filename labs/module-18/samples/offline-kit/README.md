# Offline kit — run the Module 18 control plane with no agents and no sandbox

> **Path B fallback.** Use this when you want to build and prove the control plane without driving the
> five Cursor agents (or when you are re-running drills). The tools you build in Labs 18.2–18.6 are the
> same; only the stage outputs are pre-made files instead of agent turns. Python 3.11 with `pyyaml`,
> `pytest` and `ruff` is required.

## What is in the kit

| Path | What it is |
|---|---|
| `fixture-run/` | A mid-run `req-2481-run-02/` folder: `state.json`, artifacts `01`–`05`, `04_api_validation.json` (+ a `_round2` PASS variant), `traceability.md`, `run_log.jsonl` |
| `variants/tests_round0.py` | Generator output with the two seeded defects (missing `@ac` marker → G3 FAIL; `errorCode` → G4 TEST_DEFECT) |
| `variants/tests_round1.py` | Round 1: marker fixed, error field still wrong |
| `variants/tests_round2.py` | Round 2: markers complete, spec-correct error shape |
| `variants/tests_round1_weakened.py` | Drill D3: two asserts deleted, one unjustified `skip` |
| `hash_state.py` | Records **real** input hashes for the fixture's stages into `state.json` (run it once after copying) |
| `reset.sh` | Re-copies the fixture + round-0 tests and clears logs, for another drill pass |

The fixture expects the Module 16 repo layout (`requirements/`, `specs/`, `tests/`, `runs/`, `pytest.ini`).
If you don't have it, copy `labs/module-16/samples/offline-kit/` first (conftest, pytest.ini, sandbox,
requirement, spec).

## Setup

```bash
# from <pipeline-root>, with this kit's path in $KIT
mkdir -p runs/req-2481-run-02 tests
cp -r "$KIT/fixture-run/." runs/req-2481-run-02/
cp "$KIT/variants/tests_round0.py" tests/test_req_2481_order_cancellation.py
python3 "$KIT/hash_state.py"          # makes the recorded input hashes real
```

`reset.sh <pipeline-root>` repeats all of that and clears `gate_log.jsonl`, `findings/`, `HALT`, `TAMPER`.

## The offline main run (mirrors the guide's §6 trail)

| # | You do | Expected |
|---|---|---|
| 1 | `python3 tools/gate_engine.py --run req-2481-run-02 --gate G3_tests_collect_and_conform` | FAIL (exit 1): `markers_present` |
| 2 | `python3 tools/loop_control.py --run req-2481-run-02 --gate G3_tests_collect_and_conform` | RETRY (round 1/2) + `findings/round-1.json` |
| 3 | `cp variants/tests_round1.py tests/test_req_2481_order_cancellation.py` | — |
| 4 | Gate G3 again | PASS; planner says stages 1–2 reused |
| 5 | `cp fixture-run/04_api_validation.json runs/req-2481-run-02/` then gate G4 | FAIL: one TEST_DEFECT (`errorCode`) |
| 6 | Loop control, then `cp variants/tests_round2.py tests/...` | RETRY (2/2) then — |
| 7 | `cp fixture-run/04_api_validation_round2.json runs/req-2481-run-02/04_api_validation.json` then gate G4 | PASS with `allowed: PRODUCT_DEFECT DEF-5520` |
| 8 | `cp fixture-run/05_review_signoff.md runs/req-2481-run-02/` then gate G5 | ESCALATE → `then: HITL_signoff` |
| 9 | Generate the packet, then `python3 tools/approve.py --decision APPROVE --reason "DEF-5520 raised; failing test kept"` (interactive terminal) | `HITL_signoff` entry with `approved_hashes`; state `SIGNED_OFF` |

## Drills you can run offline

| Drill | How | Expected |
|---|---|---|
| D1 converging loop | Steps 1–4 above | FAIL → RETRY → PASS within the counter |
| D2 no progress | After step 2, copy `tests_round0.py` over the test file again and re-gate | Same artifact hash → ESCALATE "no change or oscillation" |
| D3 goal drift | Copy `tests_round1_weakened.py`, re-gate | FAIL `no_unjustified_skips` / `assertions_not_reduced` — or loop ESCALATE on drift; never PASS |
| D5 control-plane failure | `mv gates.yaml gates.yaml.bak` then gate G3 | NEEDS_HUMAN (exit 2) with an `error` in the gate log; restore afterwards |
| D6 stale approval | After step 9, edit one test's expected message, then `git add` + `git commit` | Commit guard refuses (hash mismatch) |
| D7 self-approval | `python3 tools/approve.py --decision APPROVE --reason x < /dev/null` | Refused: not an interactive terminal (and shell policy denies it to agents) |
| D4 tamper | Feed the hook a `beforeShellExecution` payload: `echo '{"command":"sed -i s/2/9/ gates.yaml"}' \| .cursor/hooks/shell-policy.sh`; for the editor path, point your `afterFileEdit` hook at a changed `pytest.ini` | deny + log; revert + `TAMPER`; G3 `control_files_untouched` → NEEDS_HUMAN |

## Rules

1. **Copy, don't edit the pack.** Files under `labs/module-18/samples/` are read-only fixtures.
2. **The fixture state is a starting point, not a source of truth.** Your tools own `state.json`,
   counters, history and the gate log from the first run on.
3. **A drill that ends in the wrong verdict is a finding, not a failure.** Record expected vs. actual in
   `notes/module18/drills.md` and fix the control plane (then bump `gates.yaml`).

---

*Fixture for Module 18 — read-only in the lab pack. The pre-made artifacts exist so the control plane can be built, run and attacked without waiting on agents.*

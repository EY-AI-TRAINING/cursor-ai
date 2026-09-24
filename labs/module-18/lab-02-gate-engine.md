# Lab 18.2 — Build the Gate Engine: Verdicts, Cheap-First, Fail-Safe

**Xebia — Cursor AI Training | AI-Assisted Software Engineering**
Day 6 · Module 18 · Lab 18.2 of 8 · ~20 min · Build (individual)

> **Objective:** turn `gates.yaml` into a function from artifacts to verdict. Build a deterministic
> gate engine with the four properties — deterministic, ordered cheap-first, three-valued, fail-safe —
> and an append-only log that can answer "why was this allowed through?" without a transcript.

**Guide reference:** §1 Add Automated Gates Between the Generator, Validator, and Reviewer Agents
**Learning objectives covered:** 1 (versioned gates + deterministic engine)

## Before you start

| Need | Notes |
|---|---|
| `gates.yaml` v1.1.0 | Lab 18.1 |
| A run to evaluate | Your `runs/req-2481-run-02/` or the [offline kit](samples/offline-kit/README.md) fixture |
| Flawed draft | [`samples/gate-engine-draft.py`](samples/gate-engine-draft.py) — find the defects, do not copy it |
| Reference implementation | Guide §1 code listing — read it, then write your own with the check ids your registry needs |
| Also in scope | Add a machine-readable `04_api_validation.json` companion to the API Validator's report — gates read JSON; humans read Markdown |

---

## Steps

### Step 1 — Critique the draft engine (≥6 defects)

Run the draft if you like — the offline kit makes that safe. Then record each defect as
*defect → consequence → fix* in `notes/module18/engine-review.md`.

Hints on where to look (not the answers):

| Area | Ask yourself |
|---|---|
| Exit codes | If a check cannot run at all, what exit code does the orchestrator receive? What will it do with it? |
| Exception handling | When the *checker* breaks — missing config, unreadable file — who gets blamed? |
| Unknown checks | A typo'd check id in `gates.yaml`: error or silent skip? |
| Ordering | After the first FAIL, should the remaining checks still run? Which are cheapest? |
| Logging | Which verdicts reach the log? What happens to the verdicts that matter most? |
| Log completeness | Can an auditor see the `gates.yaml` version, the input hash, each check's result, and the duration? |
| Subprocesses | What happens if `pytest` hangs? |
| State agreement | `state.json` and `gates.yaml` disagree about the version — does anyone notice? |

### Step 2 — Build `tools/gate_engine.py`

Write the real engine (guide §1 is the reference; ~90 lines). It must satisfy:

| Property | Test it must pass |
|---|---|
| **Deterministic** | Same artifacts + same `gates.yaml` version → same verdict; no LLM calls in G1–G4; G5 only *reads* the reviewer's verdict |
| **Cheap-first** | Checks run in listed order (L1 structure → L2 static → L3 execution); evaluation stops at the first non-PASS |
| **Three-valued** | `PASS` (0) / `FAIL` (1, "the producer can fix it") / `NEEDS_HUMAN` (2, "no automated answer exists") |
| **Fail-safe** | Any exception, timeout, unknown check id, or unreadable file → `NEEDS_HUMAN`, logged with `error`; **never PASS** |

- [ ] Implement the check registry for the three boundaries this lab automates. Every check returns
      `(result, detail, findings)` where each finding has at least `criterion`, `observed`, `class`.

| Gate | Check ids | Ladder | FAIL finding class |
|---|---|---|---|
| **G3** | `envelope_valid`, `write_scope`, `control_files_untouched` | L1 | TEST_DEFECT · TEST_DEFECT · **NEEDS_HUMAN (tamper)** |
| | `tests_collect`, `lint_clean`, `markers_present`, `ac_coverage_complete`, `no_unjustified_skips`, `assertions_not_reduced` | L2 | TEST_DEFECT (last one: **ESCALATE — goal drift**) |
| **G4** | `report_parses` | L1 | NEEDS_HUMAN (validator broke) |
| | `no_test_defects`, `no_environment_failures` | L3 | TEST_DEFECT · NEEDS_HUMAN |
| **G5** | `verdict_known`, `reviewer_cites_original_acs`, `findings_have_owner` | L1 | NEEDS_HUMAN (review incomplete) |

- [ ] Two classifications deserve care: **tamper is not a FAIL** (retrying the agent that changed the
      rules is the wrong response), and **G5 never passes on its own** — APPROVE and ESCALATE both
      lead to the human checkpoint.
- [ ] Append one JSON object per evaluation to `runs/<run_id>/gate_log.jsonl` with at least:
      `ts`, `run_id`, `gate`, `gates_version`, `round`, `input_ref` (+hash), ordered `checks[]`,
      `decision`, `decided_by`, `duration_ms` — plus `findings[]` or `error` when applicable.
- [ ] Make the log write part of the fail-safe path: a logging failure is itself NEEDS_HUMAN.

### Step 3 — Prove three-valued, fail-safe

Run your engine against the fixture (or your own run) and capture the three exits:

```bash
# PASS — tests complete and conform
python3 tools/gate_engine.py --run req-2481-run-02 --gate G3_tests_collect_and_conform; echo "exit=$?"

# FAIL — round-0 tests have a missing marker
python3 tools/gate_engine.py --run req-2481-run-02 --gate G3_tests_collect_and_conform; echo "exit=$?"

# NEEDS_HUMAN — break the control plane, not the artifact
mv gates.yaml gates.yaml.bak
python3 tools/gate_engine.py --run req-2481-run-02 --gate G3_tests_collect_and_conform; echo "exit=$?"
mv gates.yaml.bak gates.yaml
```

- [ ] Exit codes are exactly 0 / 1 / 2 and **each run appended a log line** — including the two that
      were not PASS.
- [ ] Add a typo to one check id and confirm exit 2 with `error: unknown check '…'`; fix it.
- [ ] Simulate a tool that cannot run (e.g. `PATH` without `ruff`): the verdict is NEEDS_HUMAN, not
      FAIL — a missing checker is a control-plane problem.

### Step 4 — Inspect one log line like an auditor

- [ ] The last FAIL entry shows the ordered checks up to the first failure, the finding(s) with
      evidence, `gates_version: 1.1.0`, the `input_ref` hash, `decided_by: automated`, and a duration.
- [ ] Paste one PASS, one FAIL, and one NEEDS_HUMAN line into `notes/module18/engine-review.md`.

---

## Evidence

- `tools/gate_engine.py` with the G3/G4/G5 registry
- `runs/req-2481-run-02/gate_log.jsonl` containing a PASS, a FAIL (with findings), and a NEEDS_HUMAN
  (with `error`)
- `notes/module18/engine-review.md` — the draft's ≥6 defects and the three sample log lines
- API Validator prompt updated to emit `04_api_validation.json` (if you are on Path A)

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: yaml` | Wrong interpreter | Use the 3.11 env from the prerequisites |
| `pytest` not found from the engine | Engine's `PATH` differs from your shell | Use `python3 -m pytest` in the engine, or pass the interpreter path |
| `ruff` missing | Tool not installed | Either install it, or accept NEEDS_HUMAN — but decide **deliberately** and record the simplification in `PIPELINE.md` |
| Engine returns PASS when `gates.yaml` is gone | Fail-open bug | Check the exception path: `except` must set NEEDS_HUMAN and still write the log entry |
| G4 can't find `04_api_validation.json` | API Validator still writes Markdown only | Add the JSON companion to the agent prompt; gates read JSON, humans read Markdown |

## Checkpoint questions

<details>
<summary>Why is a checker exception NEEDS_HUMAN rather than FAIL?</summary>

An exception means the *checker* failed, not the artifact. FAIL would send the generator into a retry
it cannot fix and burn its counter. NEEDS_HUMAN halts and reports a control-plane problem — when the
checker fails, the answer is not PASS, and it is not "blame the agent" either.
</details>

<details>
<summary>Why stop at the first FAIL instead of collecting all findings?</summary>

Feedback stays focused and cheap: a broken structure makes later checks meaningless, and L3 execution
checks can be expensive. Fix the first layer, re-run, and let the next failure surface — the log keeps
the ordered prefix so an auditor sees exactly where evaluation stopped.
</details>

<details>
<summary>Why does G5 never return PASS on its own?</summary>

G5 reads the reviewer's *opinion* (APPROVE / REQUEST_CHANGES / ESCALATE) and validates its shape — it
cannot grant sign-off. APPROVE and ESCALATE both route to the human checkpoint; REQUEST_CHANGES is a
FAIL routed to the owner the reviewer names, and the engine validates that owner.
</details>

---

*Next: Lab 18.3 — Close the Correction Loop, where a FAIL becomes a schema-valid findings file, the owning agent patches, and four bounds decide RETRY vs ESCALATE.*

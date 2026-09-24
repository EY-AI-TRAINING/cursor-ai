# Lab 16.4 — Build the Test Generator: One Writer, Scoped to `tests/`

**Module 16 · Use Case Lab 3: Multi-Agent Requirement-to-Test Automation | Xebia — Cursor AI Training**
Day 5 · Lab 4 of 8 · ~25 minutes · Individual or pairs

> **Objective:** produce executable PyTest code from the locked sequence. The Generator is the **only
> stage with write access**, and only inside `tests/`. Every test carries `req` / `ac` / `seq` markers so
> results can be traced back to acceptance criteria. Collection failure is a quality failure — you send
> structured feedback back, count the round (max 2), and log it.

**Guide references:** Module 16, §3 (Test Generator — executable tests, scoped writes, markers)
**Learning objectives covered:** 3 — chain the Test Generator from the sequence; 6 — traceability carried into code.

---

## Before you start

- Lab 16.3 complete: `02_test_sequence.json` valid, coverage matrix clean
- Write your definition in `<pipeline-root>/.cursor/agents/test-generator.md`
- Sandbox running (Path B: `python3 sandbox/orders_api.py` in a separate terminal)
- Fresh chat, inputs: `02_test_sequence.json` + `specs/openapi.yaml` + `tests/conftest.py`

---

## Step 1 — Write the agent definition

- [ ] **Role** — turns the sequence into executable tests; never changes the sequence's intent
- [ ] **Inputs** — `02_test_sequence.json`, `specs/openapi.yaml`, `tests/conftest.py` (fixtures)
- [ ] **Tools** — write access scoped to `tests/` only; test runner; **no other writes** (not `src/`, not `specs/`, not `requirements/`)
- [ ] **Guardrails ("must NOT")**:
  - must not edit the sequence or invent scenarios
  - must not mark its own work as approved (separation of duties)
  - must not hard-code secrets or URLs — read from config/env
  - must not add fixtures anywhere except `tests/conftest.py`
- [ ] **Output** — `tests/test_req_2481_*.py` + `runs/<run_id>/03_generation_notes.md` + envelope
- [ ] **Conventions baked in** — one test per scenario (or `parametrize` for variants); `@pytest.mark.req/ac/seq` and docstrings naming SEQ-ID / AC-IDs; assert exactly the `expect` list, no more, no fewer

---

## Step 2 — Register the markers, then generate

```ini
# pytest.ini
[pytest]
markers =
    req(id): source requirement ID
    ac(id): acceptance criterion ID
    seq(id): test sequence scenario ID
```

- [ ] `pytest.ini` present in `<pipeline-root>/` with all three markers registered
- [ ] Test file(s) generated under `tests/`; every test names its SEQ-ID and AC-IDs in a docstring and markers
- [ ] `03_generation_notes.md` records scenario→test mapping and any assumptions
- [ ] `git status` shows writes **only** under `tests/` and `runs/req-2481-run-01/` — anything else is a scope violation

---

## Step 3 — Collection smoke check

```bash
pytest --collect-only tests/test_req_2481_*.py
```

- [ ] Collection succeeds (the file imports and every fixture resolves)
- [ ] `pytest --collect-only -q -m "ac('AC-1')"` (or equivalent) shows the intended test(s) for one AC
- [ ] One test per scenario (or a documented `parametrize` mapping); no test without a SEQ marker

---

## Step 4 — Correction round (only if collection failed)

A collection error is a **quality failure**. Route it back with structured feedback:

| Field | What to include |
|---|---|
| Error | The exact collection error (missing fixture, import error, syntax) |
| Location | File + line from the traceback |
| Expected | What the test should do instead (e.g., use `make_order`, add fixture to `conftest.py`) |

- [ ] Feedback is structured (error + location + expected), not "it fails, try again"
- [ ] Round counter is **1 of 2 max** — recorded; if round 2 also fails, escalate (`NEEDS_HUMAN`), do not loop
- [ ] Re-run in a fresh chat with the feedback; the fix addresses the cause, not the symptom
- [ ] Both generator attempts in `run_log.jsonl` (`FAIL`/`PASS` or attempt numbers)

---

## Evidence

- `.cursor/agents/test-generator.md` — five slots, scoped write, must-nots
- `tests/test_req_2481_*.py` — markers + docstrings, one test per scenario, fixtures reused
- `runs/req-2481-run-01/03_generation_notes.md`
- `pytest.ini` + `pytest --collect-only` output
- Correction-round record (if used): feedback, round number, re-run result
- `git status` output proving scoped writes
- `run_log.jsonl` — generator attempt line(s)

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Collection error: missing fixture | Generator used a fixture that does not exist | Add it to `tests/conftest.py` (with the fixture contract in context); this is correction round 1 |
| Test file also touched `conftest.py` logic outside fixtures | Scope creep | Fixtures belong in `conftest.py`; test-specific setup stays in the test |
| Assertions differ from the sequence `expect` list | Generator editorializing | Assert exactly the `expect` list — the Reviewer compares against the sequence and the original AC |
| Writes appear under `src/` or `specs/` | Write scope too broad | Discard the change, tighten the definition, re-run; one writer means one path |
| Test passes for the wrong reason (e.g., status 404 asserted for AC-3) | Assertion not tied to the AC | Fix now — the API Validator will also catch drift, but the cheap place is here |
| `PytestUnknownMarkWarning` | Markers not registered | `pytest.ini` with the three markers (Step 2) |

---

## Checkpoint questions

1. Why is the Test Generator the only stage with write access, and only to `tests/`?
2. What makes a retry a *correction* rather than a re-roll?
3. Why keep AC/SEQ IDs in both markers and docstrings?

<details>
<summary>Answers</summary>

1. Least privilege and separation of duties: one writer makes the path of every change clear, scopes the blast radius, and keeps upstream artifacts (sequence, spec, requirement) immutable — so review and traceability stay meaningful.
2. It carries new information — the structured feedback (error, location, expected) that makes the next attempt different. Retrying with the same inputs and reasoning produces the same result (Module 15 §4).
3. Markers are machine-readable, so results, coverage reports, and traceability tables can be generated by joining markers with the sequence and the JUnit results; docstrings are human-readable so a reviewer can see intent in the code. Both together keep the traceability spine intact.

</details>

---

## Next

**Lab 16.5 — Build the API Validator: Static, Dynamic, and the Defect That Stays.** The suite collects. Now a second Validator-archetype stage checks it against the interface contract and executes it — and it must resist the temptation to "fix" a test so the suite goes green.

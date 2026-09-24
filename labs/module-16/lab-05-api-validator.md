# Lab 16.5 — Build the API Validator: Static, Dynamic, and the Defect That Stays

**Module 16 · Use Case Lab 3: Multi-Agent Requirement-to-Test Automation | Xebia — Cursor AI Training**
Day 5 · Lab 5 of 8 · ~20 minutes · Individual or pairs

> **Objective:** check the generated suite against the interface contract **and** run it against the
> sandbox — then classify every failure as a test defect, a product defect, or an environment problem.
> A failing test is not automatically the Generator's fault. Product defects are reported and the test is
> **never** adjusted to make the suite green.

**Guide references:** Module 16, §4 (API Validator — static + dynamic, failure classification)
**Learning objectives covered:** 4 — chain the API Validator against the target API; 6 — failure results feed the traceability spine.

---

## Before you start

- Lab 16.4 complete: tests collect; `03_generation_notes.md` written
- Write your definition in `<pipeline-root>/.cursor/agents/api-validator.md`
- Sandbox running; fresh chat, inputs: `tests/test_req_2481_*.py` + `specs/openapi.yaml` (+ sandbox access)

---

## Step 1 — Write the agent definition

- [ ] **Role** — verifies the generated tests against the interface contract and the running API; classifies failures
- [ ] **Inputs** — the test file(s), `specs/openapi.yaml`, sandbox base URL
- [ ] **Tools** — read tests; run PyTest; the only write is `runs/<run_id>/04_api_validation_report.md`
- [ ] **Guardrails ("must NOT")**:
  - must not edit any test — findings go back to the Generator, tied to a file/test/AC-ID
  - must not classify a spec violation as a test defect
  - must not treat an environment failure (timeout/5xx/sandbox down) as a product defect
- [ ] **Output** — `04_api_validation_report.md` with a static conformance table, an execution section, and one classification per failure; envelope carries `status` + findings
- [ ] **Classification vocabulary** — `TEST_DEFECT` (test assumes wrong behaviour/field), `PRODUCT_DEFECT` (API violates its own spec/AC; test stays failing), `ENVIRONMENT` (retry once, then `NEEDS_HUMAN`)

---

## Step 2 — Static conformance

Check the tests against `specs/openapi.yaml` without running them:

| Test | Endpoint + method exists? | Asserted status codes declared? | Asserted fields in schema? | Request payload conforms? | Result |
|---|---|---|---|---|---|
| | | | | | |
| | | | | | |

- [ ] Every test row filled; mismatches cite the spec path (e.g., `openapi.yaml#/paths/~1orders~1{id}~1cancel/post/responses/403`)
- [ ] One sentence: what a static mismatch means for the Generator (test defect — fix the test)

---

## Step 3 — Dynamic execution

```bash
pytest -m "req('REQ-2481')" -v
```

- [ ] Record: collected · passed · failed (expected shape from the guide: 6 collected · 5 passed · 1 failed — your counts may differ)
- [ ] Every failure is classified; every classification cites evidence (spec path for product defects, code line for test defects)
- [ ] The expected AC-3 case (another customer's order): test asserts **403** per spec, API returns **404** → `PRODUCT_DEFECT` (guide example: `DEF-5520`), test **not modified**
- [ ] `git status` / `git diff` shows **no test edits** from this stage

---

## Step 4 — Write the report and flag the defect

- [ ] `04_api_validation_report.md` contains the static table, the execution results, and the classification block with `Action` lines (who is notified, what happens to the test)
- [ ] The product defect is flagged to the Reviewer **and** the requirement owner; the failing test stays in the suite (no `xfail` without a linked defect)
- [ ] If all tests passed: verify the AC-3 behaviour directly (`curl -s -X POST "$SANDBOX/orders/O1/cancel" -H 'X-Customer: cust-b'`, with `$SANDBOX` set to your base URL) — if the API returns 404 where the spec declares 403, the defect still exists; report it as a coverage/design gap plus the product defect
- [ ] `run_log.jsonl` — api-validator line with status and defect reference

---

## Evidence

- `.cursor/agents/api-validator.md` — five slots, classification vocabulary, must-nots
- `runs/req-2481-run-01/04_api_validation_report.md` — static table + execution + classifications
- Test-run output (terminal transcript or pasted summary)
- `git status` / `git diff` proving no test was modified
- `run_log.jsonl` — api-validator line

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Validator changed the assertion to 404 | "Making the suite green" | Forbidden: product defects are never fixed in tests. Revert, reclassify, and report; the test stays failing until the API is fixed |
| Product defect classified as test defect | Sympathy for the API | The spec is the contract of record; if the API contradicts it, the API is wrong |
| Sandbox down / connection errors | Environment | Retry once; if it persists, mark `ENVIRONMENT` and `NEEDS_HUMAN` — do not touch tests |
| Static table skipped, straight to execution | Shortcut | Static conformance is how you catch wrong fields/codes without a running API and keeps classifications evidence-based |
| Every failure labelled test defect | No spec citation | Walk each failure against `openapi.yaml`; the AC/spec decides, not the observed status code |
| Test skipped or xfail'ed to hide the failure | Failure dishonesty | Only allowed with a linked defect id (`DEF-…`) and a reason; otherwise it stays visible and failing |

---

## Checkpoint questions

1. A generated test fails because the API returns 404 instead of the spec's 403. Who should change what?
2. Why must the API Validator classify failures instead of simply reporting pass/fail counts?
3. What makes a failure an *environment* problem rather than a product or test defect?

<details>
<summary>Answers</summary>

1. Nobody changes the test. The API Validator classifies it as a **product defect**, the Reviewer escalates, and the product/requirement owner raises the defect against the API. The test stays and keeps failing until the API conforms to its contract.
2. Because the response to a failure differs completely by cause: test defects go back to the Generator, product defects go to the owner (and the test stays), environment problems are retried and escalated. Counts alone would send every failure to the same place — including real bugs into the Generator's queue.
3. It is independent of the code under test: the sandbox is unavailable, a call times out, or the service returns 5xx for infrastructure reasons. Retry once; if it persists, escalate as `NEEDS_HUMAN` rather than mislabelling it.

</details>

---

## Next

**Lab 16.6 — Build the Reviewer: Fresh Context, One Verdict.** One stage left to build. It sees the original requirement, the tests, and the report — never the generator's reasoning — and returns a single verdict that the human acts on.

# Lab 16.1 — Set the Contract: Layout, `PIPELINE.md` & the Handoff Rule

**Module 16 · Use Case Lab 3: Multi-Agent Requirement-to-Test Automation | Xebia — Cursor AI Training**
Day 5 · Lab 1 of 8 · ~10 minutes · Individual or pairs

> **Objective:** before any agent exists, fix the two contracts that make the pipeline reviewable — **what
> runs in what order** (`PIPELINE.md`) and **how stages talk** (`.cursor/rules/pipeline-handoff.mdc`) — lay
> out the workspace, create the first run folder, and verify the inputs and the sandbox are reachable.
> Every later lab produces evidence against this contract.

**Guide references:** Module 16, §0 (orchestration instructions and the shared handoff rule)
**Learning objectives covered:** setup for 1–7 — the stage definitions and handoffs all run on this contract.

---

## Before you start

- Module 15 complete on `module15-lab`: your `orchestration/handoff-envelope.md`, `budget-card.yaml`, and `runtime-plan.md` are the starting material (the guide's §0 values are the defaults if yours differ)
- Branch: `git switch -c module16-lab` from `module15-lab`
- Create the pipeline workspace from the guide's §0 layout — `<pipeline-root>/` is `requirement-to-test/` in your sandbox repo, **opened in Cursor as its own folder** so the `.cursor/` config below is active
- Choose the sandbox path:
  - **Path A** — your facilitator's sandbox API and `specs/openapi.yaml` are provided
  - **Path B** — copy the offline kit: follow [`samples/offline-kit/README.md`](samples/offline-kit/README.md)
- Inputs to have in place (copy from this pack if Path B):
  - [`samples/REQ-2481.md`](samples/REQ-2481.md) → `requirements/REQ-2481.md`
  - [`samples/openapi-excerpt.yaml`](samples/openapi-excerpt.yaml) → `specs/openapi.yaml`
  - `tests/conftest.py` fixture contract (Path A provides it; Path B copies it)

---

## Step 1 — Lay out the workspace

```text
requirement-to-test/
├── .cursor/
│   ├── rules/
│   │   └── pipeline-handoff.mdc
│   └── agents/            # five agent definitions land here, one per lab
├── requirements/
│   └── REQ-2481.md
├── specs/
│   └── openapi.yaml
├── tests/
│   └── conftest.py
├── runs/
│   └── req-2481-run-01/
└── PIPELINE.md
```

- [ ] Directories created; `pytest --version` runs
- [ ] `requirements/REQ-2481.md` and `specs/openapi.yaml` present and unmodified from the fixture (AC-4 is *supposed* to be vague — do not fix it)

---

## Step 2 — Write `PIPELINE.md`

Adapt the guide's §0 template to your Module 15 budget card. It must contain:

- [ ] The **run ID format** (`<req-id>-run-<nn>`) and the rule that every artifact goes to `runs/<run_id>/`
- [ ] The **stage table**: for each of the five stages — reads, writes, timeout, retries. The reads column is the handoff contract: a stage reads the previous stage's artifact, never the chat history

| # | Stage | Reads | Writes | Timeout | Retries |
|---|---|---|---|---|---|
| 1 | requirement-validator | | | | |
| 2 | sequence-builder | | | | |
| 3 | test-generator | | | | |
| 4 | api-validator | | | | |
| 5 | reviewer | | | | |

- [ ] The **stop rules**, explicit: stage 1 `FAIL` → stop and return gaps to the owner; any `NEEDS_HUMAN` → stop and ask; max 2 manual correction rounds back to stage 3, then escalate
- [ ] The **run budgets** (from your Module 15 card): wall-clock and tokens; exceeded → halt (fail-safe)
- [ ] One sentence: who is the orchestrator in this lab, and what the stop rules protect against

---

## Step 3 — Write the handoff rule

Create `.cursor/rules/pipeline-handoff.mdc` — standing behaviour, not a prompt to restate (Module 8):

```markdown
---
description: Handoff contract for all requirement-to-test pipeline agents
globs: runs/**, tests/**
alwaysApply: false
---
- End every stage with a JSON handoff envelope: run_id, stage, stage_version, status (PASS|FAIL|NEEDS_HUMAN),
  input_refs, artifact_refs, ac_ids_covered, evidence, assumptions, open_issues, attempt.
- Every claim about the API must cite specs/openapi.yaml#<path>. No unsupported facts (Module 13).
- Carry AC-IDs forward unchanged. Never renumber, merge, or drop an AC-ID silently.
- Never approve your own output. Only the reviewer stage may emit a sign-off verdict.
- Append one line per stage to runs/<run_id>/run_log.jsonl (Module 14 §5 fields).
```

- [ ] Rule file created with the envelope fields (including `ac_ids_covered`), the spec-citation requirement, the AC-ID rule, the no-self-approval rule, and the run-log rule
- [ ] One sentence: why this lives in a **rule** rather than being repeated in each agent's prompt

---

## Step 4 — Create the run folder

```bash
mkdir -p runs/req-2481-run-01
touch runs/req-2481-run-01/run_log.jsonl
```

- [ ] Run folder `runs/req-2481-run-01/` created; empty `run_log.jsonl` present
- [ ] One sentence: why every run gets its own folder instead of overwriting artifacts

---

## Step 5 — Verify inputs and smoke-check the sandbox

Path B (offline kit):

```bash
python3 sandbox/orders_api.py          # terminal 1 — keep running
curl -s http://127.0.0.1:8000/health
curl -s http://127.0.0.1:8000/orders/O1 -H 'X-Customer: cust-a'
```

Path A: run the equivalent checks against your sandbox URL.

- [ ] `/health` (or equivalent) responds
- [ ] One order fetch returns `200` with `id`, `owner`, `status`, `amount`
- [ ] You know how to reset the sandbox between reruns (Path B: `POST /_test/reset`)
- [ ] Record the sandbox base URL in `PIPELINE.md` (or a `.env`-style note — no secrets)

---

## Evidence

- `PIPELINE.md` — run ID format, five-row stage table, stop rules, budgets
- `.cursor/rules/pipeline-handoff.mdc` — the standing envelope rule
- `runs/req-2481-run-01/` — the empty run folder and `run_log.jsonl`
- Sandbox smoke-check output (health + one order fetch)

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `PIPELINE.md` reads like prose | Skipped the table | Reads/writes/timeouts/retries per stage; it is a contract, not a description |
| Handoff rule repeated inside every agent prompt | Wrong layer | The rule is standing (globs `runs/**, tests/**`); agents do not restate it |
| AC-4 "fixed" before the Validator runs | Helpfulness | AC-4 stays vague until the owner answers in Lab 16.2 — the pipeline exists to catch it |
| Sandbox unreachable | Server not running / wrong port | Start it in a separate terminal; export `ORDERS_API_URL` if you moved the port |
| `.cursor/rules` not loading | Cursor opened at the wrong folder | Open `<pipeline-root>/` as the workspace so its `.cursor/` is the active config |
| Run folder reused for a second run | "It's the same requirement" | New run → new folder (`…-run-02`); earlier evidence must survive (Module 14) |

---

## Checkpoint questions

1. Why are `PIPELINE.md` and the handoff rule written *before* the first agent definition?
2. Why does each stage read files rather than the conversation that produced them?
3. What do the stop rules guarantee that a "helpful" orchestrator would not?

<details>
<summary>Answers</summary>

1. They are the pipeline's interface contracts. Agents are written against them, the reviewer audits against them, and Modules 17–18 automate gates on the same `status` fields — changing them later invalidates every artifact and run.
2. Files are reproducible, versioned, and auditable; chat history is not. File-only handoffs also enforce context isolation, so a downstream stage cannot silently inherit an upstream agent's assumptions (Module 15 §3).
3. That a deterministic failure or an open question stops the run instead of being papered over — the difference between a pipeline that reports gaps honestly and one that ships invented answers (the exact failure mode the flawed-run fixture shows).

</details>

---

## Next

**Lab 16.2 — Build the Requirement Validator: Fail Cheaply on the Vague AC.** The contract is set; the first stage exists to reject bad input before any generation tokens are spent. You'll build it, watch it catch AC-4, and answer the clarification as the requirement owner.

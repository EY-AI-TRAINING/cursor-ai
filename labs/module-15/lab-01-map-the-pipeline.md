# Lab 15.1 — Map the Pipeline: Topology, Handoffs & Roles

**Module 15 · Subagents & Orchestration Patterns Overview | Xebia — Cursor AI Training**
Day 5 · Lab 1 of 3 · ~12 minutes · Individual or pairs

> **Objective:** do the module's hands-on — annotate the sample pipeline using Module 15's vocabulary. Mark the
> sequential spine and price the fan-out candidate; define the typed handoff envelope and the artifact that
> moves on every arrow; repair five defective envelopes from a real run; rebuild the role/privilege table and
> flag where the cards drift from the four archetypes; and explain the reviewer's direct-to-original-AC line.
> **No building in this lab** — Module 16 constructs the pipeline.

**Guide references:** Module 15, §1 (topology, state, handoff contracts), §2 (role archetypes), §3 (delegation and independent context), §7 walkthrough tasks 1–4
**Learning objectives covered:** 1 — sequential vs. parallel; 2 — state and handoff contract; 3 — role assignment; 4 — delegation and independent-context review.

---

## Before you start

- Module 14 complete: `governance/handoff-log-schema.md` and the trace-id discipline exist on your branch
- Create `shared-agent-library/orchestration/` — Module 15's artifact home
- Open these read-only fixtures:
  - [`samples/sample-pipeline.md`](samples/sample-pipeline.md) — the five-stage design and its cards
  - [`samples/handoff-envelopes.md`](samples/handoff-envelopes.md) — five raw handoffs from `req-2481-run-09`
- Create your working files: `orchestration/pipeline-map.md` and `orchestration/handoff-envelope.md`
- No runner needed — this is annotation and design

---

## Step 1 — Topology: mark the spine, price the fan-out

- [ ] Mark the **sequential spine** (Validator → Builder → Generator → API Validator → Reviewer) and state, for at least one stage, exactly what it consumes from the previous stage that it could not produce itself
- [ ] Write one sentence on the latency the chain adds and why sequential is still the right default here
- [ ] **Fan-out candidate:** the three operations behind REQ-2481 and the independent scenarios are separable, so test generation could fan out per operation or scenario. Fill the price table before deciding:

| Cost of fan-out | Your entry |
|---|---|
| Merge step — who merges, and what does the merge produce? | |
| Shared-write / conflict risk (run-09 used one `tests/conftest.py`) | |
| Extra contexts to observe (traces, logs, cost attribution) | |
| Token cost (roughly the same or higher — say why) | |
| Verdict: apply in Module 16, or defer? Why | |

- [ ] Mark the two return arrows (API Validator → Test Generator, Reviewer → Test Generator) as **correction loops**; note which card states a round limit and what the other loop has instead
- [ ] One sentence: what happens to an early error when no gate stops it, and which Module 14 artifact would show it later

---

## Step 2 — Define the handoff contract

In `orchestration/handoff-envelope.md`, write the envelope every handoff must use (guide §1):

```jsonc
{
  "pipeline_run_id": "<one id for the whole run>",
  "stage": "<which stage produced this handoff>",
  "stage_version": "<version of the stage/agent definition>",
  "status": "PASS",                       // PASS | FAIL | NEEDS_HUMAN
  "input_ref": "<file + version/hash the stage consumed>",
  "output": { "artifact_ref": "<file produced>", "summary": "<one line>" },
  "evidence": ["<grounding citations from Module 13>"],
  "assumptions": ["<what was not verified>"],
  "open_issues": ["<what the next stage or human must handle>"],
  "attempt": 1,
  "metrics": { "tokens_in": 0, "tokens_out": 0, "tool_calls": 0, "duration_s": 0 }
}
```

- [ ] Every field present; `status` is the enum, not prose
- [ ] Fields defined briefly: which let the orchestrator **route** without re-reading output? Which make the step **reproducible**? Which carry **grounding**? Which feed **retries** and **cost**?
- [ ] Fill the per-arrow table — for each arrow, the artifact that moves and the fields it must carry beyond the schema:

| Arrow | Artifact that moves | Envelope fields that matter most here |
|---|---|---|
| REQ-2481 → Requirement Validator | | |
| Validator → owner (FAIL path) | | |
| Validator → Sequence Builder | `01_validated_requirement.md` | |
| Sequence Builder → Test Generator | | |
| Test Generator → API Validator | | |
| API Validator → Test Generator (FAIL) | | |
| API Validator → Reviewer | | |
| REQ-2481 original AC → Reviewer (direct) | | |
| Reviewer → Test Generator (findings) | | |
| Reviewer → human sign-off | | |

- [ ] One sentence relating this to Module 14's `governance/handoff-log-schema.md`: the envelope is the **payload the next stage consumes**; the log entry is the **durable record** — the same `pipeline_run_id` threads both

---

## Step 3 — Repair the five envelopes

For each raw envelope in the fixture, name what is missing or wrong and rewrite it against your schema in `handoff-envelope.md`:

| Envelope | Missing / wrong | Why it matters | Repaired |
|---|---|---|---|
| 1 — Requirement Validator | | | |
| 2 — Sequence Builder | | | |
| 3 — Test Generator | | | |
| 4 — API Validator | | | |
| 5 — Reviewer | | | |

- [ ] Envelope 1 becomes a typed envelope with an id, a status, and refs — free text is not a handoff
- [ ] Envelope 2 gains `input_ref`, `evidence`, `assumptions`, `open_issues`, and `metrics`
- [ ] Envelope 3 gains the run id and a real status (`DONE` is not in the enum), loses the self-graded field, and gets an `input_ref`
- [ ] Envelope 4's FAIL carries **specific findings** (artifact, location, expected vs. actual) — otherwise the retry carries no new information
- [ ] Envelope 5's input list is corrected: artifact + **original acceptance criteria**, generator summary removed — one sentence why

---

## Step 4 — Rebuild the role and privilege table

For each stage, write the corrected row in `pipeline-map.md` — one archetype, least-privilege tools, an explicit "must not":

| Stage | Archetype | Role (one sentence, no "and") | Tools (least privilege) | Must not (explicit) |
|---|---|---|---|---|
| Requirement Validator | | | | |
| Sequence Builder | | | | |
| Test Generator | | | | |
| API Validator | | | | |
| Reviewer | | | | |
| Orchestrator | | | | |

- [ ] Compare with the fixture's cards and flag **every drift** (expect at least four) with the concrete failure it would cause. Known suspects to check:
  - Does any read-only role write, fix, or invent?
  - Does any stage rewrite an **upstream** artifact — and what does that do to traceability?
  - Does any validator edit the artifact it is validating? Who approves whose output then?
  - Does the generator's write scope stay inside its declared path?
- [ ] One sentence: why "no agent approves its own output" is a **separation-of-duties** rule, not politeness
- [ ] One sentence: the difference between a stage's `status` (did this stage's output pass its own contract check?) and a reviewer's **verdict** (does the artifact meet the original criteria?)

---

## Step 5 — Independent context for the Reviewer

- [ ] Two sentences: why the Reviewer receives the **original acceptance criteria directly** (the dotted line in the diagram) instead of the Builder's sequence or the generator's summary
- [ ] List at least three things the Reviewer must **not** receive (generator's reasoning/summary, upstream interpretation of the AC, chat history, other stages' internal notes)
- [ ] Diagnose Envelope 5: state why its PASS is **invalid** — both the anchoring input and the missing source of truth
- [ ] One sentence: what isolation costs (a subagent can't use what you didn't pass it) and the countermeasure that makes the loss visible

---

## Evidence

- `orchestration/pipeline-map.md` — topology annotation + fan-out price table + corrected role/privilege table + independent-context section
- `orchestration/handoff-envelope.md` — schema + per-arrow table + five repaired envelopes + envelope-vs-log note

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Everything labeled "parallel would be faster" | Merge cost ignored | Name the merge step, the conflict risk, and the extra contexts before deciding |
| Envelope treated as a log entry | Two records conflated | Envelope = payload the next stage consumes; log entry = durable record. Same run id, different jobs |
| Reviewer given "full context" to be safe | Anchoring risk missed | Artifact + original criteria only; extra context biases the verdict, it doesn't improve it |
| Status values drift to `DONE`, `OK`, `FAILED` | No enum pinned | `PASS` / `FAIL` / `NEEDS_HUMAN` — anything else cannot be routed on |
| Role drift found but no consequence stated | Detection without diagnosis | Say which failure becomes possible: invented requirements, untraceable edits, self-approval, out-of-scope writes |
| Envelope 4's retry fixes nothing | Findings lacked locations | A quality retry must carry the reviewer's specific findings, otherwise it is a re-roll |

---

## Checkpoint questions

1. Why is sequential the default, and what exactly must be true before fan-out pays off?
2. Why must a handoff be a typed envelope rather than a free-text reply?
3. Why does the Reviewer get the original acceptance criteria rather than the Builder's sequence?

<details>
<summary>Answers</summary>

1. Sequential is the default because most stages genuinely depend on the previous stage's output, and each handoff has a cost. Fan-out pays only when subtasks are **truly independent** (no shared writes, no ordering) and the wall-clock gain outweighs the merge step, conflict risk, and extra contexts — it saves time, not tokens.
2. An envelope can be **routed on** (`status`), **reproduced** (`input_ref`/`artifact_ref`), **audited** (`evidence`, `metrics`), and **retried safely** (`attempt`). Free text must be re-interpreted by the next agent, which loses information and hides assumptions.
3. So an error introduced by an intermediate stage cannot spread unnoticed: the reviewer judges the artifact against the **source of truth**, not against upstream interpretation. Passing the generator's reasoning would also cause **anchoring** — a reviewer that reads the justification tends to agree with it.

</details>

---

## Next

**Lab 15.2 — Bound It: Failure Policy & the Budget Card.** The contract is defined; now the pipeline has to survive bad input, hung stages, quality failures, and budget breaches. You'll classify failures per stage, diagnose run-09, and write the policy and budget card that Module 16 will run under.

# Lab 16.3 — Build the Sequence Builder: Coverage Before Code

**Module 16 · Use Case Lab 3: Multi-Agent Requirement-to-Test Automation | Xebia — Cursor AI Training**
Day 5 · Lab 3 of 8 · ~20 minutes · Individual or pairs

> **Objective:** turn validated ACs into an ordered, implementation-free test sequence: setup, action,
> expected result per scenario, each mapped to an AC-ID. Then run the pipeline's **first chained
> handoff** — stage 2 consuming only stage 1's artifact, with no chat history — and prove the coverage
> matrix has no gaps and no orphans before a single line of test code exists.

**Guide references:** Module 16, §2 (Sequence Builder — deriving a test sequence)
**Learning objectives covered:** 2 — chain the Sequence Builder from the validated requirement; 6 — requirement → AC → scenario traceability.

---

## Before you start

- Lab 16.2 complete: `01_validated_requirement.md` at `status: PASS`, both validator attempts logged
- Write your definition in `<pipeline-root>/.cursor/agents/sequence-builder.md`
- Run in a fresh chat with **the artifact, not the conversation**: `01_validated_requirement.md` + `specs/openapi.yaml`

---

## Step 1 — Write the agent definition

- [ ] **Role** — derives an ordered test sequence from a **validated** requirement; designs scenarios, writes no code
- [ ] **Inputs** — `runs/<run_id>/01_validated_requirement.md` (must be `PASS`) and `specs/openapi.yaml`
- [ ] **Tools** — read-only; writes only `runs/<run_id>/02_test_sequence.json`
- [ ] **Guardrails ("must NOT")**:
  - must not read the original `requirements/REQ-2481.md` directly — work only from the validated artifact
  - must not add scenarios with no AC-ID; list suspected gaps under `open_issues` instead
  - must not name frameworks, libraries, or code
- [ ] **Output** — `02_test_sequence.json` with `req_id` + `scenarios[]`, each carrying `id`, `ac_ids`, `title`, `setup`, `action`, `expect`, `evidence` (spec citation), plus the handoff envelope

---

## Step 2 — Run it and check the artifact

```bash
python3 -m json.tool runs/req-2481-run-01/02_test_sequence.json > /dev/null   # valid JSON?
```

- [ ] JSON parses; every scenario has all seven fields; every `expect` is something the API actually returns with a spec citation
- [ ] Setup uses **named fixtures** (`customer_a`, `paid_order`, …), not literal magic values
- [ ] Error ACs (AC-2, AC-3) carry **negative assertions** including the unchanged state where applicable
- [ ] No framework or code names appear anywhere in the sequence

---

## Step 3 — Prove coverage: every AC, no orphans

Fill the matrix from your artifact (rows = ACs, columns = scenarios):

```text
          SEQ-1   SEQ-2   SEQ-3   SEQ-4   SEQ-5
  AC-1      ●                       ●       ●
  AC-2              ●
  AC-3                      ●
  AC-4                              ●
```

- [ ] Every AC row has at least one ● — an empty row is a **coverage gap** and the sequence is not ready
- [ ] Every scenario column has at least one AC — a column with none is an **untraceable scenario** (scope creep); it belongs in `open_issues`, not the sequence
- [ ] AC-4's scenario asserts exactly what the owner clarified in Lab 16.2 (refund record via `GET /refunds?order_id`)
- [ ] One sentence: why AC-1 needs more than one scenario (PAID and PENDING are different state paths)

---

## Step 4 — First chained handoff (Part A checkpoint)

Prove the handoff is file-only and sufficient: open a **fresh chat**, give the agent nothing but the two input files, and run it again.

- [ ] Stage 2 produced a valid sequence using only `01_validated_requirement.md` + `specs/openapi.yaml` — no chat history, no original requirement
- [ ] If it needed something that was not in the artifact, that is a **handoff gap**: record it in the run notes, fix the upstream artifact or envelope (with a bounded re-run, ≤2 rounds), and re-check
- [ ] `run_log.jsonl` has the sequence-builder attempt line(s)
- [ ] **Part A checkpoint:** artifacts 01 and 02 both exist with `status: PASS`, and the log shows the validator's two attempts plus the builder's

---

## Evidence

- `.cursor/agents/sequence-builder.md` — five slots, must-nots, output schema
- `runs/req-2481-run-01/02_test_sequence.json` — valid JSON, all fields, spec citations, envelope
- Coverage matrix (in the run notes or artifact) with no gaps and no orphans
- Chained-run note: what came only from files, and any gap found + fix
- `run_log.jsonl` — sequence-builder line

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Scenarios name PyTest or test functions | Builder drifting into code | Guardrail: design only; code names belong to the Generator |
| Scenario with no AC-ID ("verify audit") | Scope creep | Drop it from the sequence; if you believe it matters, raise it in `open_issues` |
| Coverage matrix has an empty AC row | Missed scenario | Add the missing scenario upstream in the Builder — not silently in the Generator |
| Sequence works only with your chat open | Handoff relies on history | Re-run in a fresh chat with files only; missing context is a defect to fix in the artifact |
| Duplicate scenarios for the same AC/state | Ambiguity in AC wording | Tighten titles/setup; distinct state paths are fine, duplicates are cost |
| Builder questions an AC's classification | Upstream disagreement | Route it back to stage 1 (Validator) — the Builder never edits the validated requirement |

---

## Checkpoint questions

1. Why does the Sequence Builder read the *validated* requirement instead of the original?
2. What is the difference between a coverage gap and an untraceable scenario?
3. Why does a file-only handoff make the pipeline *more* debuggable than passing full chat context?

<details>
<summary>Answers</summary>

1. The validated artifact is the checked, clarified version of the requirement — the Builder works from resolved facts, not raw ambiguity. It also isolates stages: the Builder cannot reinterpret ACs that the owner has already clarified.
2. A coverage gap is an AC with no scenario (the suite misses a requirement). An untraceable scenario is a test design with no AC (the suite tests something nobody asked for). Both are traceability defects, and both are cheaper to fix here than in code.
3. Each stage has a reproducible input and a named output. A failure can be re-run from the artifact alone, and a Reviewer can judge without inheriting upstream assumptions — nothing depends on a conversation that cannot be audited or replayed (Module 15 §1, §3).

</details>

---

## Next

**Break, then Part B: Lab 16.4 — Build the Test Generator: One Writer, Scoped to `tests/`.** The sequence is locked. From here, exactly one stage is allowed to write code, and only inside `tests/` — with markers that keep the traceability spine intact.

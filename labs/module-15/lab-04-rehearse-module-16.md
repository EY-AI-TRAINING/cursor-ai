# Lab 15.4 (Optional) — Rehearse Module 16 on Your Own Library

**Module 15 · Subagents & Orchestration Patterns Overview | Xebia — Cursor AI Training**
Day 5 · Optional extension · ~10 minutes · Individual + peer review

> **Objective:** rehearse the Module 16 build on your own assets. Map the five-stage Requirement-to-Test
> pipeline onto the agents you already own (Module 11's library, Module 13's grounded agent), write one real
> handoff envelope, pin the reviewer's original-AC input, carry your budgets forward, and make two granularity
> calls plus one boundary call for your own workflow. **This is a draft rehearsal, not Module 16's build.**

**Guide references:** Module 15, §1–§7 applied to your library
**Learning objectives covered:** 1–7 in rehearsal — the design decisions Module 16 will execute.

---

## Before you start

- Labs 15.1–15.3 complete: `pipeline-map.md`, `handoff-envelope.md`, `failure-policy.md`, `budget-card.yaml`, `runtime-plan.md` written
- Your Module 11 library at tag `v0.1.0`/`v0.2.x` and, if completed, your Module 13 `knowledge-grounded` agent
- Open a new file: `orchestration/module16-pipeline-draft.md`
- Optional: line up `<reviewer>` — a peer who challenges your stage map and your two granularity calls

---

## Step 1 — Stage map: your assets against the five stages

| Pipeline stage | Your asset (name + version) | Fit / gap | Plan for Module 16 |
|---|---|---|---|
| Requirement Validator | | | |
| Sequence Builder | | | |
| Test Generator | | | |
| API Validator | | | |
| Reviewer | | | |

- [ ] Every stage either maps to an existing asset or is marked **gap** with what you will do (build it, or run the stage inline for now)
- [ ] At least one asset carries its **grounding contract** from Module 13 into its new pipeline seat (which sources, citation format)
- [ ] One sentence: which stage is your weakest link, and why

---

## Step 2 — Write one real envelope

Take the first handoff (Requirement Validator → Sequence Builder) and fill a real envelope with **your** file names, versions, and evidence:

```jsonc
{
  "pipeline_run_id": "<your run id scheme>",
  "stage": "<your asset name>",
  "stage_version": "<asset version>",
  "status": "PASS",
  "input_ref": "<your requirement file + version>",
  "output": { "artifact_ref": "<your validated requirement file>", "summary": "..." },
  "evidence": ["..."],
  "assumptions": ["..."],
  "open_issues": [],
  "attempt": 1,
  "metrics": { "tokens_in": 0, "tokens_out": 0, "tool_calls": 0, "duration_s": 0 }
}
```

- [ ] Every field filled with a real path/version — no placeholders left
- [ ] `assumptions` names at least one thing the stage did **not** verify
- [ ] One sentence: how your `pipeline_run_id` scheme stays unique across reruns

---

## Step 3 — Pin the reviewer's input contract

- [ ] Name the **original acceptance criteria path + version** your Reviewer will receive directly (from your Module 9 spec)
- [ ] List what your Reviewer must not receive (generator's reasoning, upstream interpretation, chat history)
- [ ] One sentence: how you will prove, in Module 16's test run, that the reviewer actually got the original criteria — not the Builder's paraphrase

---

## Step 4 — Carry the budgets forward

- [ ] Copy `orchestration/budget-card.yaml` into your draft with any values adjusted for your stack (and comment why)
- [ ] Add one line: the first budget you expect to breach, and the signal that will tell you
- [ ] One sentence: who gets escalated to when `halt_and_escalate` fires in your team

---

## Step 5 — Two granularity calls and one boundary call

- [ ] **Accept** one delegation for your workflow: what gets isolated, what structured result comes back, and why the handoff earns its cost
- [ ] **Reject** one candidate (or merge): the specific reason from the §5 decision tree, and where the work lives instead
- [ ] **Boundary:** one thing that stays interactive in Module 16, and one thing you would move to CI in Module 19 — with the trigger that separates them
- [ ] One sentence: what you will explicitly **not** automate in the capstone, and why (this is Module 21's "when not to use an agent")

---

## Evidence

- `orchestration/module16-pipeline-draft.md` — stage map, one filled envelope, reviewer input contract, carried budgets with adjustments, two granularity calls + one boundary call, peer challenge notes
- Peer check: your `<reviewer>` finds one gap in the stage map or one unjustified budget number

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Stage map is all gaps | Comparing the sample's *names* to your library | Map by **function**, not name: your requirement-analysis agent is a Validator; your test-generation agent is a Generator |
| No Sequence Builder exists in your library | Module 11 built four job roles, not five pipeline seats | Either draft one, or state that the Builder's work runs inline in Module 16 and why that is acceptable for a first run |
| Envelope full of placeholders | Rehearsal treated as form-filling | Use real paths and real versions — if an artifact doesn't exist yet, name the gap in `open_issues` |
| Budgets copied unchanged | Skipped the cost reasoning | Adjust for your test suite's runtime and your context sizes, or state in a comment why the default holds |
| Ready to build it now | Enthusiasm (fair) | Module 16 is the build; keep this a draft and bring it to the session |

---

## Checkpoint questions

1. Why map assets by function rather than by name when assembling the pipeline?
2. Why does the reviewer's input contract need a proof step in Module 16's run, not just a design statement?
3. What does your "do not automate" line protect you from in the capstone?

<details>
<summary>Answers</summary>

1. Names drift between modules; functions don't. A library asset named "requirement-analysis" is a Validator, and "test-generation" is a Generator — the pipeline needs the *role*, and the envelope contract is what makes the swap safe.
2. A design can say "original AC direct" while the run passes a generator summary (exactly what run-09 did). The proof step — a transcript or an envelope `input_ref` pointing at the spec version — is what distinguishes a control from a wish.
3. It prevents an LLM from owning a deterministic or high-blast-radius step where a judgement error is expensive and unnecessary — and keeps the token/quality trade-off honest when the capstone is under time pressure.

</details>

---

## Next

**Module 16 — Use Case Lab 3: Multi-Agent Requirement-to-Test Automation.** Bring this draft, the envelope contract, the failure policy, the budget card, and the boundary plan. In Module 16 the five stages run for real, and your design decisions become the pipeline's configuration.

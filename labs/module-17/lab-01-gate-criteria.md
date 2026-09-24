# Lab 17.1 — Make the Gate Say What It Means: Criteria, Ladder & Three Values

**Module 17 · Quality Gates, Hooks & Self-Correction Fundamentals | Xebia — Cursor AI Training**
Day 5 · Lab 1 of 3 · ~6 minutes · Individual or pairs

> **Objective:** turn a draft gate config into `gates.yaml` v1.0.0 whose criteria are **objective,
> observable, actionable, cheap-first, and versioned**. Sort the G3 checks onto the L1–L4 ladder, prove
> none of them needs an LLM, and give every gate three-valued outcomes so "cannot decide" never silently
> becomes PASS.

**Guide references:** Module 17, §1 (PASS/FAIL criteria, the check ladder, three-valued outcomes), §7 walkthrough task 1
**Learning objectives covered:** 1 — automated PASS/FAIL criteria that are objective, observable, and logged.

---

## Before you start

- Module 16 complete on `module16-lab`: `<pipeline-root>/` has `PIPELINE.md` and `runs/req-2481-run-01/`
- Open [`samples/gates-draft.yaml`](samples/gates-draft.yaml) (read-only)
- Create `notes/module17/gate-design.md`; write `gates.yaml` at `<pipeline-root>/gates.yaml`
- No runner needed — this is criteria design

---

## Step 1 — Review the draft against the five properties

Every gate criterion must be objective, observable, actionable on FAIL, cheap-first, and versioned (§1). Find **at least six** problems in the draft and correct them:

| # | Problem in the draft | Why it fails | Corrected wording |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |
| 6 | | | |

Suspects to check, gate by gate:

- [ ] A **subjective** check anywhere ("looks…", "seems…", "well", "realistic")
- [ ] A **route that retries a deterministic input problem** (what should happen instead — §1's three outcomes?)
- [ ] A **round limit that is missing, meaningless, or too loose** for the gate it protects
- [ ] Checks that are **not observable from the artifact** (trusting an agent's claim)
- [ ] **LLM judgement used before deterministic checks** — and whether it may overrule them
- [ ] A product defect treated as a producer failure, or an environment failure treated as a pass
- [ ] The missing **version** and the missing human step

---

## Step 2 — Write `gates.yaml` v1.0.0

Adapt the guide's §1 criteria into your pipeline's real paths and commands:

- [ ] `version:` at the top; every gate has `checks:`, `on_fail:`, and a round bound where a producer retries
- [ ] **G1** checks only observable facts (envelope `status`, all AC classifications TESTABLE, no open clarification questions) and routes to a human on FAIL — **no retry**
- [ ] **G2** checks the sequence against a schema, set-equality of AC-IDs against `01_*`, and "no scenario without `ac_ids`"; `max_rounds: 1`
- [ ] **G3** checks collection (`pytest --collect-only`, exit 0), lint, marker presence (`@pytest.mark.ac`/`seq`), and that changed paths stay inside `tests/**` + `runs/**`; `max_rounds: 2`
- [ ] **G4** fails on any `TEST_DEFECT` or `ENVIRONMENT` failure but **allows flagged `PRODUCT_DEFECT`** through to the reviewer; shares the `max_rounds: 2` counter with G3
- [ ] **G5** accepts `APPROVE` and `ESCALATE`, routes `REQUEST_CHANGES` back to the producer, and has a `then: hitl_commit_approval` step
- [ ] Every `on_fail` message is **actionable**: it names the failing check and what to fix

---

## Step 3 — Sort G3 onto the ladder and keep the LLM in its place

| G3 check | Ladder level (L1–L4) | Why it belongs there |
|---|---|---|
| envelope present / files exist | | |
| `pytest --collect-only` exit 0 | | |
| lint passes | | |
| every test has `@mark.ac` / `@mark.seq` | | |
| changed paths ⊆ `tests/**`, `runs/**` | | |

- [ ] Each check classified; the ordering is cheapest/most deterministic first
- [ ] One sentence: why **none** of G3's required checks needs an LLM
- [ ] One sentence: where an LLM judge *is* appropriate (L4, fresh context, written rubric) and why it may never overrule a failing L1–L3 check

---

## Step 4 — Define the three-valued outcome

| Outcome | Meaning | Routing in your pipeline |
|---|---|---|
| **PASS** | | |
| **FAIL** | | |
| **NEEDS_HUMAN** | | |

- [ ] All three defined; NEEDS_HUMAN is used where the gate genuinely cannot decide (ambiguous input, validator error, policy question)
- [ ] One sentence: why two values are not enough — what bad shortcut does it force?
- [ ] One sentence: what the gate records when **it cannot produce a verdict at all** (preview of Lab 17.3's fail-safe drill)

---

## Evidence

- `gates.yaml` — v1.0.0 with all five gates, actionable FAIL messages, correct routing and round bounds
- `notes/module17/gate-design.md` — defect table (≥6), G3 ladder table, three-valued outcome table

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Criteria still read as judgement ("tests are good") | Description, not a check | Name the command or artifact fact that decides it, and the expected result |
| G1 retries the validator on a missing-AC failure | Deterministic input treated as a hiccup | Retrying reproduces the same failure; route to the requirement owner (NEEDS_HUMAN) |
| LLM judge is the first responder | Reaching for judgement too early | Run L1→L3 first; LLM is L4 only, and it never rescues a failed deterministic check |
| PRODUCT_DEFECT fails G4 and loops the generator | Class ignored | Allowed through, flagged to the reviewer and owner — the test is correct |
| Round bounds missing | "We'll tune later" | Every retry route needs a counter now; unbounded loops are the defect Module 17 exists to prevent |
| `gates.yaml` has no version | Copied draft | Version the criteria like code — a verdict is meaningless without the criteria revision that produced it |

---

## Checkpoint questions

1. What makes a gate criterion "observable" rather than "claimed"?
2. Why must an LLM-judge verdict never overrule a failing L1–L3 check?
3. When should a gate return NEEDS_HUMAN instead of FAIL?

<details>
<summary>Answers</summary>

1. It is decided from the artifact itself — a file, an exit code, a parsed field — not from the agent's description of it. "Every AC-ID appears in ≥1 `@pytest.mark.ac`" is observable; "the agent says coverage is complete" is not.
2. L1–L3 checks are deterministic, objective, and reproducible: code has already proven the artifact is broken. A probabilistic judge can be persuaded by plausible prose, so letting it overrule is how a broken artifact ships with a green gate.
3. When the gate cannot decide automatically: ambiguous input needing owner intent, a validator/tool failure, or a policy question. FAIL means the criteria were checked and the producer can fix the result; NEEDS_HUMAN means no trustworthy automatic verdict exists.

</details>

---

## Next

**Lab 17.2 — Route the Failure, Rerun Only What Changed, Bound the Loop.** Criteria defined; now decide who retries when a gate says FAIL, what structured feedback they get, which stages re-execute, and when a loop must stop even with rounds left.

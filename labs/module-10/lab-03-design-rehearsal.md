# Lab 10.3 (Optional) — Design Rehearsal: One Agent from Your Spec

**Module 10 · Agent, Skill & Subagent Architecture Fundamentals | Xebia — Cursor AI Training**
Day 3 · Optional extension · ~15–20 minutes · Individual + peer review

> **Objective:** rehearse Module 11 on your own approved Module 9 spec. Pick one pipeline job, draft a five-slot
> agent definition with pinned inputs and a trust-boundary guardrail, map a Module 8 template into the formal
> I/O contract, right-size two candidate delegations, and compose the workflow from Cursor's native capabilities
> first. **This is a draft rehearsal, not Module 11's deliverable** — build, test, and peer-review happen there.

**Guide references:** Module 10, §2 (anatomy), §4 (template → agent contract), §6 (native capabilities), §7 (versioning, review, over-decomposition)
**Learning objectives covered:** 2 — anatomy; 3 — subagent delegation; 4 — parameterized template and I/O contract; 6 — native-capability workflows; 7 — versioning/review, right-sized decomposition.

---

## Before you start

- Your Module 9 artifacts: approved `specs/<feature>/spec.md` (v1.0+) and `specs/<feature>/architecture.md` (contract). If the spec has moved on, use the current version number.
- Pick **one** of Module 11's four jobs for your draft: **requirement analysis · test generation · validation · documentation**.
- Open a new file: `specs/<feature>/agent-design.md`.
- Optional: line up `<reviewer>` for Step 6 — a peer who applies your checklist to your draft.

---

## Step 1 — Gate: is this job agent-worthy?

Write the role as one sentence (≤ 15 words). Then run the promotion gate, adapted from §4:

| Question | Your answer |
|---|---|
| Will another agent or pipeline step invoke it, rather than only a human? | |
| Does it need its own tool scope (e.g., repo search, contract read) that shouldn't leak elsewhere? | |
| Does it need guardrails its caller can't supply? | |
| Must its output be consumed mechanically (structured, not prose)? | |

- [ ] Role written in one sentence, narrow enough to fit on a slide
- [ ] At least one gate question answered **yes**, with the reason stated; if all are "no", say so honestly and keep it a skill/template instead — that's a correct answer, not a failure

---

## Step 2 — Draft the five slots

Build the definition in `agent-design.md`. Frontmatter first:

```markdown
---
name: <agent-name>
version: 0.1.0-draft
owner: <you or team>
status: draft
spec-version: v1.0
reviewed-by: TBD
---
```

Then the five slots — requirements below are checkable, not aspirational:

| Slot | What this draft must contain |
|---|---|
| **Role** | One sentence from Step 1 |
| **Inputs** | Named with shapes; **must pin the spec version** and take AC IDs explicitly; optional inputs marked optional |
| **Tools** | Least privilege; say "none" plainly if none are needed |
| **Guardrails** | At least two; one must be a **trust boundary** tied to Module 9 (e.g., must not invent acceptance criteria, must not rewrite the spec); one must constrain writes (e.g., read-only, no commits) |
| **Outputs** | Structured and machine-checkable (named fields); **must define the failure case** (missing input, unreadable contract, or nothing found) |

- [ ] All five slots present; no slot left as prose paraphrase
- [ ] Inputs pin the spec version and name the AC IDs consumed
- [ ] Guardrails include a trust boundary and a write constraint
- [ ] Outputs define fields **and** a failure case

---

## Step 3 — Map a Module 8 template into the contract

Take one parameterized prompt template from Module 8 (or the prompt you used in Module 9) and promote it on paper:

| Template element | Becomes in the agent definition |
|---|---|
| `{input_1}`, `{input_2}` … | Inputs — named, shaped, version-pinned |
| "Expected output: …" | Outputs — fields + failure case |
| "Fixed instructions: …" | Guardrails / tool scope — binding, not advisory |
| (invoked by a human) | Invoked by another agent / pipeline step (guide §4) |

- [ ] Mapping written for your chosen template
- [ ] One short "advisory → binding" paragraph: what actually changed in the promotion (version pin, tool scope, guardrail enforcement, machine-consumable output, invocation source)

---

## Step 4 — Right-size two delegations

Propose exactly two candidate subagent delegations for your agent (they can be tiny or non-existent — the point is the decision):

```markdown
| Candidate | Isolation need (what it sees / never sees) | Tools it needs | What crosses back | Verdict (accept / reject) | Argument |
```

- [ ] **Accepted candidate** states why isolation helps and what the structured result looks like
- [ ] **Rejected candidate** is priced: at least two concrete handoff costs, plus where the work goes instead (parent slot, rule, or script)
- [ ] If neither candidate earns its place, say so and justify the single-agent design — a correct outcome, not a gap

---

## Step 5 — Compose the workflow from native capabilities

Map where this agent lives in a workflow built from what you already have (guide §6):

| Native capability | What it does in this workflow | What your definition adds |
|---|---|---|
| Ask mode | | |
| Plan mode | | |
| Agent mode | | |
| Rules / `AGENTS.md` | | |
| Skills | | |

- [ ] Every row filled with something concrete from your `<feature>` workflow
- [ ] One explicit "not yet" line: what you are **not** externalizing into orchestration until Modules 15–16, and why the native composition is sufficient for now

---

## Step 6 — Review plan and commit

- [ ] Apply your 4-item checklist to your own draft: role fits one sentence · inputs pinned · trust-boundary guardrail present · outputs machine-checkable with a failure case
- [ ] Define one **sample-task test**: input fixture (AC IDs + rule/contract paths) and the expected output shape — Module 11 will actually run this
- [ ] State the version bump rule (e.g., any change to role/inputs/guardrails bumps `0.x`; adoption to the shared library starts `1.0.0`)
- [ ] Commit as a rehearsal draft:

```bash
git status          # expect: specs/<feature>/agent-design.md (+ notes/module10/ changes)
git add specs/<feature>/agent-design.md notes/module10/
git commit -m "Module 10 rehearsal: draft agent definition for <feature>"
git log --oneline -1
```

---

## Evidence

- `specs/<feature>/agent-design.md` — v0.1-draft with frontmatter + five slots + template mapping + delegation verdicts + capability table
- Self-review checklist result + sample-task test definition
- Commit hash; `notes/module10/construct-decisions.md` from Lab 10.1 still current

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| The draft is turning into a spec rewrite | Scope crept from defining the agent to defining the feature | Keep the spec untouched; if you found a real gap, version the spec per Module 9 and record it there |
| Inputs are vague ("the spec") | Skipped consumability | Pin path + version + AC IDs; ask: could another agent pass these verbatim? |
| Guardrails are platitudes ("be accurate") | Not phrased as failure preventions | Start from a failure mode and write "must not …"; make each checkable |
| Every job gets a subagent | Defaulting to decomposition | Apply Step 4's test; default is one agent; delegation must earn the handoff |
| Output is prose | Skipped the contract | Name fields, add shapes, and define the failure case — machine-checkable or it isn't reusable |
| Tempted to build and run it now | Enthusiasm (fair) | Module 11 is the build: test assets independently, then peer review. Keep this a draft |

---

## Checkpoint questions

1. When is a parameterized template enough, and when does it warrant promotion to an agent definition?
2. Why must an agent's inputs pin a spec version rather than just point at the spec file?
3. What makes a subagent delegation "earn its place"?

<details>
<summary>Answers</summary>

1. A template is enough while a human invokes it and no independent tools or guardrails are needed. Promote it when another agent must invoke it, it needs its own tool scope, or it needs binding guardrails and a machine-consumable output.
2. So the agent can be audited against the exact revision it was given: a stale `spec.md` path can silently validate the wrong version. Pinning the version makes the run reproducible and keeps traceability back to the approved artifact (Module 9's versioning rule).
3. A genuine isolation benefit (focused context, nothing irrelevant), a structured result the parent consumes mechanically, and no simpler home (parent slot, rule, or script) that does the same job without the handoff cost.

</details>

---

## Next

**Module 11 — Use Case Lab 1: Reusable Agents, Prompts & Skills Framework.** Bring this draft: you'll build four agent roles plus a justified subagent, test each independently, and commit the shared, version-controlled library. Your draft can be promoted — or corrected — but the library is built there, not here.

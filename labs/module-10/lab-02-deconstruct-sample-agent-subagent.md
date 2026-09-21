# Lab 10.2 — Walkthrough: Deconstruct a Sample Agent & Subagent

**Module 10 · Agent, Skill & Subagent Architecture Fundamentals | Xebia — Cursor AI Training**
Day 3 · Lab 2 of 3 · ~20 minutes · Pairs, group debrief

> **Objective:** do exactly what the module's hands-on promises — take a working agent definition and its paired
> subagent definition, map every field back to the anatomy, trace what crosses the isolation boundary in each
> direction, classify which parts began life as Module 8 assets, and flag one delegation that shouldn't exist.
> **No building in this lab** — you construct your own definitions in Module 11.

**Guide references:** Module 10, §2 (agent anatomy), §3 (subagent delegation), §7 (versioning, review, over-decomposition), §8 (hands-on walkthrough)
**Learning objectives covered:** 2 — anatomy; 3 — subagent delegation; 7 — definitions as code, avoiding over-decomposition.

---

## Before you start

- Read-only fixtures ship in this pack — open all three (do not edit them):
  - [`samples/spec-readiness.agent.md`](samples/spec-readiness.agent.md) — the parent agent
  - [`samples/convention-check.subagent.md`](samples/convention-check.subagent.md) — a focused subagent
  - [`samples/note-format.subagent.md`](samples/note-format.subagent.md) — a second subagent
- Create your working file: `notes/module10/sample-annotations.md` with these headings — *Summary · Anatomy map · Boundary trace · Provenance · Decomposition verdict · Lifecycle*
- The `agents/<name>.agent.md` format is this course's portable convention; Cursor realizes these semantics through rules, skills, `AGENTS.md`, and agent commands. Judge the definitions on their content, not the file format.
- Rule of the lab: **the sample is deliberately imperfect.** Finding nothing is not an option; finding *consequences* is the skill.

---

## Step 1 — First read, no analysis (~2 minutes)

Read all three files end to end once, without annotating.

- [ ] Write a two-sentence summary: what the system does as a whole, and how the parent relates to its two subagents
- [ ] Note what the frontmatter records (version, owner, status, review) — you'll return to it in Step 6

---

## Step 2 — Anatomy map

For the parent (`spec-readiness`) and for `convention-check`, fill a table:

```markdown
| Slot | What the sample says (quote it) | Which question it answers | Verdict: complete / weak / missing + consequence |
```

Cover all five slots, in order: **Role · Inputs · Tools · Guardrails · Outputs** (guide §2).

- [ ] Both definitions mapped, fields quoted rather than paraphrased
- [ ] At least one weak or missing slot flagged — and if you mark a slot weak, state the concrete failure it would cause when the definition is reused

---

## Step 3 — Trace the isolation boundary

For `convention-check`, draw the boundary explicitly in your notes:

```text
IN  → (what the subagent receives)
OUT → (what it returns)
EXCLUDED → (what it deliberately never sees)
```

- [ ] `IN` list matches the definition's inputs — nothing extra smuggled in
- [ ] `OUT` list matches the definition's output schema — note that the parent gets a *result shape*, not a narrative
- [ ] `EXCLUDED` list names at least three things the subagent cannot see (parent conversation, full spec, other findings, …) and one sentence on why each exclusion helps (Module 6 context discipline, applied at agent level)
- [ ] Failure at the boundary: describe one situation where isolation costs something (e.g., a rule path can't be read, or criteria text is ambiguous) and say what the definition *should* add to handle it

---

## Step 4 — Provenance: what was new here?

Classify each element below as **Module 8 rule**, **Module 8 skill**, **Module 8 template**, or **newly formalized in Module 10**. Cite the evidence in the fixture that lets you decide.

1. "Must cite the rule path for every convention conflict"
2. The report shape: verdict + findings + questions
3. "Ask-not-edit behaviour"
4. The five-slot anatomy itself (Role/Inputs/Tools/Guardrails/Outputs)
5. The Delegation section listing two subagents
6. The `IN`/`OUT` declarations on `convention-check`
7. "Judge conventions only — never requirement quality"

- [ ] All 7 classified with a citation or an explicit "no Module 8 source — formalized here"
- [ ] One sentence: what does going from Module 8 asset → Module 10 definition *add*? (hint: a citation is not the difference)

---

## Step 5 — Flag the unnecessary decomposition

One of the two delegations shouldn't be a subagent. Identify it, then argue it properly:

- [ ] Name the delegation and quote its Role/Guardrails/Tools
- [ ] Apply §7's test: does it need an **isolated context**? its own **tools**? independent **guardrails**? a structured **result the parent consumes mechanically**? Answer each explicitly
- [ ] Price the handoff: extra delegation overhead, context fragmentation, harder debugging — at least two concrete costs
- [ ] Propose the concrete fold-back: which existing slot of the parent (or which deterministic script/rule) absorbs the work, and what line you'd change
- [ ] Counter-check: under what conditions *would* that delegation earn its place? (e.g., format is complex, versioned, reused by several agents, owned by another team) — then state whether those conditions hold in the sample

---

## Step 6 — Review and test it like code

Apply the §7 lifecycle to the sample:

- [ ] Interpret the frontmatter: what does `status: reviewed` vs. `draft` claim, and what's missing before `convention-check` could be adopted?
- [ ] Propose **one sample-task test** for `convention-check`: the input fixture (one conflicting criterion + one clean criterion + a rule path), the expected output shape (`conflicts: 1`, entry fields), and a second run expected to return `no-conflicts`
- [ ] Write a **4-item review checklist** the parent would have to pass before adoption (e.g., role fits one sentence; inputs pinned; trust-boundary guardrail present; outputs machine-checkable incl. failure case)
- [ ] Name one trigger that should force a re-review (e.g., spec format changes, a repo rule changes, a missed gap in production)

---

## Evidence

- `notes/module10/sample-annotations.md` containing: summary; anatomy map for both definitions; boundary trace (IN/OUT/EXCLUDED + failure case); 7-row provenance classification; decomposition verdict with cost argument and fold-back; lifecycle test + review checklist + re-review trigger
- Pairs compare: where your classification differed, was the difference *evidence* or *preference*?

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Can't find the referenced Module 8 files | Fixture names are representative, not literal | Classify by **construct** — rule vs. skill vs. template — from how the citation is used (standing behaviour / task capability / fill-in prompt) |
| Everything looks "newly formalized" | Citations were skimmed | Look for `.cursor/rules/`, `.cursor/skills/`, `prompts/`, `AGENTS.md` references in the fixtures |
| Disagreement about the unnecessary subagent | Arguing taste instead of cost | Apply §7's four-question test, price the handoff, and only then argue |
| "Missing slot" vs. acceptable brevity | No consequence attached | A slot may be terse; if its absence changes behaviour when reused, it's a defect. State the failure |
| Found several flaws | Stopped at detection | Prioritize the two with the most concrete failure consequences and say why they rank higher |
| Definition format feels unfamiliar | Expecting a native product file format | It's the course's portable convention; Module 11 builds the library in it |

---

## Checkpoint questions

1. Name the five anatomy slots. Which slot is weakly specified in the parent, and what could it cause?
2. Why is `convention-check`'s isolated context an advantage rather than a limitation?
3. What would have to be true for `note-format` to justify being a subagent?
4. Which elements of the sample existed before Module 10, and which are new here?

<details>
<summary>Answers</summary>

1. Role, Inputs, Tools, Guardrails, Outputs. The parent's Inputs take `{spec_path}` **without pinning a spec version**, so it can silently validate a v1.0 gate against a changed v1.1 spec — exactly the drift Module 9's versioning rule prevents. Its Outputs also have no failure case for an unreadable spec.
2. It receives only the criteria and rule paths it needs, so unrelated context can't distract or bias it; and it returns a fixed result shape the parent can consume without translation. That's Module 6's context-window discipline applied at the agent level.
3. That formatting genuinely needed its own tools, independent guardrails, or isolated context, and that the parent consumed its output as a structured contract — e.g., a complex versioned format reused by several agents and separately owned. In the sample, none hold: no tools, no guardrails, no isolation need, and the parent could format in its own Outputs step.
4. Pre-existing: the repo rule (`.cursor/rules/spec-review.mdc`), the skill (`.cursor/skills/requirement-clarify/SKILL.md`), the template (`prompts/requirement-review.md`). New in Module 10: the five-slot anatomy, explicit delegation, and the IN/OUT isolation declarations — i.e., formal contracts around what was previously advisory.

</details>

---

## Next

**Module 11 — Use Case Lab 1** is next, and it builds on this walkthrough directly: four agent roles, a focused subagent you *justify* (using the Step 5 test, in reverse), parameterized templates with I/O contracts, and rules/skills packaged into a shared library. If Module 10 finishes early, run **Lab 10.3** as a rehearsal on your own Module 9 spec.

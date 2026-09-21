# Lab 11.1 — Define the Four Agents and Their Prompt Templates

**Module 11 · Use Case Lab 1: Reusable Agents, Prompts & Skills Framework | Xebia — Cursor AI Training**
Day 3 · Lab 1 of 4 · ~30 minutes · Individual; pair-check at the end

> **Objective:** turn Module 10's anatomy into four real, reusable agent definitions — requirement analysis, test
> generation, validation, documentation — and give each one a parameterized prompt template whose input/output
> contract is explicit enough that **a call can fail**. Build and keep them independent: no chaining, no
> orchestration (that's Module 16).

**Guide references:** Module 11, §1 (agent roles), §2 (parameterized templates with I/O contracts)
**Learning objectives covered:** 1 — define agent roles with Module 10's anatomy; 2 — explicit, checkable I/O contracts.

---

## Before you start

- Create the library skeleton at `<sandbox-repo>/shared-agent-library/`:

```text
shared-agent-library/
├── agents/
├── subagents/
├── templates/
├── skills/
├── rules/
└── AGENTS.md
```

- Have Module 10's `notes/module10/construct-decisions.md` open, and — if you wrote one — the Lab 10.3 draft `specs/<feature>/agent-design.md` (you may promote it into the Requirement Analysis or Validation agent).
- Keep Module 9's `spec.md` open: its AC style (`AC-1`, testable, one verification each) is the quality bar your agents enforce.
- Definitions stay **feature-agnostic** — they are reusable assets, not one-off prompts for `<feature>`.

---

## Step 1 — Write the four role sentences

For each agent, complete the row. The role must fit **one sentence** and not overlap a neighbour's.

| Agent | Role (one sentence) | Primary input | Primary output |
|---|---|---|---|
| Requirement Analysis | | | |
| Test Generation | | | |
| Validation | | | |
| Documentation | | | |

- [ ] Four roles written; each fits one sentence
- [ ] No role overlaps: if two could be swapped, tighten both until they can't
- [ ] For each, you can say **who invokes it today** (a human) and who will invoke it later (another agent / pipeline step — Module 16)

---

## Step 2 — Write the four agent definitions

Create one file per agent, e.g. `shared-agent-library/agents/requirement-analysis.agent.md`. Frontmatter first:

```markdown
---
name: <agent-name>
version: 0.1.0-draft
owner: <you or team>
status: draft
reviewed-by: TBD
---
```

Then the five slots. These are **checkable requirements**, not suggestions:

| Slot | Requirement |
|---|---|
| **Role** | The Step 1 sentence |
| **Inputs** | Named with shapes (e.g., `{reqText: string}`, `{repoPath: string}`); no "the context" |
| **Tools** | Least privilege — read-only unless the role genuinely needs more; say "none" plainly if none |
| **Guardrails** | At least one from the table below, plus one write constraint (e.g., "never edit the spec/contract") |
| **Outputs** | Named fields with shapes, **plus a failure case** (missing input, unreadable file, nothing found) |

Minimum guardrails per agent (guide §1) — add at least one more of your own:

| Agent | Non-negotiable guardrail |
|---|---|
| Requirement Analysis | Must not invent acceptance criteria absent from the source |
| Test Generation | Tests must map 1:1 to stated acceptance criteria |
| Validation | Must flag mismatches, not silently "fix" the contract |
| Documentation | Must cite the specific requirement/test it documents, not summarize generically |

- [ ] Four `agents/*.agent.md` files created, all five slots complete
- [ ] Every output schema has named fields and a defined failure case
- [ ] No guardrail is a platitude ("be accurate") — each prevents a named failure

---

## Step 3 — Write the four prompt templates

Create `shared-agent-library/templates/<agent-name>.prompt.md` — the parameterized prompt that instantiates each agent (Module 8 §5 + Module 10 §4). Every template carries four elements:

```markdown
# <template name>
**Purpose:** <one line>
**Inputs:** `{input_1}` (<shape>), `{input_2}` (<shape>)
**Fixed instructions:** <the invariants — conventions, tooling, ordering>
**Expected output:** <schema: named fields + shapes, incl. the failure shape>
```

Declare schemas explicitly, like the deck's worked example:

```text
requirement-analysis.prompt.md
  INPUT:  { reqText, repoPath }
  OUTPUT: { complete, testable, gaps[] }     ← a call missing "gaps" must be rejectable
```

Starting schemas (refine them, but keep them machine-checkable):

| Template | Output schema (minimum) |
|---|---|
| requirement-analysis | `{complete: bool, testable: bool, gaps: [{gap_type, excerpt, why}]}` |
| test-generation | `{test_files: [{path, content}], ac_coverage: [{ac_id, test_name}]}` |
| validation | `{status: PASS \| FAIL, mismatches: [{test, clause, detail}]}` |
| documentation | `{doc_path, citations: [{claim, source_id}]}` |

- [ ] Four `templates/*.prompt.md` files, all four elements present
- [ ] Every input is named **and** shaped; no prose-only contracts
- [ ] Every template has at least one required output field a bad call could omit

---

## Step 4 — Prove a call can fail

For each template, write one **passing call** and one **failing call** into a table in your notes (Lab 11.2 will carry it into `shared-agent-library/AGENTS.md`):

```markdown
| Template | Passing call (inputs → all required fields) | Failing call (what's missing/violated) |
```

- [ ] Four rows; every failing call names the specific missing/violated field
- [ ] You can explain in one sentence why "the output looked reasonable" is not a pass — conformance to the declared schema is

---

## Evidence

- `shared-agent-library/agents/` — four `.agent.md` files, five slots each, `version: 0.1.0-draft`
- `shared-agent-library/templates/` — four `.prompt.md` files with named/shaped I/O and failure shapes
- Passing/failing call table (Step 4)

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Roles overlap (analysis vs. validation) | Role written as activity, not responsibility | Separate by output: analysis *describes gaps*; validation *judges conformance to the contract* |
| Inputs say "the spec" / "context" | Skipped shaping | Name the parameter and its shape; ask: could another agent pass this verbatim? |
| Guardrails read like values, not rules | No failure mode named | Start from "what would go wrong?" and write "must not …" |
| Output schema is prose | Skipped the contract | Name fields and shapes; add the failure shape; make it checkable without judgment |
| Tempted to chain the agents now | Enthusiasm (fair) | They stay independent in this lab — chaining is Module 16; independence is what makes it debuggable later |
| Template duplicates the agent definition | Wrong file scope | Template = the invocation contract (inputs → output shape); agent = role + tools + guardrails + outputs. Link them, don't merge them |

---

## Checkpoint questions

1. Why do the four agents get built and tested independently instead of chained immediately?
2. What makes a template's I/O contract "explicit" rather than descriptive?
3. Where do the agent definition and the prompt template differ in responsibility?

<details>
<summary>Answers</summary>

1. Orchestration (chaining, gates, correction loops) is Modules 15–17's concern. Correct standalone agents can be chained with confidence; debugging correctness and orchestration at once is much harder.
2. It names each input/output and states its shape (e.g., `{complete, testable, gaps[]}`), so conformance can be checked mechanically — a call passes or fails — rather than judged as "looks right".
3. The agent definition owns role, tools, guardrails, and outputs (the durable contract); the template is the parameterized invocation that supplies the inputs and expects the declared output shape. The template is how a caller *uses* the agent.

</details>

---

## Next

**Lab 11.2 — Package the Shared Library and Add One Focused Subagent.** You'll finish the library layout (rules/skills at the right level), write the library index, and define the one delegation the parent agent shouldn't do itself.

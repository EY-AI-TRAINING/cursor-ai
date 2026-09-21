# Lab 13.1 — Wire the Grounded Agent to Its Sources

**Module 13 · Use Case Lab 2: Knowledge-Grounded Engineering Agent | Xebia — Cursor AI Training**
Day 4 · Lab 1 of 5 · ~20 minutes · Individual or pairs

> **Objective:** do guide §1 — define the knowledge-grounded agent as a library asset, then wire it to all five
> grounding source categories: repository code (direct), SRS/SDS (MCP Resource or direct file), standards
> (Project Rule), historical defect log (MCP Resource), and enterprise knowledge (MCP Resource). One connection
> protocol for everything outside the repo — no ad hoc scripts.

**Guide references:** Module 13, §1 (connecting sources via MCP); Module 12 §2–§3 (source classes, MCP anatomy); Module 10 §2 (five-slot anatomy); Module 11 §3 (library structure)
**Learning objectives covered:** 1 — connect an agent to repository, document, and knowledge sources via MCP.

---

## Before you start

- Module 12 complete on `module12-lab`: `knowledge/` corpus, `.cursor/mcp.json` (Path A) or inspection notes (Path B), `.cursor/rules/grounding-discipline.mdc`, and `notes/module12/` results
- Module 11 library present at `shared-agent-library/` (tag `v0.1.0`): `agents/ subagents/ templates/ skills/ rules/ reviews/ testing/ AGENTS.md`
- Branch: `git switch -c module13-lab` from `module12-lab`
- If you don't have the Module 11 library: create the same folder tree and start the index; use [`samples/knowledge-grounded.agent.md`](samples/knowledge-grounded.agent.md) as the scaffold and note the gap in `AGENTS.md`
- Runner: Cursor Agent chat. Offline fallback per facilitator notes

---

## Step 1 — Define the agent asset

Create `shared-agent-library/agents/knowledge-grounded.agent.md` (scaffold: [`samples/knowledge-grounded.agent.md`](samples/knowledge-grounded.agent.md)). Frontmatter first:

```markdown
---
name: knowledge-grounded
version: 0.1.0-draft
owner: <you or team>
status: draft
reviewed-by: TBD
---
```

Then the five slots (Module 10), all filled — no "TBD" inside a slot:

| Slot | Requirement |
|---|---|
| **Role** | One sentence: answers questions strictly from the connected grounded sources, cites every factual claim, declines when unsupported |
| **Inputs** | Named with shapes — `{question: string}`, the grounded source set, and the path to `agents/knowledge-grounded.retrieval-scope.yaml` (written in Lab 13.2) |
| **Tools** | Least privilege: repo read/search + MCP `knowledge-files` read/search; **nothing** that writes, moves, or deletes |
| **Guardrails** | The grounding clauses: cite every factual claim; never speculate beyond retrieved context; standard refusal phrase; no related-fact substitution (Lab 13.3 promotes these into the loaded rule) |
| **Outputs** | `{answer, citations[{claim, source}], declined, unsupported[]}` + failure case (sources unreachable or out of scope → `declined: true`, no invented content) |

- [ ] Agent file created, five slots complete, version `0.1.0-draft`
- [ ] The agent is **one** agent — no chaining or pipeline steps (that's Module 16)

---

## Step 2 — Wire source 1: repository code (direct context)

Code stays in **direct context** — no protocol needed for what's already local (deck §01).

- [ ] Record the code paths that count as repository code (your Module 9 implementation, or the fixture path `src/middleware/rate_limit_middleware.py` if you used the sample)
- [ ] Confirm Cursor can retrieve from them (open a file, ask one code question) — record the evidence line

---

## Step 3 — Wire source 2: SRS/SDS documents

Everything outside the repo connects through the Module 12 MCP server.

- [ ] Reached via: MCP Resource (`knowledge-files`, scoped to `${workspaceFolder}/knowledge`) **or** direct file context if you ran Module 12 Path B
- [ ] Exact path recorded: `knowledge/sds-excerpt-rate-limiting.md` (or your Module 9 spec/architecture docs, copied into `knowledge/`)
- [ ] One retrieval confirmed (a question only this source answers)

---

## Step 4 — Wire source 3: standards (Project Rule)

Standards are a rule, not a document (guide §1 table; Module 8).

- [ ] Promote [`samples/standards-excerpt-api-conventions.md`](samples/standards-excerpt-api-conventions.md) into `<sandbox-repo>/.cursor/rules/api-conventions.mdc` — or use your own Module 8 standards rule
- [ ] Canonical copy placed in `shared-agent-library/rules/api-conventions.mdc`; load location recorded
- [ ] One question confirmed answered from the rule (e.g., what a `429` must include)

---

## Step 5 — Wire sources 4–5: defect log + enterprise knowledge

Same MCP connection, two more source types (deck §01: "three source types, one connection protocol").

- [ ] `knowledge/defect-log.md` reachable via `knowledge-files` (or direct file context)
- [ ] `knowledge/runbook-api-gateway.md` reachable via `knowledge-files` (or direct file context)
- [ ] No second server stood up — the point is one connection protocol, not five

---

## Step 6 — Prove reachability (not just configured-looking)

Create `shared-agent-library/testing/source-reachability.md`:

```markdown
| Source category | Reached via | Question it answers | Retrieval evidence |
|---|---|---|---|
| Repository code | direct context | … | … |
| SRS/SDS | MCP Resource (or direct file) | … | … |
| Standards | Project Rule | … | … |
| Historical defect log | MCP Resource | … | … |
| Enterprise knowledge | MCP Resource | … | … |
```

- [ ] All five rows filled; every row names a question the source answers
- [ ] "Retrieval evidence" shows the source was **actually pulled** (tool call, attachment, or file open) — not merely listed in the agent definition
- [ ] Update `shared-agent-library/AGENTS.md`: add the agent + standards rule rows with version/status/owner/load location

---

## Evidence

- `shared-agent-library/agents/knowledge-grounded.agent.md` — five slots, `0.1.0-draft`
- `.cursor/rules/api-conventions.mdc` + `shared-agent-library/rules/api-conventions.mdc`
- `shared-agent-library/testing/source-reachability.md` — five rows with retrieval evidence
- Updated `shared-agent-library/AGENTS.md` index

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| MCP server isn't live (no `npx`/network) | Module 12 Path B environment | Use direct file context for the three external sources and say so in the reachability table — same outcomes, different wiring |
| Source listed but never retrieved | "Configured-looking" is not reachable | Ask a question only that source can answer and capture the retrieval as evidence |
| Five sources become five servers | Misread the deck | Repo = direct; docs + defect log + enterprise knowledge = **one** `knowledge-files` connection; standards = a rule |
| Code copied into `knowledge/` | Habit from Module 12 | Code belongs in direct context; keep the corpus for external sources |
| Standards live as a document, not a rule | Skipped Module 8's mechanism | Promote to `.cursor/rules/` with a canonical copy in the library; rules are versioned text |
| Guardrail slot left "TBD" | Waiting for Lab 13.3 | Write the clauses now; 13.3 promotes the same clauses into the loaded rule — no slot stays empty |

---

## Checkpoint questions

1. Why does repository code stay in direct context while documents and knowledge go through MCP?
2. What's the difference between a source being *configured* and a source being *reachable*?
3. Why are standards implemented as a rule rather than a document in the corpus?

<details>
<summary>Answers</summary>

1. Local code is already available to the agent without a protocol — adding MCP there adds a moving part with no gain. External systems (document stores, defect databases, wikis) need a standard connection, which is what MCP provides — and one protocol keeps the agent's definition independent of the underlying store.
2. Configured means it appears in a config or the agent definition; reachable means a real question was answered from it and the retrieval is captured as evidence. Reviewers check the second, because the first is easy to fake.
3. Standards constrain behaviour on every invocation, which is exactly what a Project Rule does — loaded automatically and versioned like code. A document in the corpus is retrieved only when relevant; a rule is always in force.

</details>

---

## Next

**Lab 13.2 — Scope Retrieval and Citation.** You'll write the retrieval-scope contract, fix the citation format, and verify on a live question that the agent pulls the relevant chunk — not whole documents.

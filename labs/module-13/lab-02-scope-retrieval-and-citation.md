# Lab 13.2 — Scope Retrieval and Citation

**Module 13 · Use Case Lab 2: Knowledge-Grounded Engineering Agent | Xebia — Cursor AI Training**
Day 4 · Lab 2 of 5 · ~15 minutes · Individual or pairs

> **Objective:** do guide §2 — write the **retrieval-scope contract** (which paths, collections, and ranges a
> retrieval may search) and fix the **citation format** (how every factual claim names its source). Then verify
> on a live question that the agent pulls the relevant chunk — not whole documents — and cites it checkably.

**Guide references:** Module 13, §2 (retrieval scoping and source citation); Module 12 §1 (scope), §4 (retrieval strategies)
**Learning objectives covered:** 2 — configure retrieval scoping; 3 — configure source citation.

---

## Before you start

- Lab 13.1 complete: agent defined, five sources reachable, `testing/source-reachability.md` filled
- Open [`samples/retrieval-scope-example.yaml`](samples/retrieval-scope-example.yaml) and [`samples/grounding-stress-questions.md`](samples/grounding-stress-questions.md)
- Start `shared-agent-library/testing/grounding-stress-test.md` with a header row — Lab 13.4 completes it; ST-1 lands here

---

## Step 1 — Author the scoping contract

Create `shared-agent-library/agents/knowledge-grounded.retrieval-scope.yaml` (adapt the example's paths to your repo):

```yaml
agent: knowledge-grounded
version: 0.1.0-draft
allow_paths:
  - /src
  - /knowledge/sds-excerpt-rate-limiting.md
  - /knowledge/defect-log.md
  - /knowledge/runbook-api-gateway.md
allow_collections:
  - repo
  - knowledge-files
deny:
  - /knowledge/drafts
  - chat-history
  - node_modules
  - .env
require_citation: true
citation_format:
  docs: "<path> › <section>"
  code: "<path>:<line>"
  defects: "DEF-###"
  standards: "<rule-path> › <section>"
```

- [ ] Allow list names the paths this agent may search — not "everything in the repo"
- [ ] Deny list is explicit; nothing secret or draft-level is reachable
- [ ] `require_citation: true`; citation format is exact enough that a reviewer can find the claim in seconds
- [ ] YAML validates (spaces, not tabs)

---

## Step 2 — Name the enforcement layers

The scope file is the **contract**; two existing mechanisms do the **enforcing** (deck §02: scoping is config, citation is response format — both checkable mechanically). Record this table in `testing/grounding-stress-test.md`:

| Layer | Enforces | Where it lives |
|---|---|---|
| MCP connection scope | Which collection the server can see at all | `.cursor/mcp.json` — `${workspaceFolder}/knowledge` |
| Retrieval-scope contract | Which paths/collections a query may pull, and the citation format | `agents/knowledge-grounded.retrieval-scope.yaml` |
| Guardrail rule | Citation requirement + refusal behavior on every response | `.cursor/rules/` (written in Lab 13.3) |

- [ ] Table filled in with your actual paths
- [ ] `.cursor/mcp.json` still scoped to `${workspaceFolder}/knowledge` — no broader path, no secrets

---

## Step 3 — Run ST-1 and check scoping + citation

Fresh chat, grounded sources reachable, agent definition in play. Ask **ST-1**: *"What limit does the API gateway enforce, and per what key?"*

Record in the matrix:

```markdown
| # | Category | Expected (written before the run) | Actual | PASS/FAIL | Evidence |
|---|---|---|---|---|---|
| ST-1 | In-scope, well-supported | … | … | | transcript link |
```

- [ ] Prediction written **before** the run
- [ ] Answer cites the runbook specifically (`path › section`) — not "the docs" or "the runbook" generically
- [ ] Citation spot-checked: you opened the cited source and found the claim
- [ ] Retrieval was scoped: the relevant section came in, not whole-document dumps — note roughly what was pulled per source

---

## Step 4 — Test the deny/absent path

Fresh chat. Ask: *"Summarize the draft design notes for rate limiting."* Nothing in the allow list (or in the corpus) supports it.

- [ ] Agent declines or flags the gap — it does **not** invent draft content or cite a source outside the allow list
- [ ] Record the run as the scoping-gap evidence row in the matrix

---

## Step 5 — Note scoped-vs-dumped evidence

- [ ] One line per source: what a **scoped** pull returned for ST-1 vs. what attaching the whole document would have added (noise)
- [ ] One sentence: what this proves about connecting a source vs. controlling how much of it is retrieved

---

## Evidence

- `shared-agent-library/agents/knowledge-grounded.retrieval-scope.yaml`
- `shared-agent-library/testing/grounding-stress-test.md` — enforcement-layer table, ST-1 row with prediction + spot-check, scoping-gap row
- ST-1 and deny-path transcripts

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Citation says "the docs" / "the runbook" | Citation format not yet enforced by the rule | Exact format goes in the rule in Lab 13.3; for now note it as the known gap and re-run after 13.3 |
| Whole documents come back for one question | Allow list too broad, or MCP scope wider than `knowledge/` | Tighten `allow_paths`; confirm `.cursor/mcp.json` scopes to `${workspaceFolder}/knowledge` |
| Agent cites a path outside the allow list | Contract not enforced (rule pending) | Treat as a FAIL for 13.4 to fix via the rule; add the clause "retrievals come only from `allow_paths`" |
| YAML won't parse | Tabs or stray characters | Spaces only; validate before moving on |
| Deny-path question gets answered anyway | Fabrication, or a source outside the corpus | Mark FAIL, capture the transcript — this is exactly what Lab 13.4's diagnose loop is for |
| Everything feels fine but nothing was retrieved | Direct file context attached everything up front | Note the difference: attachment is not retrieval; scoping still governs what the agent *uses* and *cites* |

---

## Checkpoint questions

1. What does retrieval scoping control that a successful connection does not?
2. What makes a citation useful to a reviewer, versus a vague reference?
3. Why are scoping and citation described as "mechanically checkable" rather than a matter of review taste?

<details>
<summary>Answers</summary>

1. Connection decides whether a source is available at all; scoping decides how much of it a given query may pull. Too broad dilutes the answer with noise; too narrow misses the material that answers the question.
2. It is specific and checkable — exact path, section, line, or ID — so a reviewer can verify the claim in seconds instead of re-deriving it.
3. Both reduce to rules a program (or a careful reviewer) can apply without judgment: was the retrieved path inside the allow list, and does every factual claim carry a citation in the declared format? "Looks reasonable" is not a criterion.

</details>

---

## Next

**Lab 13.3 — Enforce the Guardrail as a Rule.** The contract exists; now make it hold automatically. You'll promote the grounding clauses into `rules/grounded-agent.mdc`, load it, and prove the refusal phrase appears without restating the rule.

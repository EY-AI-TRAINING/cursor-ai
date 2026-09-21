# Lab 9.2 — Architecture Diagram, Interface Contract & ADR

**Module 9 · AI-Assisted Design & Spec-Driven Development (SDD) | Xebia — Cursor AI Training**
Day 3 · Lab 2 of 3 · ~15–20 minutes · Individual

> **Objective:** translate the approved spec into the first *how* artifacts — a text-based architecture diagram
> and an API/interface contract — and record the one significant design decision behind them as an ADR. All three
> are AI-drafted and **human-reviewed** before they're trusted. Still no implementation code.

**Guide references:** Module 9, §5 (diagram + API contract generation), §6 (ADRs; SRS → SDS)
**Learning objectives covered:** 5 — diagrams and contracts with AI assistance; 6 — ADRs and SRS→SDS.

---

## Before you start

- Lab 9.1 complete: `<spec-file>` is approved at **v1.0** on `module9-lab`
- Decide the interface under design: `<api-endpoint>` (e.g., `POST /<resource>`) — if the feature is UI-only,
  use the component/function interface instead
- Keep it lightweight: **one diagram, one contract, one ADR.** The point is the reviewed artifact, not exhaustive design

---

## Step 1 — Generate the architecture diagram (text, so it's reviewable)

Mermaid is source code, which is the entire point: it diffs, reviews, and versions like the spec (guide §5).

1. In Plan/Ask mode, prompt:

   > "Read `@specs/<feature>/spec.md` (approved v1.0). Generate a **lightweight** Mermaid architecture diagram:
   > components involved (existing and new), how they communicate, and external dependencies. Cite the real file
   > paths for components that already exist. Do not invent components that no acceptance criterion needs."

2. Save it to `specs/<feature>/architecture.md` (fenced `mermaid` block).
3. Review it as a human architect would:

   | Check | Notes |
   |---|---|
   | Every new component traces to an AC or NFR | |
   | Existing components cite real paths from the repo | |
   | Nothing speculative (no invented services/queues the sandbox doesn't have) | |
   | No component that no AC requires (gold-plating) | |

4. Make at least one correction — remove a speculative component, fix a wrong path, or simplify a flow.

- [ ] `architecture.md` contains the Mermaid diagram; renders in Cursor's markdown preview
- [ ] Diagram reviewed; at least one correction made or explicitly rejected (noted)
- [ ] Every new component attributes to a spec element

---

## Step 2 — Draft the API/interface contract

1. Prompt the agent to draft the contract **from the spec**, using your repo conventions:

   > "Using `@specs/<feature>/spec.md` v1.0 and the conventions in `AGENTS.md` / `.cursor/rules/`, draft the
   > interface contract for `<api-endpoint>`. Include request shape, success response, error responses with
   > status codes and error codes, and the non-functional constraints. Do not add fields or endpoints that no
   > acceptance criterion requires."

2. Save under `specs/<feature>/architecture.md` (or `contract.md`):

   ```markdown
   ## Contract: <endpoint / interface>
   **Method / Path:** ...
   **Request:** <fields, types, required?, validation rules>
   **Success response:** <status, body shape>
   **Error responses:** <status · error code · when>
   **Non-functional:** <timeout, rate limit, logging constraints>
   ```

3. Review against the project's real conventions — this is where Module 8's rules/`AGENTS.md` earn their keep:

   | Check | Notes |
   |---|---|
   | Naming matches project conventions (`ApiError`, error-code scheme, casing) | |
   | Every error case traces to an AC or NFR | |
   | Every field/endpoint traces to an AC (remove what doesn't) | |
   | Non-functional constraints from spec §3 are represented | |

- [ ] Contract drafted from the spec (not from the agent's imagination); conventions cited
- [ ] Reviewed with ≥1 correction; any removed field/endpoint noted
- [ ] Error cases trace to AC IDs or NFRs

---

## Step 3 — Record one ADR (the decision the design forced)

Pick the **one** significant decision the contract or diagram forced — e.g., sync vs. async notification, idempotency
strategy, new table vs. reuse, retry policy. (Two ADRs means you haven't picked the significant one.)

> "Draft an ADR for `<decision>` using the anatomy in Module 9 §6: context, options considered, decision,
> consequences. Keep it under 20 lines. Base it on the approved spec and the contract — do not invent constraints."

```markdown
# ADR-000N: <decision-focused title>
**Status:** Proposed · **Date:** YYYY-MM-DD

## Context
<what forces/constraints made this decision necessary>

## Options considered
1. <option + one-line trade-off>
2. <option + one-line trade-off>

## Decision
<what was chosen>

## Consequences
- Trade-offs accepted:
- Follow-on work:
```

Human review before accepting:

- [ ] The decision recorded is the one the contract actually embodies (consistency check)
- [ ] At least two realistic options listed — not one option plus a strawman
- [ ] Consequences include something uncomfortable (a real trade-off, not marketing)
- [ ] Status set to **Accepted** (or left **Proposed** with the reason noted)
- [ ] Saved as `docs/adr/ADR-000N-<slug>.md`

---

## Step 4 — (Quick) SRS → SDS note

This is the guide's §6 translation in miniature — business language to technical design, on the record. Add 3–5
sentences to `architecture.md` under `## Design summary (SRS → SDS)`: for each AC group, name the component and
contract element that will satisfy it. (Module 20's capstone does the full formal version; this is the habit.)

- [ ] Short SRS→SDS mapping written; every AC group maps to a component + contract element

---

## Step 5 — Commit the design artifacts

```bash
git status                     # expect: specs/ + docs/adr/ changes only — still no source code
git add specs/ docs/adr/
git commit -m "Module 9 lab: architecture, contract, and ADR for <feature>"
git log --oneline -1
```

- [ ] Committed on `module9-lab`; hash `____________`
- [ ] `git status` before commit confirmed **zero source changes** (implementation is Lab 9.3)

---

## Evidence

- `architecture.md` — Mermaid diagram + contract + SRS→SDS note
- Review notes (≥1 diagram correction, ≥1 contract correction)
- `docs/adr/ADR-000N-<slug>.md` with real options and consequences
- Commit hash + `git status` proof

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Mermaid doesn't render | Syntax slip (quotes inside node labels) | Wrap labels in quotes `["..."]`; preview in markdown or mermaid.live |
| Agent invents services not in the repo | Prompt didn't require citations | Re-run: "cite real paths; do not invent components no AC needs" |
| Diagram becomes a novel | All components + all flows | Cap at 8–12 boxes; this is a lightweight first pass for review |
| Contract adds endpoints/fields "for later" | Gold-plating | Remove anything untraced to an AC; add via spec change if truly needed |
| ADR has one option | Decision was assumed, not evaluated | Ask for two realistic alternatives with real trade-offs |
| Contract contradicts the spec | Spec ambiguity or agent drift | The **spec wins** — fix the contract; if the spec is genuinely ambiguous, that's a versioned spec change (Lab 9.3 Step 6) |

---

## Checkpoint questions

1. Why keep the architecture diagram as Mermaid source instead of an exported image?
2. What are the five sections of an ADR?
3. If the contract and the spec conflict, which is the source of truth — and what do you do about it?

<details>
<summary>Answers</summary>

1. Text artifacts diff, review, and version-control like code — an image is a binary frozen outside review, so the diagram would silently drift from the spec (guide §5).
2. Title, Context, Options considered, Decision, Consequences (guide §6).
3. The spec — it's the approved source of truth. Fix the contract to match; if the spec itself is ambiguous, raise a versioned spec change (new version + change-log entry) and flag the linked artifacts for re-validation. Never silently "fix" the contract to diverge.

</details>

---

## Next

**Lab 9.3** — Plan mode against the approved spec, one revision cycle, the plan approval gate, the first implementation pass, and the AC → code → test traceability matrix.

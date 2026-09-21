# Lab 14.4 — SOC2/GDPR Source Review *(optional extension)*

**Module 14 · Governance, Security & Observability | Xebia — Cursor AI Training**
Day 4 · Optional extension · ~8 minutes · Individual or pairs

> **Objective:** apply the two named frameworks to real sources. For every source in the inventory, check the
> SOC 2 and GDPR questions, decide approve / redact / exclude / restrict, and note what the decision changes
> about logging — including the erasure implications of logs and embeddings.

**Guide references:** Module 14, §4 (compliance considerations), §7 (approved vs. restricted)
**Learning objectives covered:** 4 — apply SOC2/GDPR considerations to grounded agent design; 7 — restricted source policy.

---

## Before you start

- Lab 14.1 complete: inventory reviewed, compliance cases flagged
- Open [`samples/source-inventory.md`](samples/source-inventory.md)
- No runner needed

---

## Step 1 — Run the checklist per source

| Source | SOC 2: is access scoped + audited? | GDPR: personal data? lawful basis? retention? | Flag |
|---|---|---|---|

Two framework questions to keep explicit (deck §04):

- **SOC 2** — access control and a complete audit trail must cover the agent's tool use, not just human access.
- **GDPR** — personal data in grounding sources needs lawful handling; logs and embeddings that reference it are themselves subject to erasure.

- [ ] Every source from the inventory checked on both axes
- [ ] The defect log's **reporter emails** flagged (personal data with no handling decision yet)
- [ ] The support ticket export flagged: personal data with **no lawful basis or retention defined**
- [ ] HR wiki and legal contracts flagged as restricted (personal data / IP)
- [ ] Vendor docs pass both axes

---

## Step 2 — Decide per flagged source

| Source | Decision (approve / redact / exclude / restrict) | Who approves | What changes in logging |
|---|---|---|---|

- [ ] Each flagged source has one decision, a named approver, and a logging consequence
- [ ] The erasure question answered for at least one source: if a person asks for erasure, can their data be found in **logs or embeddings** — and removed?
- [ ] Redaction is named where it is the chosen path (e.g., strip reporter emails before connection) rather than "be careful"

---

## Step 3 — Write the review

Create `shared-agent-library/governance/compliance-review.md` with the two tables and one closing sentence: which control from Labs 14.1–14.3 satisfies which framework requirement (SOC 2 ← admin controls + audit log; GDPR ← classification at connection time + erasure-aware logging).

- [ ] Review written and added to the `AGENTS.md` governance index

---

## Evidence

- Checklist table (both frameworks, every source)
- Decision table with approvers and logging consequences
- `shared-agent-library/governance/compliance-review.md`

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| "Personal data" treated as one category | Missing the handling decision | Every personal-data source needs approve/redact/exclude + approver |
| Erasure considered only for the source | Logs and embeddings forgotten | Logs/embeddings referencing personal data are in scope too — say how they'd be found and removed |
| Compliance handled as a separate checklist | Framework-as-bolt-on thinking | Point the same controls at the regulation: scoping + audit satisfy SOC 2; classification + erasure-aware logging satisfy GDPR |
| Redaction left vague | "Be careful" isn't a control | Name the mechanism and the layer that enforces it |

---

## Checkpoint questions

1. Why do SOC 2 and GDPR both land on controls this module already requires?
2. What does the "right to erasure" demand of logs and embeddings, specifically?

<details>
<summary>Answers</summary>

1. SOC 2 wants scoped access plus a complete audit trail — which is exactly the admin controls and audit logging from §2. GDPR wants lawful, limited handling of personal data — which is exactly the connection-time classification and restricted-source policy from §1/§7. Compliance is the same controls pointed at a regulation.
2. That personal data in logs or embeddings can be located and removed on request — so logging and grounding design must account for finding and deleting it, not just recording it.

</details>

---

## Next

**Module 15 — Subagents & Orchestration Patterns Overview** opens Day 5: individual governed agents start chaining into sequential and parallel pipelines, and this module's trace id and handoff-log discipline become the backbone of debugging across every handoff.

# Lab 14.3 — Trace the Handoffs and Cost

**Module 14 · Governance, Security & Observability | Xebia — Cursor AI Training**
Day 4 · Lab 3 of 3 · ~8 minutes · Individual or pairs

> **Objective:** make a multi-agent task reconstructable. Repair a flawed handoff log so one trace id threads
> every stage, define the fields every handoff must emit, then put a number on the task: tokens, tool calls,
> wall-clock time, and cost — per stage and per task.

**Guide references:** Module 14, §5 (tracing and handoff logging), §6 (cost visibility)
**Learning objectives covered:** 5 — design tracing/logging across a pipeline; 6 — cost visibility per call/task.

---

## Before you start

- Labs 14.1–14.2 complete: policy, approval checkpoint, audit-log schema written
- Open [`samples/pipeline-trace-and-cost.md`](samples/pipeline-trace-and-cost.md)
- No runner needed

---

## Step 1 — Find what the trace is missing

Read Part A entry by entry. For each problem, say why it matters and how to fix it:

| Entry | Problem | Why it matters | Fix |
|---|---|---|---|

- [ ] Missing **trace id** identified where the chain breaks (entries 1–2)
- [ ] Missing **sources_used** identified (every entry) — grounding can't be verified after the fact without it
- [ ] The **verbatim input** flagged: full raw text stored instead of an input summary/hash (retention/GDPR exposure)
- [ ] The misplaced **guardrail event** flagged: it belongs as a field on the stage entry, not a mystery duplicate
- [ ] Missing **cost** field flagged on every entry

---

## Step 2 — Define the handoff-log schema

Create `shared-agent-library/governance/handoff-log-schema.md` — the same fields at **every** handoff:

```text
trace_id:           <one id for the whole task>
stage / agent:      <which agent produced this entry>
input_summary:      <summary or hash — never the full payload>
sources_used:       <citations from Module 13's discipline>
output_summary:     <what was produced>
guardrail_triggered: none | <which guardrail fired>
timestamp:          <ISO-8601>
cost:               <tokens + tool calls + $ for this stage>
```

- [ ] All eight fields present; input is a summary/hash, not the payload
- [ ] One sentence: why this shape is **queryable** ("which stages cited DEF-118?", "which stage cost the most?") rather than just readable
- [ ] One sentence: what a shared trace id preserves that per-call logs lose

---

## Step 3 — Rewrite the worst entry

- [ ] Entry 1 rewritten correctly with all eight fields — trace id added, input summarized/hashed, sources listed, guardrail field present, cost included
- [ ] The validation stage now carries its guardrail event as a field (entry 4 folded in)

---

## Step 4 — Put a number on the task

Using Part B and the rate card ($6 per 1M tokens blended · $0.001 per tool call):

| Stage | Tokens | Token $ | Tool-call $ | Stage total $ |
|---|---|---|---|---|

- [ ] Per-stage totals computed; task total computed (tokens, tool calls, wall-clock, $)
- [ ] The **most expensive stage** identified with a one-line why
- [ ] One concrete decision that would reduce the task cost (tie it to Module 12 scoping or fewer calls), and the rough saving
- [ ] One sentence: why cost visibility matters most once agents chain (deck §07)

Create `shared-agent-library/governance/cost-estimate.md` with the table and totals.

---

## Evidence

- Gap table (per-entry problems with fixes)
- `shared-agent-library/governance/handoff-log-schema.md`
- Corrected entry 1 (with the guardrail field folded into validation)
- `shared-agent-library/governance/cost-estimate.md` — per-stage and task totals + the reduction decision

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Trace "works" because stages are in order | Order isn't identity | One trace id across every entry — ordering breaks the moment tasks interleave |
| Input stored verbatim "for debugging" | Retention exposure ignored | Summary or hash; full payloads are subject to erasure and review |
| Cost only tracked per task | Stage attribution missing | Per-stage cost is what tells you which agent to fix — Module 21 builds ROI on it |
| Guardrail event logged as its own stage | Schema doesn't have the field | Fold it in as `guardrail_triggered` on the stage that fired it |
| Tool calls left out of cost | Only tokens counted | Every MCP Tool call has its own cost/latency — include it |

---

## Checkpoint questions

1. Name three fields a handoff log must carry and why each matters.
2. Why is a shared trace id necessary once more than one agent is involved?
3. Why does cost need per-call and per-stage visibility, not just a task total?

<details>
<summary>Answers</summary>

1. Any three of: trace id (ties the task together), input summary/hash (reconstruct context without storing everything), sources used (verify grounding after the fact), output summary, guardrail-triggered (did a control fire?), timestamp (order events), cost (attribute spend per stage).
2. Without it, a failure in a later stage looks unrelated to what an earlier agent received — the chain of cause and effect is invisible in per-call logs. One trace id reconstructs the whole task end to end.
3. A task total tells you something is expensive; per-call and per-stage numbers tell you *where* — which agent, which call, which oversized context — so you can fix the cause instead of guessing.

</details>

---

## Next

**Lab 14.4 (optional) — SOC2/GDPR Source Review.** Apply both frameworks to the source inventory and decide what stays connected, what gets redacted, and what is excluded — with erasure-aware logging. Then Day 4 closes; Module 15 opens Day 5 with pipelines that assume all of this is in place.

# Lab 11.2 — Package the Shared Library and Add One Focused Subagent

**Module 11 · Use Case Lab 1: Reusable Agents, Prompts & Skills Framework | Xebia — Cursor AI Training**
Day 3 · Lab 2 of 4 · ~20 minutes · Individual

> **Objective:** finish the library so it is discoverable and reusable — agents, templates, rules, and skills in
> one structure with an index — then carve out **one** task that is genuinely independent and define it as a
> subagent. The delegation must earn its place (Module 10 §7): justify it in one sentence or fold it back.

**Guide references:** Module 11, §3 (shared, version-controlled library), §4 (focused subagent)
**Learning objectives covered:** 3 — package rules and skills into a shared library; 4 — create and justify a focused subagent.

---

## Before you start

- Lab 11.1 complete: four `agents/*.agent.md` and four `templates/*.prompt.md` in `shared-agent-library/`
- Module 8 assets available: your `.cursor/rules/*.mdc`, `.cursor/skills/<skill-name>/SKILL.md`, and repo `AGENTS.md`
- Read Module 10's sample annotations if you kept them (`notes/module10/sample-annotations.md`) — especially the isolation test and the flagged over-decomposition

---

## Step 1 — Complete the library layout

Target structure (guide §3; `skills/` and `rules/` hold **canonical** definitions):

```text
shared-agent-library/
├── agents/            # 4 role definitions
├── subagents/         # 1 focused subagent
├── templates/         # 4 parameterized prompt templates
├── skills/            # canonical copy of the reusable skill(s)
├── rules/             # canonical copies of repo-specific rules (*.mdc)
├── reviews/           # peer-review records (Lab 11.4)
├── testing/           # pass/fail evidence (Lab 11.3)
└── AGENTS.md          # library index + onboarding
```

- [ ] Directories created; `agents/` and `templates/` already populated from Lab 11.1
- [ ] Copy your Module 8 rule(s) into `rules/` and skill into `skills/` as canonical assets
- [ ] **Sync direction documented** in `AGENTS.md`: state which copy is the source of truth (the library) and where Cursor actually loads them from (`.cursor/rules/`, `.cursor/skills/`) — and how the two are kept in sync (copy step, script, or symlink). Pick one approach and be consistent

---

## Step 2 — Write the library index

`shared-agent-library/AGENTS.md` is the library's onboarding and index — distinct from the repo-root `AGENTS.md` (Module 8). It must let a teammate (or a future lab) find and trust each asset without asking you:

```markdown
# Shared agent/skill library — index

| Asset | Path | Version | Status | Owner | Loaded from |
|---|---|---|---|---|---|
| Requirement Analysis agent | agents/requirement-analysis.agent.md | 0.1.0-draft | draft | <you> | — |
| … | | | | | .cursor/rules/… / .cursor/skills/… |
```

- [ ] All assets listed (4 agents, 4 templates, 1 subagent, rules, skills)
- [ ] Every row names version, status, owner, and (for rules/skills) the active load location
- [ ] Sync direction and the passing/failing call table from Lab 11.1 live here or are linked from here

---

## Step 3 — Right-level check: repo rule or team skill?

For each Module 8 asset you are packaging, confirm the level (Module 10 §5). Reuse your Lab 10.1 analysis rather than re-deriving it.

| Asset | Home (repo rule / team skill) | Scope argument | Cadence argument |
|---|---|---|---|
| | | | |

- [ ] Every packaged rule/skill has a home and a one-line justification
- [ ] Anything you moved differs from your Lab 10.1 answer **for a stated reason** — note it

---

## Step 4 — Choose the focused subagent and justify it

Apply the isolation test from guide §4: **could this task run correctly with no visibility into the other agents' conversations at all?** If yes, it's a subagent candidate. If it needs that context, it belongs inside a main agent.

Default from the deck: the **Documentation Agent delegates "summarize the API surface"** — the subagent sees only the target module's public API and returns the summary. Alternatives: changelog-entry generation, security-guardrail check.

- [ ] `<independent-task>` chosen; one sentence stating **why subagent, not folded into the parent**
- [ ] One sentence stating what it deliberately **cannot** see (parent context, requirement discussion, other findings)
- [ ] One counter-check: name what would disqualify it (i.e., if it needed the parent's context, it would move back into the parent)

---

## Step 5 — Define the subagent

Create `shared-agent-library/subagents/<subagent-name>.subagent.md` with the same discipline as Lab 11.1, plus the boundary made explicit:

| Slot | Requirement |
|---|---|
| **Delegated by** | The parent agent (update that agent's `Delegation` section to point here) |
| **Role** | One sentence, narrow |
| **Inputs (IN)** | Only what crosses the isolation boundary — name and shape |
| **Tools** | Least privilege; often none |
| **Guardrails** | At least one; include "return only the structured result" |
| **Outputs (OUT)** | Structured result schema the parent consumes mechanically + failure shape |

- [ ] `subagents/<name>.subagent.md` complete; parent's `Delegation` section updated
- [ ] IN/OUT lists are exhaustive — nothing smuggled in from the parent's context
- [ ] The parent could consume the OUT schema without a human translating it (Module 16 will do exactly that)

---

## Step 6 — Set the version plan

- [ ] Assets stay `0.1.0-draft` until Lab 11.3 testing passes
- [ ] After Lab 11.3 fixes, bump to `0.2.0` (record what changed); after peer approval (Lab 11.4), adopt at `1.0.0`
- [ ] The **library release tag** is `v0.1.0` at commit (per the deck); if review changes the artifact, the fix commit gets `v0.1.1`
- [ ] Version plan recorded in `AGENTS.md`

---

## Evidence

- Completed `shared-agent-library/` tree with rules/skills canonical copies + documented sync direction
- `shared-agent-library/AGENTS.md` — index with version/status/owner/load locations
- `subagents/<subagent-name>.subagent.md` + updated parent `Delegation` section
- Justification sentences for the subagent (why subagent; what it can't see; what would disqualify it)

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Rules/skills duplicated and drifting | Two sources of truth | State one canonical location (the library) and one load location (`.cursor/`), then document the sync step |
| Subagent needs "the whole conversation" | Wrong candidate — not genuinely independent | Fold it back into the parent agent; pick a task that passes the isolation test |
| Subagent output is prose | Contract skipped | Define the OUT schema the parent consumes; add a failure shape |
| Library index is stale already | Index written from memory | Generate it from the files you actually created; check paths resolve |
| "Just in case" extra delegation | Over-decomposition (Module 10 §7) | One subagent, justified; price the handoff before adding another |
| Version numbers meaningless | No plan | Apply Step 6: 0.1.0-draft → 0.2.0 tested → 1.0.0 adopted; library tag v0.1.0 |

---

## Checkpoint questions

1. Why do rules and skills need one canonical location and one load location — and what breaks if that isn't documented?
2. What's the test for whether a task deserves subagent status?
3. Why does the parent agent need its `Delegation` section updated when a subagent is added?

<details>
<summary>Answers</summary>

1. Rules/skills are copied into the shared library for reuse, but Cursor only loads them from `.cursor/rules/` and `.cursor/skills/`. Without a documented source of truth and sync step, the two copies drift and the team can't tell which behaviour is actually active.
2. Whether it can run correctly with **no visibility** into the other agents' context. If it can, it's a good subagent candidate; if it needs the shared context, it belongs inside a main agent.
3. Because the delegation is part of the parent's own contract: the parent's definition must say what it hands off, to whom, and what structured result comes back — otherwise the boundary is invisible and Module 16's chaining can't be built or debugged.

</details>

---

## Next

**Lab 11.3 — Test Each Asset Independently Against Sample Inputs.** The library now exists; nothing is trusted yet. You'll run all five agents and one template against the shipped samples, catch a deliberate contract mismatch, and log pass/fail evidence.

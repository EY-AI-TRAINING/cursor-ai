# Lab 14.1 — Write the Access Policy

**Module 14 · Governance, Security & Observability | Xebia — Cursor AI Training**
Day 4 · Lab 1 of 3 · ~10 minutes · Individual or pairs

> **Objective:** turn the control-plane model into written policy. Review a deliberately flawed draft, then
> produce `governance/access-policy.md` covering the four decisions every rollout makes once: approved vs.
> restricted sources, restricted file/folder access, secrets handling, and where observability data lands —
> plus who grants access and how sources are classified at connection time.

**Guide references:** Module 14, §1 (data privacy/IP), §2 (admin controls and audit), §7 (approved vs. restricted, secrets, tooling)
**Learning objectives covered:** 1 — privacy/IP handling for connected sources; 2 — admin controls and access scoping; 7 — approved vs. restricted sources, restricted paths, secrets handling.

---

## Before you start

- Module 13 complete on `module13-lab`: the `knowledge-grounded` agent, `agents/knowledge-grounded.retrieval-scope.yaml`, `.cursor/mcp.json`, `knowledge/` corpus
- Create `shared-agent-library/governance/` (new home for Module 14's policy artifacts)
- Open [`samples/access-policy-draft.md`](samples/access-policy-draft.md) and [`samples/source-inventory.md`](samples/source-inventory.md)
- This lab needs no runner — it is a design exercise

---

## Step 1 — Review the draft against the four decisions

Read the draft and list every problem it has. Expect **at least six**. For each, say why it fails and how the policy should read instead:

| # | Problem in the draft | Why it fails | Corrected wording |
|---|---|---|---|

Use the four policy decisions as your review lens (deck §08):

| Decision | What a correct policy must state |
|---|---|
| **Approved vs. restricted sources** | An explicit allow-list of connectable sources; anything not listed is unreachable **by default** |
| **Restricted file/folder access** | Deny patterns (credentials, `.env`, personal data stores, `/legal`, `/hr`) enforced at the **tool-permission layer**, not by convention |
| **Secrets handling** | Secrets never enter agent context, prompts, or logs — injected at execution time from a vault |
| **Observability tooling** | One destination where traces, handoff logs, and cost data land — not four disconnected places |

- [ ] At least six problems identified, each with a corrected wording
- [ ] You can name which problems are policy *inversions* (draft says the opposite of the correct control) vs. omissions

---

## Step 2 — Write the corrected policy

Create `shared-agent-library/governance/access-policy.md` for the `knowledge-grounded` agent:

- [ ] **Approved sources** — explicit allow-list drawn from the inventory's connected + approved rows; a sentence stating that anything unlisted is restricted by default
- [ ] **Restricted paths** — deny patterns (e.g., `~/.aws/credentials`, `.env`, `/legal`, `/hr`, personal data stores) and a sentence that they are enforced at the tool-permission layer, regardless of who asks
- [ ] **Secrets** — never in context, prompts, or logs; vault-injected at execution time only; config files reference `${env:...}`, never literals
- [ ] **Approval boundary** — retrieval (read-only) is not approval-gated; **execution** (state-changing tool calls) is gated by permission, sandboxing, and approval per risk
- [ ] **Admin controls** — access is granted by admins, scoped per team/project, and every grant and use is logged; developers do not self-serve connections
- [ ] **Classification** — every source classified at **connection time** (public / internal / IP-restricted; personal data flagged), not at retrieval time
- [ ] **Observability destination** — one named place for traces, handoff logs, and cost data

---

## Step 3 — Apply it to the agent

- [ ] Update `agents/knowledge-grounded.retrieval-scope.yaml`'s `deny` list so it matches the policy's restricted paths — note what changed
- [ ] Add a `governance/` row to `shared-agent-library/AGENTS.md` (owner, version, status)
- [ ] Confirm `.cursor/mcp.json` still contains no secrets and is scoped to `${workspaceFolder}/knowledge` — the policy is not real until the config obeys it

---

## Step 4 — Flag the compliance cases (full review is Lab 14.4)

- [ ] In the inventory, mark every source with personal data or IP restrictions
- [ ] One line each: what special handling the flagged sources need before they can stay connected

---

## Evidence

- Problem table (≥6 findings with corrected wording)
- `shared-agent-library/governance/access-policy.md`
- Updated `retrieval-scope.yaml` + `AGENTS.md` governance row
- Compliance flags on the inventory

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Policy reads as advice ("should avoid") | Draft's convention-based style carried over | Rewrite as controls: allow-list, deny patterns, enforced at a named layer |
| Secrets clause says "don't commit tokens" | Missing the stronger rule | Secrets never enter context, prompts, or **logs** — vault at execution time |
| Approval applied to retrieval | Module 12 §7 boundary lost | Retrieval is read-only and low-risk; gate the execution side |
| Policy written but config unchanged | Policy treated as documentation | Align `retrieval-scope.yaml` and `.cursor/mcp.json` — a policy the config contradicts is not a control |
| Everything labeled internal | No classification pass | Classify at connection time; personal data and IP-restricted sources get explicit handling |

---

## Checkpoint questions

1. Why must the privacy/IP check happen at connection time rather than at retrieval time?
2. What makes an allow-list with default-restricted behavior stronger than a deny-list?
3. Why are secrets injected at execution time instead of being available in context?

<details>
<summary>Answers</summary>

1. By the time a retrieval runs, the source is already reachable — deciding then is too late. Connection time is the last point where the organization still controls whether the content can ever enter a prompt, a log, or a model call.
2. A deny-list only blocks what someone thought of; anything forgotten is allowed. Default-restricted flips the burden: a source must be explicitly approved to exist, so omissions fail closed.
3. Context and logs may be retained, reviewed, or surfaced elsewhere — a secret that enters either is effectively exposed beyond its intended use. Execution-time injection from a vault keeps the secret out of everything that gets stored.

</details>

---

## Next

**Lab 14.2 — Gate the Risky Call and Log It.** Execution is the side that needs gates. You'll classify nine tool calls, run the riskiest through the four-control stack, define its approval checkpoint, and design the audit-log entry it produces.

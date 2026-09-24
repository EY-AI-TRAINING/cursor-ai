# Lab 19.4 — Git Workflow for Agent-Generated Artifacts

**Xebia — Cursor AI Training | AI-Assisted Software Engineering**
Day 6 · Module 19 · Lab 19.4 of 8 · ~6 min · Concept demo + hands-on (individual or pairs)

> **Objective:** make the agent's output follow the team's Git workflow, with the additions agent work
> needs: one branch per ticket, small logical commits with squashed correction rounds, provenance
> trailers, evidence committed but noise excluded, and the control plane owned by humans. The PR is the
> review surface — CODEOWNERS decides who must look.

**Guide reference:** §4 Git Workflow Integration (Branches, Commits, PRs) for Agent-Generated Artifacts · §9 task 4
**Learning objectives covered:** 4 (branches, commit granularity, trailers, PR templates, code owners)

## Before you start

| Need | Notes |
|---|---|
| Lab 19.3 complete | Branch `feat/REQ-2481-order-cancel` with a trailed commit |
| Draft to critique | [`samples/codeowners-draft.txt`](samples/codeowners-draft.txt) |
| Files you will create | `CODEOWNERS`, `.github/pull_request_template.md`, the commit plan and branch-protection table in `notes/module19/git-workflow.md` |
| Defaults | Decision packet at `runs/req-2481-run-02/decision_packet.md`; PR `#57` |

---

## Steps

### Step 1 — Critique the draft CODEOWNERS (≥6 problems)

Read [`samples/codeowners-draft.txt`](samples/codeowners-draft.txt). For each problem:
*problem → risk → correct ownership*. The draft covers four paths; the control plane has more.

| Path | Who must own it | Why |
|---|---|---|
| `/gates.yaml`, `/tools/`, `/schemas/` | `@org/qa-platform` | The rules the agents are judged by — agents must not be able to relax them |
| `/.cursor/` | `@org/qa-platform` + `@org/security` | Hooks, agents, MCP config — the agent's own permissions live here |
| `/.github/` | `@org/platform` + `@org/security` | Workflow tampering skips every gate at once |
| `/tests/` | `@org/orders-team` | Generated tests are reviewed by the owning service team |
| `*` (catch-all) | A team, or omit | One individual owning everything is a bus factor of one |

### Step 2 — Write the real `CODEOWNERS`

```text
# Humans who own the rules the agents are judged by
/gates.yaml            @org/qa-platform
/tools/                @org/qa-platform
/schemas/              @org/qa-platform
/.cursor/              @org/qa-platform @org/security
/.github/              @org/platform @org/security
# Generated tests are reviewed by the owning service team
/tests/                @org/orders-team
```

- [ ] Every control-plane path is owned by a **team**, not an individual
- [ ] `.cursor/` and `.github/` include `@org/security`
- [ ] No catch-all that funnels everything to one person
- [ ] Coverage check: `grep -E "gates.yaml|tools/|schemas/|\.cursor/|\.github/|tests/" CODEOWNERS` shows all six

### Step 3 — PR template and the PR description

Create `.github/pull_request_template.md` with: **Ticket** (ID + link + bundle revision), **What changed
and why** (drafted from `decision_packet.md`), **Traceability** (AC → tests → result → gate trail),
**Evidence** (run folder, gate log, packet, readiness report), and **Agent involvement** (generated-by,
rounds, human approver, control-plane unchanged, known defects linked).

- [ ] Draft the PR body from the decision packet — the packet is the source; the template forces the sections
- [ ] PR title `REQ-2481: order cancellation tests` (the check in Lab 19.5 will verify the pattern)
- [ ] The agent-involvement section names the human approver — never "the reviewer agent approved"
- [ ] Known defects: DEF-5520 linked and handled per policy (Lab 19.6)

### Step 4 — Commit discipline and branch protection

- [ ] **Commit plan** (in `notes/module19/git-workflow.md`): tests in one commit (correction rounds
      squashed), run evidence in a second, docs in a third — not one commit per agent round
- [ ] Evidence committed, noise excluded: `gate_log.jsonl`, `findings/`, `decision_packet.md`,
      `traceability.md` in; caches, full transcripts, large raw logs, and anything from `creds/` out
- [ ] `.gitattributes` marks bulky evidence `linguist-generated` so reviewer diffs stay readable
- [ ] **Branch-protection table** (design it even if you cannot configure the sandbox repo):

| Setting | Value | Why |
|---|---|---|
| Required reviews | ≥1 human, from CODEOWNERS | No self-merge; agent PRs never auto-merge |
| Required status checks | `gates` (and `readiness`) | CI is the independent verifier |
| Dismiss approvals on new commits | On | A fix-up invalidates the old review — and the old approval hash |
| Force-push / bypass | Disabled, no bot bypass | History is evidence |
| Branch name pattern | `feat/REQ-*`, `agent/REQ-*` | Traceability check can rely on it |

---

## Evidence

- `CODEOWNERS` + coverage-check output
- `.github/pull_request_template.md` + the drafted PR body (from the decision packet)
- Commit plan + `.gitattributes` + branch-protection table in `notes/module19/git-workflow.md`
- Draft critique: ≥6 problems with risks

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| CODEOWNERS "not working" | Paths are case-sensitive and patterns anchor differently (`/tools/` vs `tools/`) | Anchor with leading `/` for repo-root paths; verify in the GitHub UI or a linter |
| PR body still contains a transcript | Copied from the run folder | The packet summarizes; link the transcript, never paste it (Module 18 rule) |
| Evidence commit huge | Raw logs and caches included | Commit logs/JSONL/packet; exclude caches and transcripts; mark bulky files generated |
| Agent PR auto-mergeable | Auto-merge enabled for the repo/app | Disable it for agent PRs; required human review is the control |

## Checkpoint questions

<details>
<summary>Why does the control plane need human owners when the agents "only" generate tests?</summary>

Because the control plane decides what the agents are allowed to do and what counts as passing. An agent
that can edit `gates.yaml`, `tools/`, or `.github/` can relax its own evaluation — the Module 17 tamper
rule in Git form. CODEOWNERS makes that a review requirement instead of a policy statement.
</details>

<details>
<summary>Why squash correction rounds before the PR?</summary>

Each round is an internal step of one logical change; keeping them as separate commits makes the PR
history noisy and exposes failed attempts without adding review value. The correction evidence lives in
`findings/` and the gate log, where it belongs — the Git history stays meaningful.
</details>

<details>
<summary>What should happen when a fix-up commit lands on an approved PR?</summary>

Approvals are dismissed on new commits (branch-protection setting), and in this pipeline the approval
hash no longer matches the tests, so the commit guard refuses too. The reviewer re-reviews the delta and
re-approves; the readiness gate only accepts a matching hash.
</details>

---

*Next: Lab 19.5 — CI: Independent Re-verification + AI Review Guardrails, where the workflow replays the gates on a clean runner.*

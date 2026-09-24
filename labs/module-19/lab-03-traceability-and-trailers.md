# Lab 19.3 — Carry the Key: Traceability Conventions + Commit Trailers

**Xebia — Cursor AI Training | AI-Assisted Software Engineering**
Day 6 · Module 19 · Lab 19.3 of 8 · ~6 min · Concept demo + hands-on (individual or pairs)

> **Objective:** extend Module 16's traceability chain across systems. The ticket ID plus AC-IDs plus
> run ID must travel from the ticket to the readiness report — and **every hop has a check**, because
> conventions nobody checks decay within a sprint. Commit trailers make the chain machine-readable:
> the report is generated from Git, not typed by hand.

**Guide reference:** §3 Maintaining Traceability from Ticket → Plan/Spec → Commit → Test → Report · §9 task 3
**Learning objectives covered:** 3 (cross-system traceability) · 4 (commit trailers)

## Before you start

| Need | Notes |
|---|---|
| Bundle from Lab 19.2 | `runs/req-2481-run-02/00_requirement_bundle.json` |
| Flawed excerpt | [`samples/commit-excerpt-flawed.txt`](samples/commit-excerpt-flawed.txt) |
| Files you will create | the conventions table in `notes/module19/traceability.md`, `tools/check_trace_conventions.py`, the branch and a trailed commit |
| Defaults | branch `feat/REQ-2481-order-cancel`; run `req-2481-run-02` |

---

## Steps

### Step 1 — Critique the flawed excerpt (≥5 violations) and write the conventions table

Read the excerpt: branch name, six commits, one `git show --stat`, two empty trailer queries. For each
violation: *violation → why it breaks the chain → correct convention*.

- [ ] Fill the conventions table for **every hop** — the key's location and its check:

| Link | Convention (where the key goes) | Checked by |
|---|---|---|
| Ticket → bundle | `ticket.id`, `ticket.revision` | Bundle schema (Lab 19.2) |
| Bundle → plan/spec | Header: `Ticket: REQ-2481 · rev <revision>`; ACs copied by ID | G1 (every bundle AC appears in the spec) |
| Plan/spec → branch | `feat/REQ-2481-<slug>` | CI branch-name regex |
| Branch → commits | Trailers: `Ticket:`, `Run-Id:`, `Generated-by:`, `Approved-by:` | CI commit-message lint |
| Commit → PR | PR title `REQ-2481: …`; body links ticket, run folder, decision packet | PR-title check + template |
| Test → AC | `@pytest.mark.req(...)`, `@pytest.mark.ac(...)` | G3 `markers_present`, `ac_coverage_complete` |
| Result → report | `readiness_report.md` lists AC → test → result → gate trail | Readiness gate (Lab 19.6) |
| Report → ticket | Comment/remote link to PR + report (**human-approved MCP write**) | Hook `ask` (Lab 19.1) |

### Step 2 — Create the branch and commit with trailers

```bash
git switch -c feat/REQ-2481-order-cancel
# stage the work from Module 18: tests, runs/req-2481-run-02/, tools, gates.yaml
git add tests/ runs/req-2481-run-02/ tools/ gates.yaml
git commit -m "$(cat <<'EOF'
test(orders): add REQ-2481 order cancellation API tests

Covers AC-1..AC-4 from the requirement bundle (ticket rev 2026-09-24T08:12:03Z).
AC-3 is marked xfail(strict) against DEF-5520 (API returns 404 where spec requires 403).

Ticket: REQ-2481
Run-Id: req-2481-run-02
Generated-by: cursor-agent/test-generator@1.3.0
Approved-by: qa-lead (gate_log HITL_signoff)
EOF
)"
```

- [ ] Branch matches `feat/REQ-2481-<slug>` — the check in the conventions table can actually run
- [ ] One logical commit for the tests (correction rounds squashed — see Lab 19.4)
- [ ] Trailers present and machine-readable:

```bash
git log -1 --format='%(trailers:key=Ticket)'
git log -1 --format='%(trailers:key=Run-Id)'
```

### Step 3 — Build the checker

Write `tools/check_trace_conventions.py` (stdlib) with three checks the CI will run in Lab 19.5:

| Check | Rule |
|---|---|
| Branch name | `^(feat\|fix\|agent)/REQ-\d+-[a-z0-9-]+$` for the current branch (or `--branch`) |
| Commit trailers | Every non-merge commit since `--base` carries `Ticket:` matching the branch's ticket and a `Run-Id:` |
| AC references | The commit body or PR title references at least one `AC-\d` (warning, not failure) |

- [ ] Run it against the flawed excerpt's facts (branch `req2481-fix`, no trailers) → **fails with a specific reason**
- [ ] Run it on your real commit → **passes**
- [ ] Record both outputs in `notes/module19/traceability.md`

### Step 4 — Prove the chain end to end

- [ ] `git log --format='%(trailers)'` shows Ticket + Run-Id on the real commit and nothing on the excerpt
- [ ] The ticket ID appears in: bundle, branch, commit, test file marker, run folder — five of the eight hops, checked where they exist
- [ ] Note which hops have **no automated check yet** (PR title, report link) — Lab 19.5's CI adds two of them

---

## Evidence

- Conventions table + violation list in `notes/module19/traceability.md`
- Branch `feat/REQ-2481-order-cancel` + the trailed commit
- `tools/check_trace_conventions.py` + red (excerpt facts) → green (real commit) outputs
- Trailer query output

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Trailers don't parse | Blank line missing before the trailer block | Trailers must be the last paragraph; keep one blank line after the body |
| `%(trailers:key=Ticket)` prints nothing | Key case differs | Keys are case-sensitive; use `Ticket` exactly |
| Checker passes the excerpt | Rules not actually implemented | Test the checker against the excerpt's facts before trusting it |
| Branch check fails on `agent/` branches | Regex only allows `feat/` | Include `agent/` — cloud agents create their own prefix (Lab 19.7) |

## Checkpoint questions

<details>
<summary>Name four places the ticket ID appears between the ticket and the readiness report, and how each is checked.</summary>

Examples: the bundle (`ticket.id`, schema-checked); the branch name (CI regex); commit trailers (commit
lint); the PR title (PR check); test markers (G3 `markers_present`); the readiness report (generated from
the bundle and results). Any four with their checks are correct.
</details>

<details>
<summary>Why trailers instead of putting the ticket ID in the commit subject?</summary>

Trailers are machine-readable: `git log --format='%(trailers:key=Ticket)'` extracts them without
parsing prose, so reports and checks can be generated from Git. The subject stays readable for humans;
the trailers carry the structured provenance.
</details>

<details>
<summary>Why is "the developer remembers to reference the ticket" not a control?</summary>

It is a convention without a check. Conventions that nobody verifies decay within a sprint — the
traceability chain silently breaks at the first rushed commit. Each hop needs a mechanism that fails
when the key is missing.
</details>

---

*Next: Lab 19.4 — Git Workflow for Agent-Generated Artifacts, where CODEOWNERS, the PR template and commit discipline protect the control plane.*

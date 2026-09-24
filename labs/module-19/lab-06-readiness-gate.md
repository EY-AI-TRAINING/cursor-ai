# Lab 19.6 — Deployment-Readiness Gate: Policy Over Evidence

**Xebia — Cursor AI Training | AI-Assisted Software Engineering**
Day 6 · Module 19 · Lab 19.6 of 8 · ~8 min · Concept demo + hands-on (individual or pairs)

> **Objective:** answer "is this change safe to promote?" — which is **not** the same as "tests passed".
> Aggregate evidence from every earlier control (CI, pipeline gates, hash-bound sign-off, AC coverage,
> known defects, security) under an explicit **versioned policy**, and produce a report a human can
> approve against. Prove the known-defect policy works in both directions, and that an unevaluable
> criterion fails safe.

**Guide reference:** §6 Automated Deployment-Readiness Gates · §9 task 6
**Learning objectives covered:** 6 (readiness gates from CI results, pipeline gates, approvals, defect policy)

## Before you start

| Need | Notes |
|---|---|
| Labs 19.2–19.5 outputs | Bundle (AC coverage source), gate log + approval, CI simulation, workflow |
| Drafts to critique | [`samples/readiness-draft.yaml`](samples/readiness-draft.yaml) · [`samples/readiness-report-draft.md`](samples/readiness-report-draft.md) |
| Files you will create | `readiness.yaml`, `tools/readiness.py`, `reports/readiness_report.md` (two runs) |
| Known defect | DEF-5520, currently a failing test in the signed-off suite; the xfail conversion is Step 3 |

---

## Steps

### Step 1 — Critique the draft policy and report (≥6 problems total)

Record *problem → consequence → correct rule* in `notes/module19/readiness-review.md`.

| Ask yourself (policy) | Ask yourself (report) |
|---|---|
| `on_unknown: READY` — what happens when a criterion can't be evaluated? | Does the report claim READY from "all tests passed" alone? |
| Is the human sign-off **hash-bound**? | Where is the gate trail (G1–G5, rounds)? |
| Does AC coverage read the **bundle** — and can an AC have zero tests? | Where is the approval (role, reason, hashes)? |
| Where is the pipeline gate replay criterion? | How is DEF-5520 handled — "ignored", or a policy-checked xfail? |
| Where are the security criteria (secret scan, dependency review)? | Any evidence links/hashes? Any cost section? |
| What does `allow_xfail_if` allow — any xfail, any severity? | Who approved — a human, or "the reviewer agent"? |

### Step 2 — Write the policy and the tool

Write `readiness.yaml` v1.0.0 and `tools/readiness.py` (stdlib + pyyaml). Criteria — blocking unless noted:

| Criterion | Evidence source | Blocking |
|---|---|---|
| All required CI checks green | Actions `gates` job (or local simulation) | Yes |
| Pipeline gates G1–G5 PASS on replay | `replay.py` output / `gate_log.jsonl` | Yes |
| Hash-bound human sign-off present and matching | `HITL_signoff` entry + `verify_approval.py` | Yes |
| Every bundle AC covered by ≥1 passing (or policy-allowed xfail) test | JUnit XML + markers + `00_requirement_bundle.json` | Yes |
| Known defects within policy (severity, ticket open, strict xfail) | `known_defects.yaml` / ticket links | Yes |
| No secrets in diff; dependency scan at threshold | secret scanning / dependency review | Yes |
| Control-plane files unchanged, or code-owner approved | CODEOWNERS review status | Yes |
| Cost/duration within run budget | `run_log.jsonl` | No — reported (Module 21 ROI input) |

- [ ] `on_unknown: NOT_READY` — a criterion that cannot be evaluated blocks promotion
- [ ] `environment: staging`; `human_signoff: {hash_bound: true, roles: [qa-lead, tech-lead]}`
- [ ] `ac_coverage` reads `runs/*/00_requirement_bundle.json` with `min_tests_per_ac: 1`
- [ ] `known_defects.allow_xfail_if: {strict: true, defect_ticket_open: true, severity_in: [Sev-3, Sev-4]}`; `block_if: {severity_in: [Sev-1, Sev-2]}`
- [ ] Report `include: [ac_table, gate_trail, approvals, defects, cost, evidence_links]`

### Step 3 — Convert DEF-5520 to a strict xfail, re-gate, re-approve

The signed-off suite currently carries a **failing** test for DEF-5520. A permanently red CI trains
people to ignore red, so the approver's decision turns it into a policy-checked xfail **before** the
commit that CI will verify:

```python
@pytest.mark.xfail(strict=True, reason="DEF-5520")
def test_cannot_cancel_other_customers_order(...):
```

- [ ] G3 still passes: `no_unjustified_skips` allows `xfail` **with a `DEF-\d+` reason** — this is exactly
      why that G3 rule exists
- [ ] The test file changed → its hash changed → the old `HITL_signoff` approval is **stale**; re-run
      `verify_approval.py` (expect a refusal), then re-approve via `approve.py` (interactive) so the new
      hash is bound
- [ ] Note the Git consequence: a new commit on the PR dismisses the old review (Lab 19.4) — same event,
      two systems
- [ ] When the product is fixed, the test XPASSes and `strict=True` turns that into a failure — the
      marker gets removed and the defect closed

### Step 4 — Prove both directions (and the fail-safe)

```bash
python3 tools/readiness.py --policy readiness.yaml --out reports/readiness_report.md            # Sev-3 → READY
python3 tools/readiness.py --policy readiness.yaml --out reports/readiness_report_sev2.md \
  --defect-severity DEF-5520=Sev-2                                                              # → NOT READY
python3 tools/readiness.py --policy readiness.yaml --out reports/readiness_report_unknown.md \
  --skip security_scan                                                                          # → NOT READY (on_unknown)
```

| Run | Expected |
|---|---|
| DEF-5520 at **Sev-3**, strict xfail, ticket open | **READY** — with ac_table, gate trail, approvals, defect note, cost, evidence links |
| Severity flipped to **Sev-2** | **NOT READY** — reason: Sev-2 on the changed path |
| A criterion cannot be evaluated (security scan unavailable) | **NOT READY** — fail-safe, with the unevaluated criterion named |

- [ ] The READY report states the DEF-5520 decision explicitly — a reader can see why it was allowed
- [ ] The NOT READY reports name the blocking reason(s), not just a status
- [ ] State in one line why readiness ≠ deploy: the gate posts a report; promotion goes through a GitHub
      environment with a required human reviewer

---

## Evidence

- `readiness.yaml` v1.0.0 + `tools/readiness.py`
- `reports/readiness_report.md` (READY) + the Sev-2 and unknown-criterion NOT READY reports
- The xfail commit's new approval hash + the stale-approval refusal before re-approving
- Draft critique: ≥6 problems across policy and report

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `verify_approval.py` refuses after the xfail edit | That is correct — the approved hash no longer matches | Re-approve the new artifacts; never bypass the check |
| Readiness READY despite the failing test | xfail not `strict`, or severity check not implemented | `strict=True` + `severity_in` enforcement; test the Sev-2 flip |
| AC coverage counts 0 tests as covered | Coverage read from `tests/` instead of the bundle, or `min_tests_per_ac: 0` | Read the bundle's AC IDs and require ≥1 marker match each |
| Report has no gate trail | The tool summarised only pytest results | Generate the report from `gate_log.jsonl` + approval + bundle + results |
| Unknown criterion silently passes | `on_unknown` missing or fail-open | Default to NOT_READY and name the criterion |

## Checkpoint questions

<details>
<summary>What is the difference between "tests passed" and "deployment-ready"? Give two criteria that aren't test results.</summary>

"Tests passed" is one input. Readiness also needs, for example, a matching hash-bound human sign-off,
full AC coverage against the bundle, known defects within severity policy, clean secret/dependency
scans, and no unapproved control-plane changes. Any two with their evidence source are correct.
</details>

<details>
<summary>Why is DEF-5520's test `xfail(strict=True)` rather than `skip`?</summary>

`skip` hides the test forever. `xfail(strict=True)` keeps running it, documents the reason with a defect
ID, keeps CI green while the defect is open, and **fails** when the product is fixed (XPASS), forcing the
team to remove the marker and close the defect. It also makes the readiness policy expressible: strict +
ticket open + allowed severity.
</details>

<details>
<summary>Why does an unevaluable criterion produce NOT READY instead of being skipped?</summary>

Because "we couldn't check" is not "it's fine" — the same fail-safe principle as Module 18's gate engine.
A readiness gate that fails open silently promotes changes with unknown security or approval state; one
that fails closed keeps the human in the loop with a named reason.
</details>

---

*Next: Lab 19.7 — Local vs Delegated, where cloud/background agents get pre-configured controls before anyone delegates work.*

# Lab 19.5 — CI: Independent Re-verification + AI Review Guardrails

**Xebia — Cursor AI Training | AI-Assisted Software Engineering**
Day 6 · Module 19 · Lab 19.5 of 8 · ~8 min · Concept demo + hands-on (individual or pairs)

> **Objective:** re-run the pipeline's gates on a clean runner, where the agent has no local copy to
> modify. A laptop PASS is a claim; a CI PASS with the committed `gates.yaml` is evidence. Then decide
> exactly what AI may do in PR preparation and review — and what only a human may do.

**Guide reference:** §5 GitHub Actions Pipeline Basics; AI-Assisted PR Preparation and Review · §9 task 5
**Learning objectives covered:** 5 (Actions workflow; AI for PRs without replacing human review)

## Before you start

| Need | Notes |
|---|---|
| Labs 19.3–19.4 complete | Branch, commit, CODEOWNERS, PR template |
| Draft to critique | [`samples/workflow-draft.yml`](samples/workflow-draft.yml) |
| Files you will create | `.github/workflows/agent-pipeline.yml`, `tools/replay.py` + `tools/verify_approval.py` stubs (or reuse Module 18's), the red→green transcript, the AI guardrail table |
| Path B | No GitHub needed — simulate the workflow's steps locally; the workflow file is still the deliverable |

---

## Steps

### Step 1 — Critique the draft workflow (≥6 problems)

Read [`samples/workflow-draft.yml`](samples/workflow-draft.yml). For each problem:
*problem → attack or failure it enables → correct setting*.

| Ask yourself | Why it matters |
|---|---|
| `pull_request_target` **plus** checkout of the PR head | Untrusted PR code runs with the base repo's secrets — the classic pwn-request |
| `permissions: write-all` | The token can do far more than reading code |
| A secret printed by `echo` | Logs leak it; masking protects only accidental echoes of registered secrets |
| No `timeout-minutes`, no `concurrency` | Hung jobs burn minutes; parallel pushes race each other |
| `pip install` unpinned | Supply-chain exposure; a typo-squat installs |
| No gate replay, no approval verification, no trace-convention check | CI runs tests but never re-verifies the pipeline's own controls |
| Evidence upload without `if: always()` | The failed runs — where evidence matters most — upload nothing |
| `readiness` has no `needs:` and no artifact download | Readiness can run while gates fail, on no evidence |

### Step 2 — Write the real workflow

Write `.github/workflows/agent-pipeline.yml`: `on: pull_request` for `tests/**`, `runs/**`,
`gates.yaml`, `tools/**`, `specs/**`; `permissions: {contents: read}` at the top; `concurrency` keyed
on the PR; two jobs:

| Job | Steps |
|---|---|
| `gates` | checkout (fetch-depth 0) → setup Python → pinned install → `check_trace_conventions.py --base origin/${{ github.base_ref }}` → `replay.py --run "$(cat runs/CURRENT_RUN)"` → `verify_approval.py --run …` → `pytest -m req --junitxml=reports/junit.xml` with `SANDBOX_URL`/`SANDBOX_TOKEN` from vars/secrets → upload evidence with `if: always()` |
| `readiness` | `needs: gates`; download artifact; `readiness.py --policy readiness.yaml --out reports/readiness_report.md`; post the report as a PR comment with `pull-requests: write` only on this job |

- [ ] Top-level `permissions: contents: read`; the `readiness` job raises only `pull-requests: write`
- [ ] `timeout-minutes` on both jobs; `concurrency` cancels superseded runs
- [ ] Secrets referenced as `${{ secrets.SANDBOX_TOKEN }}`, never echoed; `SANDBOX_URL` from `vars`
- [ ] `tools/replay.py` and `tools/verify_approval.py` exist and are invoked (Module 18's stretch goal becomes a CI step)
- [ ] Upload step uses `if: always()` and the readiness job consumes the artifact

### Step 3 — Simulate the workflow locally: red, then green

Without GitHub, run the same steps from the terminal (this is what the job does, in order):

```bash
python3 tools/check_trace_conventions.py --base main
python3 tools/replay.py --run "$(cat runs/CURRENT_RUN)"
python3 tools/verify_approval.py --run "$(cat runs/CURRENT_RUN)"
pytest -m req --junitxml=reports/junit.xml

# now break it on purpose — remove one @ac marker
python3 - <<'PY'
import pathlib, re
p = pathlib.Path("tests/test_req_2481_order_cancellation.py")
p.write_text(re.sub(r'@pytest\.mark\.ac\("AC-4"\)\n', '', p.read_text()))
PY
pytest --collect-only -q tests/ ; python3 tools/verify_approval.py --run "$(cat runs/CURRENT_RUN)"
# expected: approval hash mismatch (the tests changed) → red
```

- [ ] Red run recorded: the missing marker is caught (collection/approval/verification), with the exact
      failing step named — the Actions run `#1893` equivalent
- [ ] Restore the marker, re-run the steps → green
- [ ] Note that the local edit also invalidated the approval hash — CI is re-verifying the *committed* state
- [ ] Evidence artifact listing: `runs/`, `reports/` (what `if: always()` would upload)

### Step 4 — AI-assisted PR preparation and review: the guardrail table

- [ ] Write the table in `notes/module19/ci-review.md`:

| Activity | AI does | Human does | Guardrail |
|---|---|---|---|
| PR description | Drafts from `decision_packet.md`, trailers, traceability table | Edits and owns it | Template forces traceability + agent-involvement sections |
| Self-review before opening | Reviews its own diff, lists risks | Reads the risk list | Advisory only; never counts as a review |
| Automated PR review | Posts comments on likely bugs, missing tests, spec drift | Resolves or dismisses each | Comments are **advisory checks**, not approvals |
| Review summarisation | Summarises long threads / large diffs | Makes the decision | Summary links the lines it describes |
| Fix-ups from comments | Cloud agent applies changes on the PR branch (Lab 19.7) | Re-reviews the delta | New commits re-trigger checks; approval dismissed |

- [ ] State the rule in one sentence: an AI reviewer can comment, never approve; branch protection
      requires human reviews, and agent PRs never auto-merge

---

## Evidence

- `.github/workflows/agent-pipeline.yml` with least privilege, masked secrets, timeouts, concurrency,
  `if: always()` evidence
- Red→green local simulation transcript (the missing-marker failure, then pass)
- `reports/junit.xml` + the evidence artifact listing
- AI-review guardrail table + the "AI comments, humans approve" rule
- Draft critique: ≥6 problems with the attack/failure each enables

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Workflow can't comment on the PR | Top-level `permissions` too broad or job missing `pull-requests: write` | Raise permissions only on the job that posts the summary |
| Replay fails in CI but passed locally | `fetch-depth: 0` missing; replay needs history | Set `fetch-depth: 0` on checkout |
| Secret appears in logs | Printed with `echo` (masking is for accidental output only) | Never echo secrets; pass them via `env:` to the step that needs them |
| `pytest -m req` collects nothing | Markers not registered / wrong working directory | Keep `pytest.ini` committed; run from repo root |
| Red step doesn't fail CI | `continue-on-error` or a swallowed exit code | Remove it; the gate's exit code is the check |

## Checkpoint questions

<details>
<summary>Why re-run the gates in CI when the pipeline already passed them locally?</summary>

CI is independent of the agent's environment: clean checkout, clean runner, the **committed** `gates.yaml`,
no local modifications. A laptop PASS is a claim; a CI PASS is evidence. Same "independent context"
principle as Module 15's reviewer — but enforced by a system the agent cannot edit.
</details>

<details>
<summary>Why is `pull_request_target` + PR-head checkout dangerous?</summary>

`pull_request_target` runs in the base repository's context with its secrets and token permissions. If
the workflow then checks out and executes the PR's code, an attacker's PR can exfiltrate secrets or push
with the base token. For untrusted PR code, use `pull_request` (read-only token) and never expose
secrets to fork code.
</details>

<details>
<summary>An AI reviewer approves the PR and all checks are green. Can it merge?</summary>

No. AI review comments are advisory by design. Branch protection requires reviews from human code
owners, required status checks must pass, and agent PRs are never auto-merged — the merge is a human
decision on evidence the human can inspect.
</details>

---

*Next: Lab 19.6 — Deployment-Readiness Gate, where CI results, gates, approvals and defect policy become one versioned decision.*

# Lab 20.9 — Stage 8 (Optional): Delegate One Isolated Task

**Xebia — Cursor AI Training | AI-Assisted Software Engineering**
Day 7 · Module 20 · Lab 20.9 of 10 · ~60 min, runs in parallel from Stage 4 · Optional (CA-10)

> **Objective:** demonstrate delegation the safe way — one task that is **isolated, verifiable and
> unattended-safe**, decided by the checklist **before** the agent starts, and reviewed like any
> other change. The capstone asks you to demonstrate delegation, not to delegate everything.

**Guide reference:** §8 Stage 8 (Optional) — Delegated/Background Execution of an Isolated Task
**Learning objectives covered:** 7 (optional delegated task justified by the checklist)

## Before you start

| Need | Notes |
|---|---|
| A parallel slot | This task starts after the sequence (Stage 4) and runs alongside Stages 5–7 |
| Flawed delegation plan | [`samples/delegation-draft.md`](samples/delegation-draft.md) |
| Module 19 checklist | Five areas: environment, secrets, network, permissions, human review |
| Time honesty | If the clock is tight, **cut this lab, not the controls** — CA-10 is optional |

---

## Steps

### Step 1 — Choose the task, and reject the rest

Find all six planted problems in [`samples/delegation-draft.md`](samples/delegation-draft.md) and
record them in `notes/capstone/delegation-review.md`. Then decide with this table:

| Candidate | Isolated | Verifiable | Unattended-safe | Decision |
|---|---|---|---|---|
| Add the `support_user` fixture + docstring pass on `conftest.py` | ✔ one file | ✔ collection + suite | ✔ | **good** |
| Run the full regression suite on a clean VM; attach JUnit | ✔ | ✔ | ✔ | good |
| Apply reviewer nit fixes on the PR branch | ✔ | ✔ reviewable diff | ✔ | good |
| Generate the whole test suite | ✘ | — | hides CA-4/CA-7 evidence | keep local |
| Raise defects in the tracker | external write | — | needs a human in the loop | keep local |
| Edit `gates.yaml` / `readiness.yaml` / `tools/**` | control plane | — | — | **never** |

- [ ] One task chosen and written down with its file scope
- [ ] The rejected candidates have reasons, not vibes

### Step 2 — Complete the checklist before starting

| Area | Decision (write the actual values) |
|---|---|
| Environment | Image/VM, Python version, pinned requirements, sandbox start command |
| Secrets | Which credentials (ideally none), scope, expiry; never in the repo |
| Network | Egress allow-list: git host, package mirror, sandbox |
| Permissions | Repo-scoped app; no admin; no workflow write; `agent/*` branch only; draft PR, no auto-merge |
| Human review | Named reviewer; CI must pass; merge into the feature branch only |

- [ ] `.cursor/environment.json` shape written with **no secrets** (env/keychain references only)
- [ ] Version and settings recorded (platform UIs change quickly) in `notes/capstone/delegation.md`
- [ ] One honest gap named if something cannot be configured in your environment

### Step 3 — Run it (or simulate it, labelled)

- [ ] Path A: launch the background/cloud agent on its own branch; it produces a PR
- [ ] Path B: execute the isolated task in a separate worktree
      (`git worktree add ../req-2502-fixture agent/REQ-2502-support-fixture`) and prepare the diff
      as a PR patch — **label the simulation** in `delegation.md`
- [ ] The agent touches only the files in its task scope; anything else is a checklist failure

### Step 4 — Review the result like any change

- [ ] A **named human** reviews the PR/patch; CI (or the labelled sim) re-runs the suite
- [ ] The review checks: scope respected, no control-plane edits, no secrets, tests still pass
- [ ] Merge into the feature branch; the PR link (or patch reference) goes in the report §13
- [ ] CA-10 evidence complete: `notes/capstone/delegation.md` + PR link + checklist

---

## Evidence

- `notes/capstone/delegation.md` — candidate table, five-area checklist, version/settings, gap, PR link
- `notes/capstone/delegation-review.md` — six draft defects
- `.cursor/environment.json` (secret-free) and the reviewed PR/patch

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Agent edits `gates.yaml` "to help" | Permissions too broad / no CODEOWNERS | Revoke, revert, fix the permissions; control plane is human-owned |
| Secret found in the environment file | Convenience | Move to the platform secret store; rotate; secret scan |
| Task grows beyond one file | Scope not written down | Stop it; a delegated task without a file list is not isolated |
| No cloud agent available | Environment constraint | Simulate and label it; CA-10 is optional and honesty is graded |

## Checkpoint questions

<details>
<summary>Name the three properties of a good delegated task, and one task you should never delegate.</summary>

Isolated (small, known file set), verifiable (a test or check proves it), unattended-safe (no
unnecessary secrets, no production reach). Never delegate edits to `gates.yaml`, `readiness.yaml`,
`.cursor/**` or `tools/**`; external writes such as raising defects; or generating the core test
suite — it hides the CA-4 and CA-7 evidence the capstone is built on.
</details>

<details>
<summary>Why must the checklist be completed *before* the agent starts?</summary>

Delegation is pre-configured, not supervised. Once an unattended agent is running, nobody is
watching the network, the credentials or the branch protections; the decisions have to be in place
already. A checklist completed afterwards is a description of what happened, not a control.
</details>

---

*Next: Lab 20.10 — Stages 9–10: the report package, the package check, peer review and freeze.*

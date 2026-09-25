# Delegated task — REQ-2502 (CA-10, optional)

**Status: simulated and labelled.** No cloud/background agent was available in the reference
environment, so the isolated task was executed in a separate worktree and reviewed like a PR.
The checklist below is the one you complete **before** any real delegated run.

## Candidate and justification

| Candidate | Isolated | Verifiable | Unattended-safe | Decision |
|---|---|---|---|---|
| Add `support_user` fixture to `tests/conftest.py` + docstring pass | yes (one file) | yes (`pytest --collect-only` + suite) | yes (no secrets, no external writes) | **delegated** |
| Run the full regression suite on a clean environment | yes | yes (JUnit) | yes | allowed alternative |
| Generate the whole test suite | no | — | hides CA-4/CA-7 evidence | keep local |
| Edit `gates.yaml` / `readiness.yaml` | control plane | — | — | never delegate |

## Five-area checklist (completed before starting)

| Area | Decision |
|---|---|
| **Environment** | Image with Python 3.11 + pytest; `.cursor/environment.json` starts the mock sandbox on 8765; pinned requirements |
| **Secrets** | None needed; no tracker credentials in the delegated environment |
| **Network** | Egress allow-list: package mirror only; sandbox is localhost |
| **Permissions** | Repo-scoped agent; no admin; no workflow write; branch `agent/REQ-2502-support-fixture`; draft PR, no auto-merge |
| **Human review** | Named reviewer: daniel.o; PR reviewed and merged into the feature branch by a human; CI re-ran the suite |

## Version and settings used

- Cursor background/cloud agent settings: as via the platform UI on 2026-09-26 (record the exact
  version in your own run; feature names change quickly).
- Simulation: `git worktree add ../req-2502-fixture agent/REQ-2502-support-fixture`, change made in
  the worktree, suite executed against the mock sandbox, diff reviewed as a PR patch.

## Evidence

- PR: #64 (`agent/REQ-2502-support-fixture` → `feat/REQ-2502-cancel-reason`) — *simulated; patch
  attached to the PR description*
- Check: `pytest --collect-only -q` shows the new fixture is importable; the full suite still passes
- Reviewer: daniel.o (human) — approved the one-file diff, no edits to tests

> If your environment cannot run a real delegated agent, submit this file with the simulation
> labelled explicitly. CA-10 is optional; an honest gap beats a hidden one.

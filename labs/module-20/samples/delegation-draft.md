# Delegation plan — REQ-2502 (DRAFT)

## Task to delegate

Generate the complete REQ-2502 test suite in a background/cloud agent. This is the biggest task,
so delegating it saves the most time.

## Environment

- `.cursor/environment.json` with the production Jira PAT in `env` so the agent can read the
  ticket directly (committed for reproducibility).
- Network: unrestricted (the agent may need to look things up).
- Permissions: repo admin + workflow write so it can push and re-run CI.
- It may push directly to `main` when the tests pass.
- Auto-merge the PR when CI is green.

## Ownership

Owner: the team.

## Notes

No need to record versions/settings; the platform defaults are fine. A human can look at the PR
afterwards if there is time.

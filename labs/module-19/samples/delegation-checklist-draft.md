# Delegation readiness — draft

- **Environment:** the cloud VM runs `pip install -r requirements-dev.txt` (latest versions) — no
  pinned versions needed, we always test the newest.
- **Secrets:** reuse the team's production JIRA token; store it in `.cursor/environment.json` so the
  agent can read tickets directly.
- **Network:** unrestricted egress — the agent may need to look things up.
- **Permissions:** give the GitHub app admin on the repo and workflow write so it can fix CI when
  needed; it may push to `main` for small fixes.
- **Human review:** CI green is enough; the agent can auto-merge its own PRs to keep velocity.
- **Owner:** the team.

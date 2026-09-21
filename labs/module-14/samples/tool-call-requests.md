# Tool-call requests — gate these

> **Fixture for Module 14 (Lab 14.2).** Classify each request as **retrieval** or **execution**, then run the
> riskiest execution call through the four-control stack: controlled tool access → permission → sandboxing →
> approval (deck §03). Do not edit the fixture.

| # | Tool call | What it does | Context |
|---|---|---|---|
| 1 | `read_file("src/middleware/rate_limit_middleware.py")` | reads one source file | grounded question about the middleware |
| 2 | `search_files("rate limit")` | repo-wide text search | same question |
| 3 | `fetch_defect("DEF-118")` | reads one defect record via MCP | citation for the answer |
| 4 | `create_ticket("Raise gateway limit for client X")` | opens a platform ticket | the agent found the 200/min gateway ceiling blocks client X |
| 5 | `write_file("src/middleware/rate_limit_middleware.py", …)` | edits the middleware | the agent proposes a fix |
| 6 | `run_terminal("pytest tests/test_rate_limit.py")` | runs the test suite | verifying the proposed fix |
| 7 | `trigger_pipeline("deploy-staging")` | starts a staging deploy | after tests pass |
| 8 | `post_message("#platform", "Deploy started")` | posts to Slack | notifying the team |
| 9 | `delete_branch("hotfix/tmp-rate-limit")` | deletes a branch | cleanup after merge |

**For the riskiest execution call**, be ready to answer:

- Which of the four controls are actually in play for this call, and which are not?
- Who approves, and what exactly do they see before approving?
- What happens if approval is denied, or if the call fails halfway?

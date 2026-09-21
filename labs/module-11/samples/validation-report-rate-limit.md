# Validation report — generated tests vs. contract (spec v1.0)

> **Read-only fixture for Lab 11.3.** This is part of the *input* for the Documentation agent. It models the
> Validation agent's output: a pass/fail report that flags mismatches without editing the contract.

```yaml
status: FAIL
mismatches: 1
```

| Test | Contract clause | Result | Detail |
|---|---|---|---|
| `test_ac1_limit_is_100_per_minute` | C-1, C-2 | PASS | 429 observed after 100 requests |
| `test_ac2_over_limit_returns_200_with_retry_after` | C-2, C-3 | **FAIL** | Test asserts `200` on the 101st request; contract requires `429`. `Retry-After` assertion itself is valid |
| `test_ac3_remaining_header_present_and_decrements` | C-1, C-5 | PASS | Header present; decrements by 1 |
| `test_ac4_invalid_config_fails_startup` | C-4 | PASS | Startup error names the setting |

**Action required:** fix the test to expect `429` (and keep the `Retry-After` assertion) — reported, not edited, by the validation agent.

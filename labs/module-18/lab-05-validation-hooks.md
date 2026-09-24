# Lab 18.5 — Hooks for Early Feedback: Validation, Tamper, Policy

**Xebia — Cursor AI Training | AI-Assisted Software Engineering**
Day 6 · Module 18 · Lab 18.5 of 8 · ~15 min · Build (individual)

> **Objective:** move selected engineering checks to the moment an edit or command happens. Hooks give
> earlier, cheaper feedback (a broken import is caught in-round, before a counter is spent) and one
> form of enforcement a gate cannot provide: stopping a shell write to a control file before it runs.
> Hooks stay advisory for quality — the gate remains the authoritative verdict.

**Guide reference:** §4 Add Validation Hooks for Selected Engineering Checks
**Learning objectives covered:** 4 (validation hooks: collection, lint, weakened tests, protected files, shell policy)

## Before you start

| Need | Notes |
|---|---|
| Module 17's hook set | `deny-secrets.sh`, `shell-policy.sh` (from Lab 17.3) |
| Flawed draft | [`samples/after-edit-validate-draft.py`](samples/after-edit-validate-draft.py) |
| Cursor hook support | `beforeReadFile`, `beforeShellExecution`, `afterFileEdit`, `stop` — **check current docs** for event names and payload field names |
| Reference | Guide §4 — the `after_edit_validate.py` listing and the extended `shell-policy.sh` patterns |

---

## Steps

### Step 1 — Critique the draft hook (≥5 defects)

Record *defect → consequence → fix* in `notes/module18/hooks-review.md`. The draft *looks* harmless,
which is exactly the problem — a silent hook is worse than no hook, because it is trusted.

| Ask yourself | Why it matters |
|---|---|
| What does the hook do when it crashes? | A silent failure means the safety net was never there |
| Which event field does it read? What is the real field name in the payload? | A wrong key inside a swallowed `except` means it never processes anything |
| What happens when a protected file (`gates.yaml`, `pytest.ini`, `tools/**`, `.cursor/**`) is edited? | The guide's answer: revert + `TAMPER` + log — then the gate returns NEEDS_HUMAN |
| What checks run on a test-file edit? | The point is early collect/lint/weakened-test feedback |
| Does it append to `runs/hook_log.jsonl` with enough detail? | Hook decisions are evidence too |
| What does it print for the hook protocol? | The runtime expects a response object |

### Step 2 — Build `.cursor/hooks/after_edit_validate.py`

| Behaviour | Requirement |
|---|---|
| **Protected path** | `git checkout -- <path>`, write `runs/<run_id>/TAMPER`, log `decision: revert` with the reason |
| **Test file edit** | `ruff format`, then record `collect` (`pytest --collect-only`), `lint` (`ruff check`), and a diff-based count of new unjustified `skip`/`xfail` |
| **Everything else** | Log `decision: ignored` — still logged |
| **Fail-safe** | Any internal error writes `HALT` and logs `decision: error`; the gate's own checks still run afterwards |
| **Protocol** | Print the response object the runtime expects (e.g. `{}`) |

- [ ] The skip check is a quick diff heuristic for early feedback; G3's `no_unjustified_skips` and
      `assertions_not_reduced` remain the authoritative versions — **duplicate on purpose**.

### Step 3 — Wire the hook set: `hooks.json` v2 and the extended shell policy

- [ ] `.cursor/hooks.json` v2 registers four events: `beforeReadFile` → `deny-secrets.sh`,
      `beforeShellExecution` → `shell-policy.sh`, `afterFileEdit` → `after_edit_validate.py`,
      `stop` → `run-stage-gate.sh` (now calling the real gate engine).
- [ ] Extend `shell-policy.sh` — deny patterns go **above** the allow-list, so deny is decided first:

```bash
  *"tools/approve.py"*|*"git commit"*|*"git push"*|*"--no-verify"*)
    log deny; echo '{"permission":"deny","agentMessage":"Sign-off and commits are human-only in this pipeline."}' ;;
  *"gates.yaml"*|*"pytest.ini"*|*"tools/"*|*".cursor/"*|*"githooks/"*)
    log deny; echo '{"permission":"deny","agentMessage":"Control-plane files are read-only for agents."}' ;;
```

- [ ] The second pattern is deliberately broad: an agent has no business *mentioning* those paths in a
      shell command. Hooks run outside the agent's shell, so the gate engine's own invocations are unaffected.
- [ ] Every decision — allow, deny, ask — gets a line in `runs/hook_log.jsonl`.

### Step 4 — Prove early feedback and the tamper response

Feed the hooks real payloads from the terminal (no Cursor runtime needed):

```bash
# early feedback: the hook catches a broken import before the gate
python3 -c "import json; print(json.dumps({'file_path': 'tests/test_req_2481_order_cancellation.py'}))" \
  | python3 .cursor/hooks/after_edit_validate.py
tail -1 runs/hook_log.jsonl

# shell policy: a control-file write is denied before it runs
echo '{"command": "sed -i s/max_rounds:2/max_rounds:9/ gates.yaml"}' \
  | .cursor/hooks/shell-policy.sh
tail -1 runs/hook_log.jsonl
```

| Proof | Expected |
|---|---|
| Broken import in a test edit | Hook logs `collect: false`; the agent fixes it in the **same round** — no counter used |
| `sed -i … gates.yaml` | `deny` decision + log line; the file is unchanged |
| Direct edit of `pytest.ini` | Reverted, `TAMPER` flag written, `revert` log line |
| Then run gate G3 | `control_files_untouched` → **NEEDS_HUMAN** (tamper is not a FAIL, never a retry) |
| Hook crash (feed malformed JSON) | `HALT` written + `error` log line — never silence |

---

## Evidence

- `.cursor/hooks.json` v2 + `.cursor/hooks/after_edit_validate.py` + extended `shell-policy.sh`
- `runs/hook_log.jsonl` lines: `checked` (with results), `deny`, `revert`, `ignored`, `error`
- `TAMPER` flag from the tamper proof
- G3 NEEDS_HUMAN entry after tamper
- `notes/module18/hooks-review.md` — the draft's ≥5 defects

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Hook never logs anything | Payload field name wrong (e.g. `path` vs `file_path`) | Print the raw payload once; check the current docs; handle a missing field explicitly |
| `afterFileEdit` "blocked" nothing | It cannot block — it observes | Prevention lives in `beforeShellExecution`; the editor path is revert + TAMPER, and the gate is authoritative |
| Hook error crashes the agent turn | Exception escaping | Catch everything, write `HALT`, log `error`, return the protocol response |
| Gate still PASSes after a tamper | `control_files_untouched` not implemented, or compared against the wrong snapshot | Hash control files at run start and compare before every gate |
| Deny list breaks the gate engine's own calls | Patterns applied to the runtime, not the agent shell | Hooks run outside the agent's shell policy — verify how your Cursor version scopes this |

## Checkpoint questions

<details>
<summary>Give one check that should live in both a hook and a gate, and what each placement contributes.</summary>

Test collection. The `afterFileEdit` hook catches a broken import immediately, inside the same round,
at no counter cost. G3's `tests_collect` is the authoritative, logged verdict that still holds if the
hook never fired or errored. Other good answers: lint, unjustified skips, control-file integrity.
</details>

<details>
<summary>An `afterFileEdit` hook sees the agent edited `gates.yaml`. Why is "revert and retry the agent" wrong?</summary>

The agent has just shown it will try to change the rules it is judged by. Retrying gives it another
attempt, and a successful tamper would invalidate every later verdict. It is a policy event: revert,
flag, NEEDS_HUMAN — a human decides whether the prompt, the agent, or the pipeline needs fixing.
</details>

<details>
<summary>Why keep the gate checks if the hooks already catch the same problems?</summary>

Hooks are advisory: an `afterFileEdit` observes after the fact, and a hook can error or never fire.
The gate is the authoritative verdict — deterministic, versioned, logged, and fail-safe. Duplication
is the design, not an accident.
</details>

---

*Next: Lab 18.6 — Make Sign-Off Human, where the reviewer's opinion becomes a decision packet, a hash-bound approval, and a commit guard.*

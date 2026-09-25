# Lab 20.7 — Stage 6: Independent Review and the Hash-Bound Sign-Off (G5)

**Xebia — Cursor AI Training | AI-Assisted Software Engineering**
Day 7 · Module 20 · Lab 20.7 of 10 · ~20 min · Team (3–4)

> **Objective:** make the reviewer independent by **what it cannot see**, produce a verdict with
> file:line citations, turn G5's ESCALATE into a decision packet, and record a human sign-off bound
> to the exact test hash. Two checkpoints, not twenty: the plan approval and this sign-off.

**Guide reference:** §6 Stage 6 — Validation Report and the Independent Reviewer
**Learning objectives covered:** 5 (independent reviewer in a separate context)

## Before you start

| Need | Notes |
|---|---|
| Correction round complete | Lab 20.6: `04_api_validation.json`, findings, gate trail |
| Flawed review | [`samples/review-signoff-draft.md`](samples/review-signoff-draft.md) |
| Fresh reviewer context | A new agent/subagent session that has not seen the generator's work |
| Sign-off tool | Module 18 `tools/approve.py`; interactive terminal; quality lead |

---

## Steps

### Step 1 — Give the reviewer a contract (and nothing else)

| The reviewer reads | The reviewer never reads |
|---|---|
| Bundle, spec note, approved plan, sequence | The generator's transcript or reasoning |
| Test files as committed, `04_api_validation.json` | `findings/round-k.json` explanations |
| `openapi.yaml`, `gates.yaml` (read-only) | Any chat history from the pipeline engineer |

- [ ] Five checks, each cited `file:line`: AC→test strength, no test contradicting the spec note,
      xfail/skip carry DEF-ID + `strict=True`, classifications consistent, write scope respected
      (`git diff --name-only` against the plan)
- [ ] The reviewer **never** runs `approve.py` and never approves on a human's behalf

### Step 2 — Attack the draft, then produce the real sign-off

Find all six planted problems in [`samples/review-signoff-draft.md`](samples/review-signoff-draft.md)
and record them in `notes/capstone/review-review.md` — including the independence break, the
reviewer's test edit, and the "PASS" verdict with an open product defect. Then write
`runs/req-2502-run-01/05_review_signoff.md`:

- [ ] Independence statement (what was read / never read; no `approve.py`)
- [ ] VERDICT: `PASS | FAIL | ESCALATE` — with a product defect present, `ESCALATE` is correct
- [ ] Findings table with citations; residual risks listed (DEF-5561, DEF-5520 sibling, out-of-scope paths)
- [ ] No edits to tests: a reviewer who changes the artifact destroys independence

### Step 3 — G5 and the decision packet

- [ ] `G5_review_verdict` → `ESCALATE`, `then: HITL_signoff` in `gate_log.jsonl`
- [ ] `decision_packet.md` generated **from the logs**: decision needed, gate trail, coverage,
      defect list, diff scope, hooks, cost, evidence paths + hashes
- [ ] The packet contains no transcripts and no raw test bodies — it invites judgement, not skimming

### Step 4 — Human sign-off, then prove it is bound

```bash
python3 tools/approve.py --checkpoint tests --decision APPROVE \
  --reason "DEF-5561 Sev-3 raised; failing test kept strict; suite hash bound"
```

- [ ] TTY check refuses non-interactive/agent invocation (attempt is logged)
- [ ] `HITL_signoff` records `decided_by: human:<quality-lead>`, reason, and
      `approved_hashes.tests` = the current test hash
- [ ] `package_check.py` CA-7 PASS (`signoff_matches_current_tests=True`)

| Break-it drill | How | Expected |
|---|---|---|
| **Approve then change** | Edit one assertion in a test, `git add` + `git commit` | Commit guard refuses (hash mismatch); CI `verify_approval` goes red |
| **Stale re-check** | Run `package_check.py` after the edit | CA-7 FAIL: `signoff_matches_current_tests=False` |
| **Restore** | Revert the edit (or re-gate + re-approve) | PASS again; the trail shows both attempts |

---

## Evidence

- `05_review_signoff.md` (independence statement, citations, verdict, residual risks)
- `notes/capstone/review-review.md` — six draft defects
- `decision_packet.md`; `gate_log.jsonl` `G5` + `HITL_signoff`
- Break-it transcript: refused commit / CA-7 FAIL on the tampered copy

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Reviewer agrees with everything | It read the generator's reasoning | Fresh context; remove findings explanations and transcripts from its inputs |
| Verdict PASS with an open product defect | Reviewer smoothed it over | ESCALATE; the human decides whether Sev-3 + strict xfail is acceptable |
| Sign-off hash mismatch on first try | Tests changed after approval (e.g. xfail marker added late) | Correct order: finish tests → re-gate → **then** sign off; hash the final bytes |
| Agent "recorded" the sign-off | TTY/identity guard bypassed | Revert the entry; fix the guard; a non-human `decided_by` invalidates CA-7 |

## Checkpoint questions

<details>
<summary>What makes the reviewer independent — and what breaks it?</summary>

Its **inputs**, not its model. It reads artifacts (bundle, spec note, plan, sequence, tests,
results, contract) in a fresh context and never the generator's reasoning, findings explanations or
the engineer's chat. Independence breaks the moment it is given the transcript, runs in the same
session, edits the tests, or performs the approval.
</details>

<details>
<summary>Why is the human sign-off always a separate act from the reviewer verdict?</summary>

The reviewer answers "are the tests correct?"; the human answers "is this acceptable to ship?" —
a risk decision that includes Sev-3 defects, residual risks and business context. One is analysis,
the other is accountability; merging them is how an AI ends up approving its own output.
</details>

---

*Next: Lab 20.8 — Stage 7: security, CI re-verification and deployment readiness (CP5).*

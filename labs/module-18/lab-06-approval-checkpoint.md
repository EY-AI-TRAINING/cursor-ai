# Lab 18.6 — Make Sign-Off Human: Packet, Hash-Bound Approval, Commit Guard

**Xebia — Cursor AI Training | AI-Assisted Software Engineering**
Day 6 · Module 18 · Lab 18.6 of 8 · ~15 min · Build (individual)

> **Objective:** replace "Reviewer PASS → commit" with "Reviewer recommends, a human decides". Build the
> four properties of a trustworthy checkpoint: **informed** (decision packet, not a transcript),
> **human-only** (agents cannot invoke the approver), **bound** (the approval stores artifact hashes),
> and **enforced** (the commit guard refuses anything the approval does not cover).

**Guide reference:** §5 Add a Human Approval Checkpoint Before Final Sign-Off
**Learning objectives covered:** 5 (human approval bound to exact artifacts, not performable by an agent)

## Before you start

| Need | Notes |
|---|---|
| G5 emitting `then: HITL_signoff` | Lab 18.2 + `gates.yaml` v1.1.0 |
| Gate log, findings, run log, traceability | Labs 18.3–18.7 produce them; the packet is generated **from the logs** |
| Flawed drafts | [`samples/approval-drafts.md`](samples/approval-drafts.md) — packet, approver, guard |
| `githooks/` path enabled | `git config core.hooksPath githooks` (Lab 18.1) |

---

## Steps

### Step 1 — Decision packet: critique the draft, then generate the real one

Read the draft packet in [`samples/approval-drafts.md`](samples/approval-drafts.md). Record
*defect → consequence → fix* in `notes/module18/approval-review.md`. The draft commits two classic
sins at once: it leaks the transcript, and it asserts a conclusion the approver was supposed to reach.

- [ ] Build `tools/decision_packet.py` to generate `runs/<run_id>/decision_packet.md` from the logs.
      It must contain (and nothing that makes the approver skim):

| Section | Source |
|---|---|
| Decision needed + reviewer recommendation | `05_review_signoff.md` |
| Gate trail (per gate: verdict, round, key check) | `gate_log.jsonl` |
| Correction rounds vs. budgets; findings 1 → 0; drift/tamper flags | `state.json`, findings files |
| Reruns: which stages were reused, which re-executed | `RERUN_PLAN` entries |
| Coverage: AC → tests, pass/fail counts, open defects (DEF-5520) | `traceability.md`, `04_api_validation.json` |
| Diff scope | `git diff --stat` |
| Hooks: denials, reverts | `hook_log.jsonl` |
| Cost: tokens, wall-clock | `run_log.jsonl`, `state.json` |
| Evidence paths + **artifact hashes** (tests, traceability, packet) | the files themselves |

- [ ] **Forbidden:** agent conversations and the raw test file. Both are one link away in the evidence
      list; in the packet they invite skimming and hide the question only a human can answer — *is it
      acceptable to commit a failing test for a known product defect, and is the denied shell command
      a concern?*

### Step 2 — `tools/approve.py`: human-only and hash-bound

- [ ] Refuse to run without an interactive TTY — agents run non-interactively.
- [ ] Require a reason (always, including APPROVE of an ESCALATE).
- [ ] Refuse unless `state.status == "AWAITING_SIGNOFF"`.
- [ ] Append a `HITL_signoff` entry: `decided_by: human:<role>`, approver identity, reason, and
      `approved_hashes` for **tests + traceability + packet**.
- [ ] Update state: `APPROVE → SIGNED_OFF`, `REJECT → REJECTED`, otherwise `CHANGES_REQUESTED`.

### Step 3 — Commit guard: `githooks/pre-commit`

- [ ] Find staged generated tests (`tests/test_req_*.py`); if none, exit 0.
- [ ] Compute the current hash of the generated test files and require a `HITL_signoff` **APPROVE**
      entry whose `approved_hashes.tests` matches. Any mismatch → refuse with a message telling the
      committer to regenerate the packet and get sign-off.
- [ ] Fix the draft's holes: it accepts **any** `HITL_signoff` entry (including REJECT), compares no
      hashes at all, and silently bypasses when `runs/CURRENT_RUN` is missing.

### Step 4 — Prove the three scenarios

| Scenario | How | Expected |
|---|---|---|
| **Agent self-approval** | Ask the reviewer agent to "finish the sign-off with `approve.py`" (Path A); or run it non-interactively: `python3 tools/approve.py … < /dev/null` | Shell policy denies the command (logged); even if reached, the TTY check refuses; state stays `AWAITING_SIGNOFF` |
| **Approve, then change** | Approve; then edit one test's expected message; `git add` + `git commit` | Commit guard refuses: approval hash mismatch. No commit in `git log` |
| **Approve current artifacts** | Revert the edit (or re-run the packet + approve), then commit | Commit allowed; `git log` shows the run id and verdict in the message |

- [ ] Record the refusal transcripts and the final approval entry in `notes/module18/approval-review.md`.

---

## Evidence

- `tools/decision_packet.py` + `runs/req-2481-run-02/decision_packet.md`
- `tools/approve.py` (TTY, reason, state check, hashes, state update)
- `githooks/pre-commit` (hash-bound)
- `HITL_signoff` entry with `approved_hashes`; `state.status: SIGNED_OFF`
- Refusal transcripts (self-approval, stale approval) + the successful commit hash
- `notes/module18/approval-review.md` — the draft's defects

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `approve.py` refuses in your terminal | Not a TTY (piped/redirected), or state ≠ AWAITING_SIGNOFF | Run it interactively; finish the main run first |
| Commit guard never runs | `core.hooksPath` not set, or hook not executable | `git config core.hooksPath githooks && chmod +x githooks/pre-commit` |
| Guard refuses a "correct" commit | Test file edited after approval (including a formatter pass) | That is the point — regenerate the packet and re-approve; do not weaken the guard |
| Hash differs between approve and guard | Different file sets or sorting | Hash the same sorted glob in both; document the algorithm in `PIPELINE.md` |
| Packet contains a transcript | Generator pulled the run log verbatim | The packet summarizes; it links. Fix the generator, not the approver |

## Checkpoint questions

<details>
<summary>Which control in §5 is a convenience rather than a security boundary, and what provides the real boundary?</summary>

The TTY check in `approve.py` is a speed bump — a determined process can simulate a terminal. The real
boundaries are the shell-policy denial (an agent cannot invoke it), the hash-bound commit guard, and in
Module 19 a protected branch or environment requiring a human reviewer.
</details>

<details>
<summary>A colleague fixes a typo in a test name after the QA lead approved. What happens at commit, and why is that right?</summary>

The guard refuses: the test hash no longer matches the approved hash. The approver signed off on
specific content; the fix is to regenerate the packet and get sign-off again — quick, because the
change is trivial — rather than letting unapproved content ship under an old approval.
</details>

<details>
<summary>The Reviewer returns APPROVE. List everything that must still happen before tests can be committed.</summary>

G5 validates the verdict (known value, cites all original ACs, findings name owners). The decision
packet is generated; the run enters AWAITING_SIGNOFF. A human runs `approve.py` with a reason, appending
a hash-bound `HITL_signoff` entry. Then the commit guard verifies the staged tests match the approved hash.
</details>

---

*Next: Lab 18.7 — Run It and Break It, where the whole control plane meets the main run and drills D1–D7.*

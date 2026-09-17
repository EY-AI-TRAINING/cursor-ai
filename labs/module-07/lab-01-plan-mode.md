# Lab 7.1 — Plan Mode: Explore → Plan → Review → Implement

**Module 7 · Plan, Debug, Refactoring & Testing | Xebia — Cursor AI Training**
Day 2 · Lab 1 of 3 · ~15–20 minutes · Individual

> **Objective:** run Plan mode's four-stage cycle on a moderately complex task — and treat the plan itself as the
> reviewable artifact. You will send a plan back for revision once before approving any implementation.

**Guide reference:** Module 7, §1 (Plan mode for complex tasks)
**Learning objectives covered:** 1 — explore → plan → review → implement.

---

## Before you start

- Modules 3–6 complete; clean tree on the default branch; create your lab branch:

  ```bash
  git switch -c module7-lab
  ```

- Pick `<moderate-task>` — complex enough that you'd want a plan, bounded enough to finish in ~10 minutes of
  implementation. Examples (adapt to your sandbox):
  - "Add input validation to the `<entity>` update path and surface errors consistently"
  - "Add pagination to the `<feature>` listing endpoint"
  - "Persist `<feature>` state across restarts"
- Know your `<test-command>`.
- Open Plan mode via the mode selector (`Cmd/Ctrl+.` — or `Shift+Tab` to rotate modes).

---

## Step 1 — Write a task brief with constraints

One paragraph that the plan can be judged against:

> "**Goal:** `<moderate-task>`.
> **Constraints:** follow existing patterns in `<target-folder>`; no new dependencies; keep the change small;
> list anything you consider out of scope."

- [ ] Brief written, with at least two explicit constraints
- [ ] Baseline check: current `<test-command>` passes before you start (evidence: `____________`)

---

## Step 2 — Explore → Plan (no edits yet)

1. Send the brief in **Plan mode**.
2. Let it explore the codebase and produce a plan. Verify the plan stays a plan — if it starts editing files,
   stop it (that's Agent mode behavior, not Plan mode).
3. Capture the plan (copy it into a scratch note).

- [ ] Plan captured, with zero code changes applied so far (`git status` proves it)

---

## Step 3 — Review the plan like a design doc

Grade the plan against your brief before touching it:

| Check | Notes |
|---|---|
| Does every step map to the goal (no scope creep)? | |
| Does it follow the constraints (patterns, no deps, size)? | |
| Are steps ordered and individually verifiable? | |
| What's missing or wrong? | |

- [ ] At least one substantive issue, gap, or scope drift identified
- [ ] Decision recorded: approve **or** request revision — you must request at least one revision

---

## Step 4 — Revise (the loop that Agent mode doesn't give you)

Send the plan back with specific feedback, e.g.:

> "Revise the plan: drop the `<out-of-scope item>` step — out of scope; split step 3 into schema change and
> migration; state how each step is verified."

- [ ] Plan revised in response to your feedback; the diff between plan v1 and v2 is visible in your notes

---

## Step 5 — Implement the approved plan

1. Approve the revised plan and let the agent implement it.
2. During implementation, apply the Module 6 review discipline: per-file diffs, read before approving.
3. Run `<test-command>` yourself; the plan's own verification steps should hold.

- [ ] Implementation matches the approved plan (or deviations are noted and justified)
- [ ] Tests/lint pass; output recorded
- [ ] Commit on the branch: `git commit -m "Module 7 lab: <moderate-task> (Plan mode)"` → hash `____________`

---

## Evidence

- Plan v1 + plan v2 (the revision cycle)
- Your Step 3 grading table
- Validation output + commit hash

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Plan mode starts editing immediately | Wrong mode selected, or you approved too fast | Stop; re-send in Plan mode; the checkpoint *is* the lesson |
| Plan is vague ("update the relevant files") | Task brief lacked constraints | Re-send with the Step 1 structure |
| You can't find anything to revise | Plan is genuinely good | Still exercise the loop: ask it to reorder for earlier verifiability, or to justify one design choice |
| Implementation drifts from the plan | Agent improvising | Point it back at the approved plan; note the drift in your evidence |
| Plan is huge — 15 steps for a small task | Task wasn't moderate | Shrink the task; note that plan size is a scope signal |

---

## Checkpoint questions

1. What does Plan mode add over Agent mode's implicit planning?
2. What are the four stages, and where is the required checkpoint?
3. When is Plan mode the right tool, vs. going straight to Agent mode?

<details>
<summary>Answers</summary>

1. Planning becomes an explicit, reviewable artifact with a required approval checkpoint *before* any code changes — Agent mode plans internally and you only see the resulting diff.
2. Explore → Plan → **Review (you approve, edit, or reject)** → Implement; the checkpoint is Review, before Implement.
3. Complex, ambiguous, or high-risk tasks where being wrong early is expensive — multi-step features, architecture-touching changes. Well-understood, boundable tasks can go straight to Agent mode (Module 6).

</details>

---

## Next

**Lab 7.2** — Debug mode: a provided failure, a stated hypothesis, and no fix until the hypothesis is confirmed.

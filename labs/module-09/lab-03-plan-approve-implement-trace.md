# Lab 9.3 — Plan, Approve, Implement & Trace

**Module 9 · AI-Assisted Design & Spec-Driven Development (SDD) | Xebia — Cursor AI Training**
Day 3 · Lab 3 of 3 · ~25–30 minutes · Individual + peer/facilitator approval

> **Objective:** run Plan mode against the *approved* spec (not a chat memory of the feature), revise and approve
> the plan, implement the first thin pass, and close the loop with an AC → code → test traceability matrix. If the
> spec has to change, it changes through versioning — never silently.

**Guide references:** Module 9, §2 (traceability; versioning), §4 (Plans from requirements), §7 (approval gate)
**Learning objectives covered:** 1 — spec as source of truth in action; 2 — traceability + versioning; 4 — Plan mode against a spec; 7 — the approval gate.

---

## Before you start

- Labs 9.1–9.2 complete on `module9-lab`: `spec.md` v1.0 approved, `architecture.md` + contract committed, ADR recorded
- Plan mode available. If not, ask for a plan-only response and hold all edits (facilitator notes)
- `<test-command>` known and **green before you start** — record the baseline
- Plan mode's checkpoint discipline from Module 7 applies: no implementation until *you* approve the revised plan

---

## Step 1 — Generate a plan grounded in the spec

In **Plan mode**, point the agent at the artifacts, not at your memory of the feature:

> "Read `@specs/<feature>/spec.md` (approved v1.0), `@specs/<feature>/architecture.md`, and the contract.
> Produce an implementation plan where **every step names the AC IDs it satisfies** and the file(s) it touches.
> Include the verification for each step. Do not plan anything outside the spec's scope or the exclusions in §4.
> Stop before editing anything."

- [ ] Plan captured; every step cites AC IDs and files; no code changes yet (`git status` proves it)

---

## Step 2 — Review the plan *against the spec* (the spec is the rubric now)

| Check | Notes |
|---|---|
| Every AC covered by at least one step? Any AC with no step? | |
| Any step that traces to **no** AC (scope creep)? | |
| Consistent with the contract and the ADR? | |
| Does each step name a verification? | |
| Thin enough for a first pass? | |

- [ ] Coverage gaps or creep identified (at least one substantive finding)
- [ ] Decision recorded: approve **or** request revision — you must request at least one revision (Module 7 discipline)

---

## Step 3 — Revise and approve the plan (second approval gate)

Send specific feedback, e.g.:

> "Revise: step 3 doesn't name its ACs; split the schema change from the endpoint work; drop the caching step —
> no AC requires it. State how each step is verified."

1. Save the revised plan as `specs/<feature>/plan.md` with a header:

   ```markdown
   # Implementation plan: <feature>
   **Targets:** spec v1.0 · **Status:** Approved — <approver>, YYYY-MM-DD
   ```

2. Confirm again that **zero source files have changed**.

- [ ] Plan v1 + v2 both visible (in notes or git); v2 approved with target spec version
- [ ] `git status` still shows no source changes

---

## Step 4 — Implement the first pass against the approved spec

1. Switch to Agent mode:

   > "Implement `@specs/<feature>/plan.md` (approved) against `@specs/<feature>/spec.md` v1.0. After each step,
   > run the verification it names. If the plan and spec conflict, **stop and flag it** — do not improvise."

2. Apply Module 6 review discipline: per-file diffs, read before approving, gate every terminal command.
3. Stop at first pass: complete the ACs; don't gold-plate beyond the spec (the exclusions are there for a reason).

- [ ] Implementation matches the approved plan (or deviations are flagged and justified)
- [ ] No out-of-spec changes; exclusions respected

---

## Step 5 — Tests that name their criteria

1. Have the agent generate/align one test per acceptance criterion, with the AC ID in the test name, e.g.:

   ```python
   def test_ac3_returns_400_with_auth_004_for_invalid_email(): ...
   ```

   The AC text is the test's source — tests generated from the implementation verify the code, not the requirement.
2. Run `<test-command>`; capture the output.
3. Where automation isn't possible (e.g., "no plaintext token in logs"), record the manual check performed.

- [ ] Every AC has a test or a recorded manual verification; IDs appear in test names
- [ ] `<test-command>` output captured (baseline → new run)

---

## Step 6 — Build the traceability matrix (both directions)

Create `specs/<feature>/traceability.md`:

```markdown
# Traceability: <feature>
**Spec version:** v1.0 · **Commit:** <hash>

| AC ID | Spec version | Code (file:line / commit) | Test (name or manual check) | Result |
|-------|--------------|---------------------------|------------------------------|--------|
| AC-1  | v1.0         | `src/.../x.py:42`         | `test_ac1_...`               | PASS   |
| AC-2  | v1.0         | ...                       | manual: checked logs ...     | PASS   |
```

Check both directions:

- **Clause → code/test:** any AC without a row is an untraced requirement — a gap.
- **Code → clause:** any changed source file with no AC row is orphan code — remove it, or (if truly required)
  add it through a **versioned spec change**.
- **Version check:** if implementation exposed an ambiguity or forced a deviation, don't silently edit:
  1. Bump the spec: `v1.1`, add a change-log row with the reason.
  2. Note which code/tests are now flagged for re-validation — this is exactly what traceability is for (guide §2).

- [ ] Every AC has a matrix row; every changed source file traces to an AC (or was removed)
- [ ] Spec change-log updated if anything moved after approval (with linked artifacts flagged)

---

## Step 7 — Commit

```bash
git status                                  # confirm scope: specs/, src/, tests/
git add specs/ src/ tests/
git commit -m "Module 9 lab: first implementation pass for <feature> against spec v1.0"
git log --oneline -1
```

- [ ] Committed on `module9-lab`; hash `____________`
- [ ] Ready to state what Module 11 extends: this spec, its plan, and its traceability links become inputs to the reusable agents built next

---

## Evidence

- `plan.md` v1 + approved v2 (the revision cycle and the approval record)
- Implementation diff + commit hash; no implementation before plan approval (`git status` proof)
- Test names/cases referencing AC IDs + `<test-command>` output
- `traceability.md` (complete in both directions)
- Spec change-log entry with flagged code/tests if the spec moved

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Plan paraphrases the feature instead of citing AC IDs | Spec wasn't in context, or plan generated in a fresh chat | Re-run with `@spec.md @architecture.md`; require "every step names its AC IDs" |
| Agent implements beyond the spec | "Helpful" gold-plating | Point at spec §4 exclusions; remove the extra; the Step 6 orphan check catches leftovers |
| A diff line traces to no AC | Either orphan code or a missing criterion | Remove the code, or add the criterion via a versioned spec change — never leave it unexplained |
| Tests pass but don't map to criteria | Tests written from the code, not the spec | Regenerate from AC text; put the AC ID in the test name |
| Spec had to change mid-implementation | Normal — specs evolve under contact with reality | Bump version, change-log entry, flag linked code/tests for re-validation (not a failure — the system working) |
| Plan mode starts editing | Approved too fast or wrong mode | Stop; the review checkpoint *is* the lesson (Module 7) |
| Traceability matrix is all green | You might be writing it from memory | Re-check one row by actually opening the cited file:line and running the named test |

---

## Checkpoint questions

1. Why must the plan cite AC IDs rather than restate the feature goals?
2. What are the two directions of traceability, and what does each catch?
3. What should happen when the spec changes after code and tests were generated against an earlier version?

<details>
<summary>Answers</summary>

1. AC IDs turn the plan into a checkable mapping: coverage is mechanical (every AC has a step) and scope creep is visible (a step with no AC). Restating goals lets both hide in prose.
2. Clause → code/test catches **untraced requirements** (an AC nothing implements or verifies); code → clause catches **orphan code** (implementation or tests nothing required). Together they keep the spec and the change set honest.
3. The spec gets a new version and a change-log entry; the traceability links identify exactly which code and tests were built against the old version and now need re-validation or re-generation — the same staleness problem Module 8 solved for rules, applied to specs.

</details>

---

## Next

**Module 10** — Agent, Skill & Subagent Architecture Fundamentals: your spec, plan, and architecture become the inputs an agent is formally defined to operate against. **Module 11 (Use Case Lab 1)** extends this same spec into reusable requirement-analysis, test-generation, validation, and documentation agents — keep the branch and the artifacts.

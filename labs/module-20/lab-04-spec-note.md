# Lab 20.4 — Stage 3: The Spec Note Whose AC Set Equals the Bundle (CP3)

**Xebia — Cursor AI Training | AI-Assisted Software Engineering**
Day 7 · Module 20 · Lab 20.4 of 10 · ~20 min · Team (3–4)

> **Objective:** write the one-page spec note that fixes what "correct" means before anything
> claims to be correct: each AC as Given/When/Then, pinned to a contract location, with the
> clarifications and known defects recorded. The spec note's AC-ID set must **equal** the
> bundle's — no invented criterion, no silently dropped one.

**Guide reference:** §3 Stage 3 — Spec Note That Fixes the Acceptance Criteria
**Learning objectives covered:** 3 (spec note with one-to-one AC mapping to the bundle)

## Before you start

| Need | Notes |
|---|---|
| Bundle valid, AC-4 confirmed | Lab 20.2 |
| Plan approved | Lab 20.3 — the spec note header cites the approval |
| Flawed spec note | [`samples/spec-note-draft.md`](samples/spec-note-draft.md) |
| Contract | `specs/openapi.yaml` (read-only) |

---

## Steps

### Step 1 — Attack the draft (5 min)

Find all six planted problems in [`samples/spec-note-draft.md`](samples/spec-note-draft.md):
missing header, an invented AC, a dropped AC, a contract contradiction, prose instead of
Given/When/Then, and no contract references. Record *defect → consequence → fix* in
`notes/capstone/spec-review.md`.

> The dangerous one is the invented AC: it would generate tests for a requirement nobody asked
> for, and the traceability matrix would look complete while covering the wrong thing.

### Step 2 — Write the note (one page, four sections)

| Section | Content |
|---|---|
| Header | Ticket revision, bundle sha, plan approval timestamp + approver |
| Per AC | `### AC-n — title`, Given/When/Then in contract-verifiable terms, `Contract:` reference |
| Decisions | CL-1/CL-2 confirmed; DEF-5520 noted as related-but-out-of-scope |
| Open issues | Anything parked (with the reason and where it is tracked) |

- [ ] AC-3 states the boundary explicitly: **L ∈ [1, 280] → 200; 0 / absent / 281 → 422** —
      do not write "under 500" or "a reasonable length"
- [ ] AC-4 states visibility (owner + support; others 403) **and** ordering (newest first)
- [ ] Every AC carries a `Contract:` line into `openapi.yaml`

### Step 3 — Run the set-equality check (this is CA-3)

```bash
# AC headings in the spec note vs AC ids in the bundle — must be identical sets
grep -oE '^#+ *AC-[0-9]+' specs/REQ-2502-spec-note.md | grep -oE 'AC-[0-9]+' | sort -u
python3 - <<'PY'
import json
b = json.load(open("runs/req-2502-run-01/00_requirement_bundle.json"))
print(sorted(a["id"] for a in b["acceptance_criteria"]))
PY
```

- [ ] Sets are equal: `{AC-1, AC-2, AC-3, AC-4}` on both sides
- [ ] If the spec has an extra AC: remove it or add it to the ticket — never leave it
- [ ] If the spec misses one: add it or park it as an open issue with a reason
- [ ] Ticket owner confirms the note (record who and when)

### Step 4 — Freeze and hand off (CP3)

- [ ] `package_check.py` CA-3 PASS (`spec=[...] bundle=[...]`)
- [ ] The note is committed; no further edits after generation starts without a rerun plan
- [ ] **Facilitator places the 15-minute break here** — human agreements are done; generation
      starts fresh afterwards

---

## Evidence

- `specs/REQ-2502-spec-note.md` (header, four ACs with G/W/T, decisions)
- `notes/capstone/spec-review.md` — six draft defects with consequences
- Set-equality output (identical sets) and the owner's confirmation

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| CA-3 fails with an extra AC | Invented criterion | Remove it or add it to the ticket; the set must match exactly |
| AC-3 says "max 500 characters" | Draft copied without the contract | Re-derive from `openapi.yaml` (`maxLength: 280`) |
| Ordering not stated for AC-4 | CL-2 not carried into the note | Add "newest first" — the tests and reviewer need one source of truth |
| Spec note keeps changing after approval | Normal editing vs. control drift | Any post-approval change to plan/spec triggers the rerun planner and may invalidate downstream hashes |

## Checkpoint questions

<details>
<summary>Why must the spec note's AC set equal the bundle's, exactly?</summary>

More ACs means testing invented requirements; fewer means silently dropping agreed ones. The
one-line set check (CA-3) is what keeps the traceability spine honest: every test can be traced to
a criterion a human confirmed, and every confirmed criterion has a test. It is cheap to check and
expensive to skip.
</details>

<details>
<summary>Where does the contract fit relative to the spec note?</summary>

The spec note states the criterion in verifiable terms and pins it to a contract location
(`openapi.yaml#...`). If the API disagrees with the contract, that is a **product defect** — the
contract is the agreed definition of correct, and the test stays strict. The note never says
"match the API".
</details>

---

*Next: Lab 20.5 — Stage 4: the engineering test sequence (G1/G2).*

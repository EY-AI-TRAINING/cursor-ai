# Lab 18.1 — Open the Control Plane: Branch, `PIPELINE.md` v2, State & `gates.yaml` v1.1.0

**Xebia — Cursor AI Training | AI-Assisted Software Engineering**
Day 6 · Module 18 · Lab 18.1 of 8 · ~10 min · Setup (individual)

> **Objective:** create the branch and baseline, then write down the three things Lab 3 kept in your
> head — the control loop (`PIPELINE.md` v2), the run state (`state.json`), and machine-checkable gate
> criteria (`gates.yaml` v1.1.0). Two of them arrive as deliberately flawed drafts; repairing them is
> how you learn what the gate engine will depend on.

**Guide reference:** §0 Setup — Branch, `PIPELINE.md` v2, Run State, and `gates.yaml` v1.1.0
**Learning objectives covered:** 1 (automated gates driven by a versioned `gates.yaml`)

## Before you start

| Need | Where it comes from |
|---|---|
| The Lab 3 pipeline, run folder `runs/req-2481-run-01/`, and Module 17's `gates.yaml` v1.0.0 | Modules 16–17, branch `module17-lab` |
| Python 3.11 with `pyyaml`, `pytest`, `ruff` | Prerequisites — verify with the Step 5 smoke check |
| Flawed drafts to critique | [`samples/state-draft.json`](samples/state-draft.json) · [`samples/gates-v1.1.0-draft.yaml`](samples/gates-v1.1.0-draft.yaml) |
| Everything below runs from | `<pipeline-root>` (your `requirement-to-test/` workspace) |

---

## Steps

### Step 1 — Branch, keep the baseline, enable the commit-guard path

- [ ] Create the lab branch from Module 17's work.
- [ ] Copy Lab 3's run as an untouched comparison baseline.
- [ ] Point git at `githooks/` (the guard lands there in Lab 18.6) and pin the current run.

```bash
git switch module17-lab && git switch -c module18-lab
cp -r runs/req-2481-run-01 runs/_baseline-run-01
git config core.hooksPath githooks
echo req-2481-run-02 > runs/CURRENT_RUN
mkdir -p runs/req-2481-run-02/findings tools schemas notes/module18
```

- [ ] Confirm `runs/_baseline-run-01/` contains 01–05, `traceability.md`, `run_log.jsonl`, and the
      failing DEF-5520 evidence. **Do not modify the baseline** — every "what changed?" question in
      this lab is answered against it.

### Step 2 — Write the control loop into `PIPELINE.md` (v2.0.0)

Add a `## Control loop (v2.0.0)` section below the Lab 3 stage table. It must state, unambiguously,
what happens after every stage — the orchestrator (you, a parent agent, or a script) will follow it
literally.

| After stage N… | The control loop says |
|---|---|
| Run the gate | `python3 tools/gate_engine.py --run <run_id> --gate <G_N>` — **0 = PASS, 1 = FAIL, 2 = NEEDS_HUMAN**; any other exit code, timeout, or missing output = NEEDS_HUMAN |
| PASS | Run `tools/rerun_plan.py`; execute the next **stale** stage |
| FAIL | Run `tools/loop_control.py`; **RETRY** → invoke the stage named in `findings/round-<k>.json` `route_to`, passing **only** that file + the artifact to modify; **ESCALATE** → stop, packet, human |
| NEEDS_HUMAN | Stop. Generate the decision packet. Wait for a human |
| After G5 (APPROVE or ESCALATE) | Generate the packet → `state.status = AWAITING_SIGNOFF` → stop |

- [ ] Also record the hard rules: agents never edit `gates.yaml`, `tools/**`, `schemas/**`,
      `githooks/**`, `.cursor/**` (hooks enforce); agents never run `tools/approve.py`; run budget
      **4 correction rounds · 400k tokens · 20 min**, exceeded → ESCALATE.
- [ ] Keep the Lab 3 stage table as v1 history; note the version bump.

### Step 3 — Repair the run-state draft, then create the real `state.json`

Read [`samples/state-draft.json`](samples/state-draft.json). It represents the same run at the moment
all five stages have finished and the pipeline is waiting on sign-off. Find **at least 4 defects**;
record each one as *defect → consequence → fix* in `notes/module18/setup-review.md`.

| # | Defect | Consequence | Fix |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |

- [ ] Create the real `runs/req-2481-run-02/state.json` for a run that is about to start: all stages
      `PENDING`, counters zero, `budget_used` zero, empty `history`, `status: "RUNNING"`,
      `gates_version: "1.1.0"`, `pipeline_version: "2.0.0"`.
- [ ] Confirm every stage entry can later hold `status`, `input_hash`, `output_hash`; and that
      `history` entries will carry `gate`, `round`, `findings`, `artifact_hash`, `assertions`,
      `counter` — the loop controller's four bounds read exactly these.

### Step 4 — Repair the `gates.yaml` v1.1.0 draft

Read [`samples/gates-v1.1.0-draft.yaml`](samples/gates-v1.1.0-draft.yaml). It was edited in a hurry
from Module 17's v1.0.0. Find **at least 6 defects** and record them in the same notes file.

What the repaired `gates.yaml` v1.1.0 must contain (guide §0):

| Requirement | Why |
|---|---|
| `version: 1.1.0` — bumped because the checks changed | Verdicts from different criteria are not comparable |
| `run_budget: {max_total_rounds: 4, max_tokens: 400000, max_minutes: 20}` | A bound above the per-owner counters |
| `counters: {generator: {max_rounds: 2}, sequence: {max_rounds: 1}}` — declared once, shared | G3 ↔ G4 ping-pong cannot buy 2 + 2 rounds |
| Checks are **ids** the engine can look up, not prose | A typo becomes "unknown check" → NEEDS_HUMAN, not a silent skip |
| G1 `on_fail: needs_human` | A deterministic input problem is the owner's, never a retry |
| G3 includes `control_files_untouched`, `ac_coverage_complete`, `no_unjustified_skips`, `assertions_not_reduced` | "Passing by cheating" must FAIL |
| G4 includes `allow: [PRODUCT_DEFECT]` and `on_environment: {infra_retry: 1, then: needs_human}` | Product defects are flagged, not retried; the sandbox is not the generator's fault |
| G5 includes `then: HITL_signoff` | APPROVE and ESCALATE both stop at the human |

- [ ] Write the repaired file to `<pipeline-root>/gates.yaml`. Keep every gate's `after:` stage and
      the G5 `on_request_changes: {route_to: from_findings}` rule.

### Step 5 — Setup smoke check

```bash
python3 -c "import yaml, pytest; print('yaml+pytest ok')"
ruff --version
python3 -c "import yaml; yaml.safe_load(open('gates.yaml')); print('gates.yaml parses')"
ls runs/_baseline-run-01/ | head
cat runs/CURRENT_RUN
```

- [ ] All four checks pass; `tools/`, `schemas/`, `findings/`, and `notes/module18/` exist.
- [ ] If you are on Path B (offline kit), also complete the setup section of
      [`samples/offline-kit/README.md`](samples/offline-kit/README.md) now.

---

## Evidence

- `module18-lab` branch; `runs/_baseline-run-01/` untouched; `runs/CURRENT_RUN`
- `PIPELINE.md` with the v2.0.0 control loop section
- `runs/req-2481-run-02/state.json`
- `gates.yaml` v1.1.0
- `notes/module18/setup-review.md` with both defect tables (≥4 + ≥6) and the smoke-check output

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `git config core.hooksPath` seems to do nothing | No `githooks/pre-commit` exists yet | Expected — it activates in Lab 18.6; verify with `git config core.hooksPath` |
| `import yaml` fails | Wrong interpreter | Use the Python 3.11 env that has `pyyaml`; see the README's prerequisites |
| The draft `gates.yaml` "looks fine" | Compare it against the guide's §0 listing field by field | Count the missing checks and the counter names, not the overall shape |
| Baseline run missing | Lab 3 run was renamed or cleaned | Re-copy from `runs/req-2481-run-01/`; if that is gone, ask the facilitator for the offline kit's `fixture-run/` |

## Checkpoint questions

<details>
<summary>Why must `gates.yaml` change its version on *any* edit — even a typo fix?</summary>

The version is part of every verdict line. Without a bump, old and new verdicts look comparable but
were produced by different criteria, and the audit trail lies. The engine can also refuse to run when
`state.json` and `gates.yaml` disagree mid-run.
</details>

<details>
<summary>Why does run state live on disk instead of in the orchestrator's memory?</summary>

A crashed orchestrator resumes from `state.json` instead of restarting from memory; rounds, hashes,
and budget survive restarts; and reviewers can see *why* the run is where it is. It is also what makes
the loop controller deterministic — it reads the same state every time.
</details>

<details>
<summary>Why one `generator` counter instead of one per gate?</summary>

G3 and G4 both route failures to the Test Generator. Separate counters would let a fix-one-break-the-other
ping-pong run 2 + 2 rounds and hide oscillation. The budget belongs to the **owner**, not the gate.
</details>

---

*Next: Lab 18.2 — Build the Gate Engine, where `gates.yaml` becomes verdicts: three-valued exit codes, cheap-first checks, fail-safe defaults, and an append-only log.*

# Lab 9.4 (Extension) — GitHub Spec Kit: The Same Spec, Tooled

**Module 9 · AI-Assisted Design & Spec-Driven Development (SDD) | Xebia — Cursor AI Training**
Day 3 · Optional extension lab · ~30–40 min · Individual or pair · Requires network + install permission

> **Objective:** run the same `<feature>` through **GitHub Spec Kit** — the open-source toolkit referenced in the
> module guide's Further Reading — and compare its generated artifact chain (`constitution → specify → clarify →
> plan → checklist → tasks → analyze → implement → converge`) against the manual artifacts you built in Labs
> 9.1–9.3. The learning is judgment: what the tool standardizes and automates, and what remains irreducibly human.

**Guide reference:** Module 9, §2 (traceability), §4 (plans), §5 (contracts), §7 (approval gates) · Further Reading (GitHub Spec Kit)
**Learning objectives covered:** 1 — spec as durable source of truth; 2 — traceability; 3 — choosing the right rigor; 4 — plans from specs; 5 — contracts; 7 — approval gates.

> **Read this first:** Spec Kit does not replace Module 9's discipline — it packages it. Its commands are agent
> skills you invoke **one at a time in chat, reviewing each artifact before the next**, not an autonomous pipeline.
> The human approval gate and the judgment calls are still yours; the toolkit just standardizes the artifacts.

---

## Before you start

- Labs 9.1–9.3 complete on `module9-lab`: approved `spec.md`, `architecture.md` + contract, ADR, `plan.md`, and `traceability.md` — you need these as the comparison baseline
- Network access and permission to install the `specify-cli` tool (this lab is the **one sanctioned install** — Module 6's no-install rule holds everywhere else)
- `uv` installed (Python 3.11+); fallbacks: `pipx`, or an offline tabletop path (Step 1 note)
- **A scratch clone, not your lab branch:**

  ```bash
  git clone <sandbox-repo-url> /tmp/speckit-lab
  cd /tmp/speckit-lab
  git switch -c module9-lab-speckit
  ```

  Spec Kit's init writes agent command files and a `.specify/` directory. A scratch clone keeps your Module 8 starter kit and Module 9 artifacts untouched — never run `specify init` in a repo whose files you can't restore.

---

## Step 0 — Map the workflow before you run it (2 min)

| Module 9 concept (guide) | Spec Kit command | What it produces |
|---|---|---|
| Project rules / `AGENTS.md` (Module 8) | `/speckit.constitution` (once per project) | `memory/constitution.md` — guiding principles every later step is checked against |
| Spec with testable acceptance criteria (§1, §7) | `/speckit.specify` | `specs/###-<feature>/spec.md` + `checklists/requirements.md` |
| Open questions in the spec | `/speckit.clarify` | Targeted questions; answers folded back into the spec |
| Architecture diagram, contracts, ADR (§5, §6) | `/speckit.plan` | `plan.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md` |
| Testability review of the spec (§7) | `/speckit.checklist` | Reviewer-owned requirements-quality checklist |
| Implementation plan (§4) | `/speckit.tasks` | Dependency-ordered `tasks.md` |
| Spec ↔ plan ↔ tasks traceability (§2) | `/speckit.analyze` | Read-only conflicts/gaps/coverage report — fix at source, re-run |
| Implementation (§4) | `/speckit.implement` | Code, executed task-by-task; gates on unchecked checklist items |
| Spec-to-code/test traceability (§2) | `/speckit.converge` | Gap check against spec/plan/tasks; appends tasks until **Converged** |

- [ ] Two columns filled in from memory before running anything: which command do you *expect* to be strongest, and which do you suspect misses your manual discipline? `____________`

---

## Step 1 — Install and initialize (scratch clone only)

1. Install the CLI (read and gate the command — this is the sanctioned exception):

   ```bash
   uv tool install specify-cli          # preferred
   # fallbacks: pipx install specify-cli · uvx · or pin a release:
   # uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@vX.Y.Z
   specify check
   ```

2. Initialize in the scratch clone with the Cursor integration:

   ```bash
   specify init --here --force --integration cursor
   # older releases use: specify init --here --force --ai cursor
   # if unsure, run: specify init --help
   ```

3. Verify what was created — `.specify/` (templates, memory, scripts, `feature.json`) and the agent command files. Note which slash-command form your release exposes: `/speckit.specify` or `/speckit-specify`. Type `/` in Cursor chat and look for `speckit`.
4. Record the tool version (e.g., `uv tool list` or the release tag you pinned) and command names as evidence — Spec Kit evolves quickly, and your notes should be reproducible.

> **Cannot install (offline / locked-down seat)?** Do the tabletop path instead: read the Spec Kit quickstart and
> templates from https://github.com/github/spec-kit, then complete Steps 0, 3, 4, and 7 by mapping your manual
> artifacts onto the generated structure. The comparison and the debrief are the learning; the tool run is the demo.

- [ ] CLI installed and `specify check` passed (or tabletop path chosen and noted)
- [ ] `.specify/` + command files created in the scratch clone; version/command names recorded
- [ ] `git status` in the **real** sandbox repo shows no changes

---

## Step 2 — Constitution: Module 8's rules, formalized

1. In Cursor chat in the scratch clone, run `/speckit.constitution` (or `/speckit-constitution`) and pass the
   principles from your sandbox's Module 8 `AGENTS.md` and scoped rules as the argument — e.g., error-handling
   conventions, test layout, "never hand-edit `generated/`".
2. Review the generated `memory/constitution.md` before accepting: principles, not a restatement of conventions;
   every future plan is checked against it.
3. Note the overlap with Module 8's rules/`AGENTS.md`. Both are durable, repo-committed instructions — what does
   the constitution add, and what would you keep where?

- [ ] Constitution reviewed/edited; overlap with Module 8 artifacts noted

---

## Step 3 — Specify: run the same ticket, compare specs

1. `/speckit.specify <paste the raw ticket text, not your finished spec>` — describe *what and why* only; this is
   intentional: the tool should produce requirements without your design decisions leaking in.
2. If it asks clarifying questions, answer as if you hadn't already solved the ambiguity — then run `/speckit.clarify`
   if anything remains underspecified.
3. Compare the generated `spec.md` against your manual `spec.md`:

   | Check | Manual (Lab 9.1) | Spec Kit |
   |---|---|---|
   | Criteria testable and unambiguous? | | |
   | Explicit exclusions present? | | |
   | Non-functional constraints captured? | | |
   | Your `AC-n` IDs preserved (or need mapping)? | | |
   | Anything you missed manually that the tool caught? | | |

- [ ] Side-by-side comparison completed; at least one thing the tool caught that you missed (or vice versa — both are findings)

---

## Step 4 — Plan and contracts: compare against Lab 9.2

1. `/speckit.plan <your sandbox's stack and constraints>` — then inspect the generated `plan.md`, `research.md`,
   `data-model.md`, and especially `contracts/`.
2. Compare the generated contract with your Lab 9.2 contract:

   | Check | Lab 9.2 contract | Spec Kit contract |
   |---|---|---|
   | Naming follows repo conventions (`ApiError`, error-code scheme) | | |
   | Error cases trace to acceptance criteria / NFRs | | |
   | No fields/endpoints beyond the spec | | |
   | Consistent with the ADR's decision | | |

3. If the tool's answer conflicts with your ADR or conventions, note it — this is exactly the kind of drift a
   human review catches, and a reason the constitution and conventions must be in context.

- [ ] Contract comparison completed; convention/traceability gaps recorded

---

## Step 5 — Checklist, tasks, analyze: traceability, mechanized

1. `/speckit.checklist` — review the requirements-quality checklist as the spec's reviewer (unchecked items are a
   gate later, not a formality).
2. `/speckit.tasks` — inspect whether every acceptance criterion maps to tasks, and whether any task traces to no criterion.
3. `/speckit.analyze` — the read-only consistency check across `spec.md`, `plan.md`, and `tasks.md`. Record every
   conflict, gap, and ambiguity it reports. **Fix issues at the source** (spec/plan), then re-run — do not patch `tasks.md`.

- [ ] `tasks.md` maps criteria → tasks (or gaps are listed)
- [ ] `/speckit.analyze` output captured; issues fixed at source and re-run clean (or remaining findings explained)

---

## Step 6 — Implement and converge (thin slice only)

1. `/speckit.implement` — note the built-in gate: if checklist items are unchecked, it asks before proceeding.
   Answer deliberately (the same approval discipline as Lab 9.3, now enforced by the tool).
2. Keep it to the first phase / thin slice; apply Module 6 review discipline to every diff and command.
3. Run `<test-command>`; then `/speckit.converge` — it checks the codebase against spec/plan/tasks and appends gap
   tasks until it reports **Converged**. Compare its coverage verdict with your manual `traceability.md`: which
   criteria did each approach verify, and which did each miss?
4. Commit in the scratch clone as evidence.

- [ ] Implementation + `<test-command>` output captured in the scratch clone
- [ ] `/speckit.converge` output captured; compared with your manual traceability matrix
- [ ] Commit hash in the scratch clone recorded

---

## Step 7 — Debrief: tool vs. discipline (mandatory, 5 min)

Fill this in — it is the actual deliverable of this extension lab:

| Dimension | Manual (Labs 9.1–9.3) | GitHub Spec Kit |
|---|---|---|
| Setup / adoption cost | None | |
| Artifact structure | You decide | Standardized |
| Traceability mechanism | Your `AC-n` IDs + matrix | |
| Human approval gates | Explicit, yours | |
| Customization (templates/constitution) | Total freedom | |
| Fit for your sandbox repo | | |

**Adoption recommendation** (2–3 sentences): Would you adopt Spec Kit for this repository? For which kinds of
work, and what would you keep manual? Reference the rigor spectrum (guide §3) — not everything needs either SDD
*or* a toolkit.

- [ ] Debrief table + recommendation written (this is what your facilitator reviews)

---

## Evidence

- `specify` version, command names, and `.specify/` + command-file listing from the scratch clone
- Constitution draft + overlap notes vs. Module 8
- Generated `spec.md` + side-by-side comparison with your manual spec (Step 3 table)
- Generated `contracts/` + comparison with Lab 9.2 contract
- `/speckit.analyze` output (before/after fix) and `/speckit.converge` output vs. your `traceability.md`
- Debrief table + adoption recommendation

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `specify: command not found` | `uv` tool bin dir not on `PATH` | `uv tool update-shell`, restart the terminal, or `pipx install specify-cli` |
| `uv` not installed / installs blocked | Locked-down seat | Use `pipx`, a pinned `uvx` run, or the Step 1 tabletop path — note it for the facilitator |
| Init refuses on a non-empty directory | Existing files | `--force` is expected here — but only ever in the scratch clone; never in your lab repo |
| Slash commands not found in chat | Wrong integration selected, or newer/older CLI naming | Check with `specify init --help`; try `--integration cursor` vs `--ai cursor`; look for `/speckit.specify` vs `/speckit-specify` under `/` in chat |
| Spec Kit's commands don't appear in Cursor | Command files generated elsewhere or not committed/checked out | Inspect the generated agent directory in the scratch clone; re-run `specify init --here --force` with the right integration |
| Generated spec lacks your `AC-n` IDs | You passed your *finished* spec instead of the raw ticket, or the tool uses its own IDs | Pass the raw ticket; maintain an ID mapping table if you need cross-tool traceability |
| `/speckit.analyze` flags conflicts | The intended behavior — artifacts drifted | Fix at the source (spec/plan), re-run; do not edit `tasks.md` to hide it |
| `/speckit.implement` runs long / over-builds | Checklist gate bypassed or all tasks in scope | Stop, review diffs, scope to one phase; the gate is the lesson |
| Commands typed in the terminal do nothing | They're agent skills, not shell commands | Invoke them in Cursor chat |
| Init overwrote files in the sandbox repo | Scratch-clone rule skipped | Restore with `git checkout -- .` / `git stash`; rerun in a clean clone |

---

## Checkpoint questions

1. Which Spec Kit phases correspond to Module 9's spec, plan, and traceability steps?
2. Where is the human approval gate in the Spec Kit workflow — and does the tool remove it?
3. What does `/speckit.analyze` check, and how does `/speckit.converge` differ from it?
4. When is adopting Spec Kit worth its setup cost?

<details>
<summary>Answers</summary>

1. `/speckit.specify` (+ `clarify` / `checklist`) ↔ the spec with testable criteria; `/speckit.plan` ↔ architecture, contracts, and the design artifacts; `/speckit.tasks` + `/speckit.analyze` ↔ clause-to-work traceability; `/speckit.implement` + `/speckit.converge` ↔ implementation and spec-to-code/test verification.
2. Still human, still between every phase: you review each artifact before invoking the next command, and `/speckit.implement` even gates on unchecked checklist items. The tool standardizes artifacts and adds consistency checks — it does not approve them.
3. `/speckit.analyze` is a read-only consistency/coverage pass across spec, plan, and tasks (fix at the source and re-run). `/speckit.converge` compares the implemented codebase against all three and appends gap tasks until it reports converged — a correction loop, not just a report.
4. When the team wants a standardized, tool-agnostic SDD process with built-in quality gates across sessions and agents — production features and multi-session work. Same test as choosing SDD itself (guide §3): the setup cost isn't justified for spikes or small single-session fixes.

</details>

---

## Next

**Module 10** — Agent, Skill & Subagent Architecture Fundamentals: the spec artifacts (manual, or Spec Kit-generated) become the inputs agents are formally defined to operate against. **Module 11** extends this same spec into reusable requirement-analysis, test-generation, validation, and documentation agents — Spec Kit's constitution/spec/plan/tasks chain is one concrete model for how those agents' outputs must compose.

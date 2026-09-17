# Lab 8.3 — Skill, Prompt Template & the Starter-Kit Commit

**Module 8 · Rules, AGENTS.md, Skills & Team Standards | Xebia — Cursor AI Training**
Day 2 · Lab 3 of 3 · ~20–25 minutes · Individual

> **Objective:** package one reusable capability as a Skill (invoked on demand, not loaded into every conversation),
> turn a recurring prompt into a parameterized template, verify both against sample tasks, and commit the whole
> starter kit as the team's first AI asset library.

**Guide references:** Module 8, §4 (Skills), §5 (prompt templates), §6 (team standardization), §7 (version-controlled, concise, testable)
**Learning objectives covered:** 4 — Skills; 5 — templates; 6 — team standardization; 7 — instructions as code.

---

## Before you start

- Labs 8.1–8.2 complete, still on `module8-lab`
- Pick `<skill-name>` and `<recurring-task>` — a recognizable task type worth packaging, e.g.:
  - "write an ADR" / "generate release notes" / "review a PR description" / "scaffold a new endpoint"
- Rule of thumb for the format decision: a **rule** shapes ongoing behavior; a **template** is one
  fill-in-the-blanks prompt; a **skill** is a matchable capability invoked for a task type, possibly with
  scripts/reference material (guide §4)

---

## Step 1 — Choose: template or skill?

| Candidate | Best format | Why |
|---|---|---|
| A single parameterized prompt (e.g., test generation) | Template | One fill-in-the-blanks instruction, no bundled material |
| A multi-step workflow (e.g., "write an ADR": gather context → draft → review checklist) | Skill | Distinct task type, several steps, benefits from bundled guidance |
| A standing convention (e.g., error handling style) | Rule (Lab 8.1) | Always/context-scoped behavior, not a task |

- [ ] Format chosen for `<recurring-task>` and justified: `____________`

---

## Step 2 — Create the Skill

1. Easiest path: type `/create-skill` in Agent chat and describe the capability — Cursor's built-in skill walks
   through structure and saves it. Or create manually:

   ```text
   .cursor/skills/<skill-name>/SKILL.md
   ```

2. Required frontmatter: `name` (must match the parent folder, lowercase-with-hyphens) and `description` (what it
   does **and when to use it** — this is how the agent matches tasks to it):

   ```markdown
   ---
   name: <skill-name>
   description: <What this capability does. Use when the user asks for <trigger phrases>.>
   ---

   # <Skill title>

   ## Steps
   1. <step>
   2. <step>

   ## References
   - See `references/<file>.md` for <detail> (optional)
   ```

3. Optionally add `scripts/`, `references/`, or `assets/` directories if the capability needs them. Keep the main
   `SKILL.md` focused — detail belongs in `references/` (loaded only when needed).
4. Discoverability check: open Cursor Settings (`Cmd/Ctrl+Shift+J`) → Rules; your skill should appear under the
   **Agent Decides** section.

- [ ] `SKILL.md` created with valid `name` + `description`; folder name matches `name`
- [ ] Skill visible in Settings → Rules → Agent Decides

---

## Step 3 — Test the Skill

1. **Manual invocation first** (proves it loads): in Agent chat, type `/` and pick `<skill-name>`, then give it a
   sample input.
2. **Automatic match second** (proves the description works): in a new chat, phrase a request that should match the
   description — e.g., "We need an ADR for the `<feature>` decision" — and see whether the agent pulls the skill in.
3. If it doesn't trigger, the description is the problem: name the trigger phrases explicitly ("Use when…").

- [ ] Transcript: manual `/` invocation produced the expected workflow
- [ ] Transcript: description-based match confirmed (or description revised and re-tested)

---

## Step 4 — Create the parameterized prompt template

Write one fill-in-the-blanks instruction with the §5 elements — as an Apply-Manually rule in `.cursor/rules/`
(invoked via `@`-mention) or a committed markdown doc if your team prefers (follow your facilitator):

```markdown
---
# no description/globs/alwaysApply — this rule is invoked manually
---

# <Template name>

**Purpose:** <one line>
**Inputs:** `{input_1}`, `{input_2}`, `{input_3}`
**Fixed instructions:** <tooling/conventions to always apply, e.g., use pytest and existing fixtures>
**Expected output:** <what good looks like, e.g., a test file matching project conventions>
```

Example row from the guide: purpose "Generate a unit test suite for a given function"; inputs
`{function_name}`, `{file_path}`, `{edge_cases_to_cover}`; fixed instructions "use `<test-command>` tooling, follow
existing fixture patterns"; output "a test file matching the project's test conventions".

- [ ] Template has all four elements; inputs are clearly parameterized
- [ ] `@`-mention it in chat with real inputs and confirm consistent output (transcript)

---

## Step 5 — Test everything against sample tasks (the quality bar)

Run the §7 checklist over your rule, `AGENTS.md`, skill, and template:

| Quality bar | Your artifact passes? |
|---|---|
| **Concise** — instruction + brief reason, no restated obviousness | [ ] |
| **Testable** — you ran a sample task and confirmed behavior | [ ] |
| **Maintainable** — clear owner, reviewed like code, updated when stale | [ ] |
| **Version-controlled** — goes through commit/review, not someone's head | [ ] |

- [ ] Every artifact tested with a concrete sample task (transcripts/notes attached to evidence)

---

## Step 6 — Commit the starter kit (foundation for Modules 9 & 11)

One reviewable change containing everything:

```bash
git status          # confirm exactly: .cursor/rules/..., AGENTS.md, .cursor/skills/...
git add .cursor/ AGENTS.md
git commit -m "Module 8 lab: add team AI starter kit (rule, AGENTS.md, skill, template)"
git log --oneline -1
```

- [ ] Starter kit committed as one coherent change; hash `____________`
- [ ] Ready to state what Module 9 (SDD) and Module 11 build on: the specs, agents, and prompts that will live alongside these artifacts

---

## Evidence

- Format decision table (Step 1)
- `SKILL.md` + Settings → Rules screenshot
- Skill invocation transcripts (manual + automatic)
- Prompt template + `@`-mention transcript
- Quality-bar checklist + starter-kit commit hash

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Skill never auto-invoked | `description` doesn't state *when* to use it | Rewrite with explicit trigger phrases ("Use when the user asks to…") and re-test |
| Skill name rejected / not found | `name` doesn't match parent folder, or uses capitals/underscores | Lowercase-with-hyphens, folder and `name` identical |
| Agent doesn't know the skill exists | Wrong skills directory | Project: `.cursor/skills/<name>/SKILL.md`; confirm discovery in Settings → Rules |
| Template drifts between users | Instruction too loose | Tighten "fixed instructions" and "expected output"; re-test with the same inputs |
| Skill wants to run scripts that don't exist | Referenced but not created | Add them under `scripts/` or remove the reference — keep the skill self-contained |
| Commit includes unrelated files | `git add .cursor/ AGENTS.md` wasn't scoped, or Module 7 branch debris | `git status` before staging; check the branch is `module8-lab` |

---

## Checkpoint questions

1. When would you package something as a Skill rather than just a prompt template?
2. What do a rule, a skill, and a template each do — in one sentence each?
3. Why does version-controlling rules and skills matter for a team?

<details>
<summary>Answers</summary>

1. When the capability is a distinct, recognizable task type with multiple steps or bundled reference material beyond a single fill-in-the-blanks prompt.
2. A rule shapes how the agent behaves generally or in a scoped context; a skill is a matchable capability invoked for a specific task type; a template is a parameterized prompt with defined inputs and expected output.
3. They're instructions as code: version control makes changes reviewable, testable, and maintainable, and puts the standards in the repository where every teammate and every agent inherits them.

</details>

---

## Next

Day 2 is complete — and your Day-3 foundation is committed. **Module 9 — AI-Assisted Design & Spec-Driven Development** turns these durable instructions into specs as the source of truth for agent-generated code.

# Lab 12.1 — Context Engineering & Grounding Sources

**Module 12 · Context Engineering, Knowledge Grounding & MCP | Xebia — Cursor AI Training**
Day 4 · Lab 1 of 3 · ~15 minutes · Individual, pair check

> **Objective:** practice the three moves of context engineering — **select, structure, scope** — on a real
> engineering question, map the five grounding source categories to your repository, and configure the direct
> repo/SDS/standards grounding setup the walkthrough runs on. No building: this is the configuration half of the
> deck's walkthrough.

**Guide references:** Module 12, §1 (context engineering), §2 (grounding sources); hands-on walkthrough step 1
**Learning objectives covered:** 1 — select/structure/scope context; 2 — identify and use the five grounding sources.

---

## Before you start

- Branch: `git switch -c module12-lab` from `module11-lab` (Module 9 spec, Module 8 rules, and the Module 11 library all stay available)
- Copy the grounding corpus into your repo (originals stay read-only):

```bash
mkdir -p knowledge
cp labs/module-12/samples/knowledge-base/* knowledge/
git status        # knowledge/ is new — it will be committed later
```

- Create `notes/module12/grounding-setup.md`
- Keep the walkthrough question in view — **GQ-1** from [`samples/grounding-questions.md`](samples/grounding-questions.md):
  *"Does our rate-limiting design account for the API gateway's own limits, and have we hit a problem with this before?"*

---

## Step 1 — Apply the three moves to GQ-1

Fill this in `grounding-setup.md`:

| Move | Your answer |
|---|---|
| **Raw need** | GQ-1, in your own words |
| **Select** — candidate sources | List everything you *could* hand over (whole repo, all tickets, full git history, every doc…), then mark each **relevant / noise** with a one-line reason |
| **Structure** | For each selected source: excerpt, summarized pattern, or full file? (e.g., defect log → the one recurring pattern, not all 140 entries) |
| **Scope** | Bound it: which files/sections, what is explicitly excluded, rough size (lines or pages) |

- [ ] Select list includes at least two tempting-but-irrelevant sources you deliberately rejected
- [ ] Structure step names the form each source takes in context (not just "include the file")
- [ ] Scope step states an explicit exclusion and a rough size bound

---

## Step 2 — Map the five grounding sources

For each source class, say what it contributes, where it lives, and whether it exists for you today.

| Source class | What it contributes | Where it lives (path/system) | Available? | Risk if missing |
|---|---|---|---|---|
| Repository code | | | | |
| SRS / SDS documents | | | | |
| Standards | | | | |
| Historical defect log | | | | |
| Enterprise knowledge | | | | |

- [ ] All five mapped; the last two are **new in this module** — use `knowledge/defect-log.md` and `knowledge/runbook-api-gateway.md` as the shipped examples
- [ ] At least one source is marked missing **for your organization**, with a note on where it would come from and who owns it

---

## Step 3 — Configure the direct grounding setup (walkthrough step 1)

Document the exact setup in `grounding-setup.md` so a teammate could reproduce it:

| Source | Exact path / handle | How it enters the chat |
|---|---|---|
| Repository code | e.g. `src/middleware/rate_limit_middleware.py` (or your repo's equivalent) | `@`-mention / open file |
| SRS / SDS | `specs/<feature>/spec.md`, `specs/<feature>/architecture.md` | `@`-mention |
| Standards rule | `.cursor/rules/<rule-file>.mdc` | auto-loaded or `@`-mentioned |
| Knowledge corpus | `knowledge/` (SDS excerpt, runbook, defect log, code excerpt) | direct files for now — MCP in Lab 12.2 |

- [ ] Every path resolves on disk (open each one)
- [ ] The note states what is **not** included (e.g., the whole repo, unrelated specs) and why

---

## Step 4 — Choose the mechanism (preview of §7)

For each source, decide the right delivery mechanism — and why a heavier one isn't warranted.

| Source | Mechanism: direct repo context / rules-skills / MCP | Why |
|---|---|---|
| Repository code | | |
| Standards | | |
| Historical defect log | | |
| Enterprise wiki (hypothetical) | | |

- [ ] At least one row where you chose **direct context over MCP** — and can say what an unnecessary MCP server would cost to maintain

---

## Evidence

- `notes/module12/grounding-setup.md` — three-move table (GQ-1), five-source map, configured setup with paths, mechanism choices
- `knowledge/` populated from the fixtures (`git status` shows the new directory)

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| "Select" step kept everything | No noise criterion | Ask: does this source change the answer to *this* question? If not, it's noise, not completeness |
| Structure step is "paste the files" | Skipped summarization | Extract the relevant paragraph/section or the recurring pattern; note the size difference |
| Corpus copy missing files | Copied individual files | Copy the whole `knowledge-base/` directory, then verify with `ls knowledge/` |
| Spec paths don't resolve | Different Module 9 layout | Use your actual paths; the setup note must match reality, not the example |
| Mechanism table says MCP for everything | Reaching for the heaviest tool | Direct context for in-session material; rules for standing instructions; MCP only for external systems (deck §08) |

---

## Checkpoint questions

1. What are the three moves of context engineering, and what does each prevent?
2. Why is "more context" often worse context?
3. When is MCP the right mechanism — and when is it overkill?

<details>
<summary>Answers</summary>

1. **Select** (which sources are relevant) prevents noise; **structure** (organize/extract) prevents dilution by volume; **scope** (bound size/specificity) prevents blowing the context window and cost budget on material nobody reads.
2. Relevant signal gets diluted by irrelevant volume — the agent reasons over noise, and token/cost budgets are spent on context that doesn't change the answer.
3. MCP is right when the material lives in an **external** system or needs a live lookup/action beyond the repo. It's overkill when the material is already in the session (direct context) or is a standing instruction (a rule) — then an MCP server just adds something to maintain.

</details>

---

## Next

**Lab 12.2 — MCP: Connect or Inspect.** You'll wire (or inspect) an MCP server over the `knowledge/` corpus, identify its Resources and Tools, and match retrieval strategies to question shapes.

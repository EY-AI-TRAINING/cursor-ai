# Lab 4.3 — Analysis Prompts & Conversation Context Limits

**Module 4 · AI Chat, Context & Ask Mode | Xebia — Cursor AI Training**
Day 1 · Lab 3 of 3 · ~15–20 minutes · Individual · Read-only

> **Objective:** build a strong analysis prompt from its three ingredients, verify it says "not addressed" instead
> of guessing, then deliberately run a thread long enough to feel context degradation — and recover from it.

**Guide references:** Module 4, §4 (context scoping), §5 (history and context limits), §6 (analysis-task prompting)
**Learning objectives covered:** 4 — deliberate scoping; 5 — managing conversation history/limits; 6 — analysis-task prompts.

---

## Before you start

- Module 3 complete; Lab 4.1 comparison done (you know how scope changes answers)
- Keep the **same pinned model** you used in Lab 4.1
- Pick a real sandbox question with a checkable answer, e.g. session/error handling, input validation,
  or what breaks if `<target-function>` changes

---

## Step 1 — Build the prompt from its ingredients

Three ingredients make a reliable analysis answer (guide §4 and §6):

1. **Specific question** — one claim to check, not a topic to discuss
2. **Right-sized context** — 2–3 `@`-mentions, not everything
3. **Output constraints** — the format and the honesty clause

The analysis trio to bake in: **scope the evidence**, **demand citations**, **permit "I don't know"**.

Template to fill in:

> "@`<target-file>` @`<related-file>` — `<specific question>`. For each claim, cite the file and line numbers.
> If the evidence is insufficient to answer, say 'not addressed' rather than guessing. Return a table with columns:
> Requirement | Evidence (file:line) | Verdict (satisfied / violated / not addressed)."

1. Fill the placeholders with your sandbox question and send it.
2. Optional toggle drill: re-send with one ingredient removed each time (no output format; no citation instruction;
   vague question) and note how the answer degrades.

- [ ] Prompt written with all three ingredients
- [ ] Answer contains line-level citations and the requested table format
- [ ] One ingredient removed; degradation recorded

---

## Step 2 — Test the honesty clause

1. Ask about a clause that does not exist:

   > "`<target-file>` — does it comply with section `<N>` of `<spec-doc>`? If you find no evidence, state
   > 'not addressed'."

2. Record: did it decline, or invent? If it invented, re-anchor explicitly — *"Only use the attached files; make no
   outside assumptions"* — and re-test.

- [ ] "Not addressed" observed (or the re-anchor fixed the behavior)

---

## Step 3 — Blast-radius analysis (citation-demanding)

1. In a new chat, ask:

   > "List every caller of `<target-function>` and describe what breaks if its signature changes. Cite file:line
   > for each caller; if you cannot find a caller, say so."

2. Spot-check two callers in the repo. Record any the answer missed — retrieval is best-effort, citations are how
   you catch it.

- [ ] Caller list grounded with citations; at least one spot-checked
- [ ] Any missed caller recorded as a finding

---

## Step 4 — Take a thread too far (on purpose)

1. Stay in the **same chat** and continue with 4–6 related-but-different follow-ups (no new chats).
2. Then ask: *"Summarize the decisions and constraints we've established in this conversation so far."*
3. Compare the summary against what actually happened across the thread. Look for: dropped constraints, vaguer
   answers, citations that stop appearing, forgotten instructions.

- [ ] Degradation symptom observed and recorded (or a reasoned explanation of why it didn't appear)

---

## Step 5 — Mitigate: new chat + explicit re-anchor

1. Start a **new chat** for the next question and begin with an explicit re-anchor line:
   > "Context: we established `<X, Y, Z>`. Question: `<...>`"
2. Ask the same question in the old, long thread and compare. The fresh-chat re-anchored answer should be tighter
   and better cited.
3. Write your habits list:
   - new chat per topic
   - explicitly re-state key facts in long threads
   - chat is a scratchpad, not an archive — durable decisions go in a spec/ADR/ticket (Module 9)

- [ ] Fresh-chat re-anchored answer compared against the long thread
- [ ] Habits list recorded (3 lines)

---

## Evidence

- Analysis prompt with all three ingredients + the degradation variant
- The "not addressed" result from Step 2
- Thread summary vs. reality notes from Step 4
- Fresh-chat re-anchor comparison from Step 5

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Model always answers, never says "not addressed" | Honesty clause missing or too weak | Restate: "Only use attached context; if evidence is insufficient, say so explicitly" |
| Thread never seems to degrade | Questions were small; budget not strained | Good news — still adopt the new-chat-per-topic habit |
| Citations are off by a line or two | Model approximation | Verify against the file; that's exactly why citations are demanded |
| New chat "forgets" needed history | That's the point of a new chat | Re-anchor the key facts explicitly in the first message |
| Answers get slower/costlier over the thread | Growing context budget (every turn is re-read) | Start a new chat; scope with `@`-mentions |

---

## Checkpoint questions

1. What three things should a well-formed **analysis** prompt do that a generation prompt might not need?
2. Name one practical habit for managing a long-running conversation's context budget.
3. How do the failure modes differ between a generation task and an analysis task?

<details>
<summary>Answers</summary>

1. Scope the evidence explicitly, demand citations to specific lines/files, and permit the model to say
   "insufficient evidence" rather than guessing.
2. Any one of: start a new chat when switching topics; explicitly re-state key facts in long conversations; treat
   chat as a scratchpad, not the durable record.
3. A bad generation answer usually produces code that fails a test; a bad analysis answer produces a confident,
   wrong opinion with no built-in check — hence citations and the honesty clause.

</details>

---

## Next

**Module 5 — Inline Code Generation, Tab & Context** moves from asking questions to generating code in the editor.

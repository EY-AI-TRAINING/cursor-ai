# Gate-log excerpt — broken trail (`req-2481-run-01`)

> **Fixture for Module 17 (Lab 17.3).** The gate log from a run, reproduced as found. The trail cannot
> answer "why was this allowed through, and by whom or what?". Do not edit this fixture — define the
> schema and rewrite the worst entries in `notes/module17/gate-log-schema.md`.

```jsonc
{"ts":"2026-09-23T11:02:10Z","run_id":"req-2481-run-01","gate":"G3","decision":"FAIL","detail":"markers missing"}
{"ts":"2026-09-23T11:09:12Z","run_id":"req-2481-run-01","gate":"G3","decision":"PASS"}
{"ts":"2026-09-23T11:15:40Z","run_id":"req-2481-run-01","gate":"G4","decision":"PASS","note":"sandbox 503 during execution — ran again later, looked fine"}
{"ts":"2026-09-23T11:22:03Z","gate":"G5","decision":"PASS","decided_by":"automated"}
{"ts":"2026-09-23T11:31:55Z","run_id":"req-2481-run-01","gate":"G5","decision":"APPROVED"}
{"ts":"2026-09-23T11:34:20Z","run_id":"req-2481-run-01","gate":"G3","decision":"PASS","error":"gate script exited non-zero (KeyError: 'checks')"}
```

**Questions the current log cannot answer (write the schema that can):**

- Which version of the gate criteria produced each verdict?
- Which artifact — at which revision — was judged?
- Which specific check failed, and what did it observe vs. expect?
- Who or what decided (`automated`, `llm-judge@version`, `human:<role>`), and why?
- Where did a FAIL route to?
- What happened when the gate script itself crashed — and why is entry 6 dangerous?

---

*Fixture for Module 17 — read-only. Some entries are incomplete; at least one is fail-open and must never
be recorded that way.*

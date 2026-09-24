# Handoff envelopes — run `req-2481-run-09`

> **Fixture for Module 15 (Labs 15.1–15.3).** The five envelopes below are the raw handoffs from one pipeline
> run, reproduced **as produced**. The design says every handoff is a typed envelope (guide §1); the run shows
> what the orchestrator actually passed. Do not edit this fixture — repair the envelopes in your own
> `orchestration/handoff-envelope.md`.

## Envelope 1 — Requirement Validator

```jsonc
{
  "stage": "req-validator",
  "reply": "Requirement looks solid, proceeding.",
  "ts": "2026-09-23T10:02:44Z"
}
```

## Envelope 2 — Sequence Builder

```jsonc
{
  "pipeline_run_id": "req-2481-run-09",
  "stage": "sequence_builder",
  "status": "PASS",
  "output": {
    "artifact_ref": "02_test_sequence.json",
    "summary": "5 scenarios derived from 4 acceptance criteria"
  },
  "attempt": 1
}
```

## Envelope 3 — Test Generator

```jsonc
{
  "stage": "test_generator",
  "status": "DONE",
  "quality": "high",
  "artifact_ref": "03_tests/",
  "attempt": 2,
  "metrics": { "tokens_in": 58000, "tokens_out": 13000, "tool_calls": 12, "duration_s": 420 }
}
```

## Envelope 4 — API Validator

```jsonc
{
  "pipeline_run_id": "req-2481-run-09",
  "stage": "api_validator",
  "status": "FAIL",
  "output": { "summary": "1 of 6 tests fails against openapi.yaml" },
  "open_issues": ["generator should try again"],
  "attempt": 1
}
```

## Envelope 5 — Reviewer

```jsonc
{
  "pipeline_run_id": "req-2481-run-09",
  "stage": "reviewer",
  "status": "PASS",
  "input": ["02_test_sequence.json", "generator_run_summary.md"],
  "note": "The generator's approach is sound and matches the sequence. Formatting is consistent.",
  "attempt": 1
}
```

## What the schema says every handoff must carry

For reference — the intent the run was supposed to follow (guide §1):

```jsonc
{
  "pipeline_run_id": "req-2481-run-09",
  "stage": "sequence_builder",
  "stage_version": "1.3.0",
  "status": "PASS",                       // PASS | FAIL | NEEDS_HUMAN
  "input_ref": "01_validated_requirement.md#sha:9f2c…",
  "output": {
    "artifact_ref": "02_test_sequence.json",
    "summary": "7 test steps derived from 4 acceptance criteria"
  },
  "evidence": ["spec/REQ-2481.md#AC-1..AC-4", "openapi.yaml#/orders"],
  "assumptions": ["Auth token is provided by fixture, not tested here"],
  "open_issues": [],
  "attempt": 1,
  "metrics": { "tokens_in": 6120, "tokens_out": 1480, "tool_calls": 3, "duration_s": 41 }
}
```

---

*Sample fixture for Module 15 — read-only. Defects are deliberate; every envelope above is missing, mis-typed,
or leaking something the next stage should not see.*

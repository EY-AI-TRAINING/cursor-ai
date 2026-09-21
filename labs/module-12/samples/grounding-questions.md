# Grounding test questions

> **Fixture for Module 12 (Lab 12.3).** Ask each question in a **fresh chat** with only the grounded sources
> attached (repo code + SRS/SDS + standards rule + the `knowledge/` corpus). The "required behaviour" column is
> what a grounded answer must do — it does not give the answer away.

| # | Question | Required behaviour |
|---|---|---|
| **GQ-1** | "Does our rate-limiting design account for the API gateway's own limits, and have we hit a problem with this before?" | Every claim cites its source (SDS excerpt, runbook, and/or defect log). If part of the question has no support in the sources, that part is flagged, not guessed. |
| **GQ-2** | "Where in the request path is the rate-limit check invoked, and what headers does the response carry?" | Answer cites repository code (`file` and, if possible, line); no invented function names or headers. |
| **GQ-3** | "What is our SOC 2 audit-evidence retention period?" | **Declines**: states that nothing in the provided sources supports an answer. Must **not** present the gateway log's 30-day retention as the audit-evidence policy. |

**Citation spot-check (after each answer):** open at least one cited source and confirm the claim is actually
there. A citation that doesn't hold is worse than no citation — it looks verifiable but isn't.

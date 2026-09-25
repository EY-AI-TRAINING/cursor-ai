# Seeded faults — REQ-2502

**None needed.** Round 0 failed naturally with two findings:

- F-1 — `test_audit_entry_recorded_newest_first` asserted oldest-first (TEST_DEFECT).
- F-2 — 281-character `reason_note` accepted (PRODUCT_DEFECT → DEF-5561).

CA-7 is satisfied by a real correction round. A deliberately seeded fault is a legitimate
technique **only when disclosed**; if your first round passes cleanly, seed one (for example,
remove an `@pytest.mark.ac` marker) and record here:

| Fault | Where | Detection that caught it | Disclosed in report § |
|---|---|---|---|
| — | — | — | — |

An undisclosed seeded fault is misrepresentation, not testing.

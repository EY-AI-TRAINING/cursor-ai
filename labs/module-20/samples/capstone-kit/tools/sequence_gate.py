#!/usr/bin/env python3
"""Reference G1/G2 checks over the bundle and test sequence (Module 20 §4).

    python3 tools/sequence_gate.py --run req-2502-run-01

G1 `requirement_ready`: every AC is present; any llm-extracted AC must be confirmed.
G2 `sequence_coverage`: unique scenario ids; every scenario lists `ac_ids`; every AC is
covered; every error criterion (bundle text mentions 422/reject/unknown/invalid) has at
least one negative or boundary scenario.

Exit 0 PASS, 1 FAIL (findings printed).
"""
import argparse
import json
import pathlib
import sys


def main():
    parser = argparse.ArgumentParser(description="G1/G2 sequence checks")
    parser.add_argument("--run", required=True)
    args = parser.parse_args()

    run = pathlib.Path("runs", args.run)
    bundle = json.loads((run / "00_requirement_bundle.json").read_text())
    sequence = json.loads((run / "02_test_sequence.json").read_text())
    acs = {a["id"]: a for a in bundle.get("acceptance_criteria", [])}
    scenarios = sequence.get("scenarios", [])
    findings = []

    if not acs:
        findings.append(("G1_requirement_ready", "bundle has no acceptance criteria"))
    for ac_id, ac in acs.items():
        if ac.get("extracted_by") == "llm" and ac.get("status") != "confirmed":
            findings.append(("G1_requirement_ready",
                             f"{ac_id} is llm-extracted and not confirmed (status={ac.get('status')})"))

    ids = [s.get("id") for s in scenarios]
    if len(ids) != len(set(ids)):
        findings.append(("G2_sequence_coverage", "duplicate scenario ids"))
    covered = set()
    for scenario in scenarios:
        if not scenario.get("id"):
            findings.append(("G2_sequence_coverage", "scenario without an id"))
        ac_ids = scenario.get("ac_ids") or []
        if not ac_ids:
            findings.append(("G2_sequence_coverage", f"{scenario.get('id')} lists no ac_ids"))
        covered.update(ac_ids)

    missing = sorted(set(acs) - covered)
    if missing:
        findings.append(("G2_sequence_coverage", f"ACs without scenarios: {missing}"))

    error_markers = ("422", "reject", "unknown", "invalid")
    for ac_id, ac in acs.items():
        text = (ac.get("text") or "").lower()
        if any(marker in text for marker in error_markers):
            types = {s.get("type") for s in scenarios if ac_id in (s.get("ac_ids") or [])}
            if not types & {"negative", "boundary"}:
                findings.append(("G2_sequence_coverage",
                                 f"{ac_id} is an error criterion with no negative/boundary scenario"))

    if findings:
        print("G1/G2: FAIL")
        for gate, detail in findings:
            print(f"- {gate}: {detail}")
        sys.exit(1)

    print(f"G1/G2: PASS — {len(acs)} ACs, {len(scenarios)} scenarios, all covered; "
          f"every error criterion has negative/boundary coverage")


if __name__ == "__main__":
    main()

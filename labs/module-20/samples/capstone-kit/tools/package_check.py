#!/usr/bin/env python3
"""Reference `package_check.py` — CA-1…CA-10 as code (Module 20 §10).

Exit 0 if all required rows pass, else 1. A floor, not a verdict: it checks existence,
hashes, sets and ordering; judgement belongs to the reviewer and the peer review.

Usage (from the capstone root, where capstone.yaml lives):
    python3 tools/package_check.py
"""
import glob
import hashlib
import json
import pathlib
import re
import sys

import yaml  # pyyaml, already used by the gate engine


def sha12(paths):
    h = hashlib.sha256()
    for p in sorted(paths):
        h.update(pathlib.Path(p).read_bytes())
    return h.hexdigest()[:12]


def jsonl(path):
    p = pathlib.Path(path)
    return [json.loads(line) for line in p.read_text().splitlines() if line.strip()] if p.exists() else []


def main():
    cfg = yaml.safe_load(pathlib.Path("capstone.yaml").read_text())
    t, run = cfg["ticket"], pathlib.Path("runs", cfg["run_id"])
    bundle_p, plan_dir = run / "00_requirement_bundle.json", pathlib.Path("plans", t)
    spec_p, rep = pathlib.Path("specs", f"{t}-spec-note.md"), pathlib.Path("reports", t)
    tests = glob.glob(cfg["tests_glob"])
    gates, runlog = jsonl(run / "gate_log.jsonl"), jsonl(run / "run_log.jsonl")
    rows = []

    def check(ca, ok, detail, required=True):
        rows.append((ca, "PASS" if ok else ("FAIL" if required else "INFO"), detail))

    # CA-1 — bundle
    acs = set()
    if bundle_p.exists():
        b = json.loads(bundle_p.read_text())
        acs = {a["id"] for a in b.get("acceptance_criteria", [])}
        unconfirmed = [a["id"] for a in b["acceptance_criteria"]
                       if a.get("extracted_by") == "llm" and a.get("status") != "confirmed"]
        check("CA-1", b.get("ticket", {}).get("id") == t and acs and not unconfirmed,
              f"{len(acs)} ACs; unconfirmed llm ACs: {unconfirmed or 'none'}")
    else:
        check("CA-1", False, "bundle missing")

    # CA-2 — plan approved, hash current, before generation
    appr_p = plan_dir / "plan_approval.json"
    if appr_p.exists() and (plan_dir / "plan.md").exists():
        a = json.loads(appr_p.read_text())
        fresh = a["approved_hashes"]["plan"] == sha12([plan_dir / "plan.md"])
        gen_ts = [e["ts"] for e in runlog if e.get("stage") == "test-generator"]
        before = bool(gen_ts) and a["ts"] < min(gen_ts)  # ISO-8601 UTC strings compare correctly
        check("CA-2", a["decision"] == "APPROVE" and fresh and before,
              f"approve={a['decision']} hash_fresh={fresh} before_generation={before}")
    else:
        check("CA-2", False, "plan.md or plan_approval.json missing")

    # CA-3 — spec note AC set equals bundle AC set
    spec_acs = set(re.findall(r"^#+\s*(AC-\d+)\b", spec_p.read_text(), re.M)) if spec_p.exists() else set()
    check("CA-3", bool(acs) and spec_acs == acs, f"spec={sorted(spec_acs)} bundle={sorted(acs)}")

    # CA-4 — sequence exists; every AC has a marked test; every test file has the req marker
    src = "\n".join(pathlib.Path(p).read_text() for p in tests)
    marked = set(re.findall(r'mark\.ac\("(AC-\d+)"\)', src))
    req_ok = bool(tests) and all(f'mark.req("{t}")' in pathlib.Path(p).read_text() for p in tests)
    check("CA-4", (run / "02_test_sequence.json").exists() and acs <= marked and req_ok,
          f"{len(tests)} test files; ACs without tests: {sorted(acs - marked) or 'none'}")

    # CA-5 / CA-6 — execution evidence and independent review
    check("CA-5", (run / "04_api_validation.json").exists(), "04_api_validation.json")
    check("CA-6", (run / "05_review_signoff.md").exists(), "05_review_signoff.md")

    # CA-7 — at least one correction round and a sign-off matching the current tests
    loops = sum(1 for e in gates if e.get("event") == "LOOP")
    signed = any(e.get("gate") == "HITL_signoff" and e.get("decision") == "APPROVE"
                 and e.get("approved_hashes", {}).get("tests") == sha12(tests) for e in gates) if tests else False
    check("CA-7", loops >= 1 and signed, f"LOOP events={loops} signoff_matches_current_tests={signed}")

    # CA-8 — readiness report from policy
    rr = rep / "readiness_report.md"
    decision = re.search(r"Decision:\s*\**\s*(NOT READY|READY)", rr.read_text()) if rr.exists() else None
    check("CA-8", decision is not None, f"readiness decision: {decision.group(1) if decision else 'missing'}")

    # CA-9 — final report links every stage + cost summary
    fr = rep / "final_engineering_report.md"
    needed = ["00_requirement_bundle.json", "plan.md", "spec-note", "02_test_sequence.json",
              "test_req_", "04_api_validation", "05_review_signoff", "readiness_report", "cost_summary"]
    missing = [n for n in needed if not fr.exists() or n not in fr.read_text()]
    check("CA-9", fr.exists() and not missing and (rep / "cost_summary.md").exists(),
          f"missing links: {missing or 'none'}")

    # CA-10 — optional delegation evidence
    check("CA-10", pathlib.Path("notes/capstone/delegation.md").exists(), "delegation.md", required=False)

    print("| CA | Result | Detail |\n|---|---|---|")
    for ca, res, detail in rows:
        print(f"| {ca} | {res} | {detail} |")
    sys.exit(0 if all(r != "FAIL" for _, r, _ in rows) else 1)


if __name__ == "__main__":
    main()

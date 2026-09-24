#!/usr/bin/env python3
"""DRAFT gate engine — read it, run it, find out why it cannot be trusted.

Evaluates one gate from gates.yaml and appends the verdict to gate_log.jsonl.
This draft was written quickly and never reviewed; the lab asks you to find the
planted defects before you build the real tools/gate_engine.py.
"""
import argparse
import ast
import datetime
import glob
import json
import pathlib
import subprocess
import sys

import yaml

CHECKS = {}
EXIT = {"PASS": 0, "FAIL": 1, "NEEDS_HUMAN": 0}


def check(fn):
    CHECKS[fn.__name__] = fn
    return fn


@check
def tests_collect(ctx):
    r = subprocess.run(["pytest", "--collect-only", "-q", *ctx["tests"]],
                       capture_output=True, text=True)
    if r.returncode == 0:
        return "PASS", "", []
    return "FAIL", r.stdout[-200:], [{"criterion": "tests must collect",
                                      "observed": r.stdout[-200:], "class": "TEST_DEFECT"}]


@check
def markers_present(ctx):
    missing = []
    for path in ctx["tests"]:
        for node in ast.walk(ast.parse(pathlib.Path(path).read_text())):
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                marks = " ".join(ast.unparse(d) for d in node.decorator_list)
                if "pytest.mark.ac" not in marks:
                    missing.append(node.name)
    if missing:
        return "FAIL", f"missing marker on {missing}", [
            {"test": t, "criterion": "every test has markers",
             "observed": "marker missing", "class": "TEST_DEFECT"} for t in missing]
    return "PASS", "", []


def evaluate(run_id, gate_id):
    run_dir = pathlib.Path("runs", run_id)
    entry = {"ts": datetime.datetime.now().isoformat(timespec="seconds"),
             "run_id": run_id, "gate": gate_id, "decided_by": "automated"}
    try:
        cfg = yaml.safe_load(pathlib.Path("gates.yaml").read_text())
        gate = cfg["gates"][gate_id]
        state = json.loads((run_dir / "state.json").read_text())
        ctx = {"run_dir": run_dir, "state": state,
               "tests": sorted(glob.glob("tests/test_req_2481_*.py"))}
        entry["gates_version"] = cfg["version"]
        decision = "PASS"
        for cid in gate["checks"]:
            if cid not in CHECKS:
                continue
            result, detail, findings = CHECKS[cid](ctx)
            entry.setdefault("checks", []).append({"id": cid, "result": result})
            if result == "FAIL":
                decision = "FAIL"
                entry["findings"] = findings
    except Exception as exc:
        decision = "FAIL"
        entry["error"] = f"{type(exc).__name__}: {exc}"
    if decision == "PASS":
        with open(run_dir / "gate_log.jsonl", "a") as log:
            log.write(json.dumps(entry) + "\n")
    return decision


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--gate", required=True)
    args = ap.parse_args()
    sys.exit(EXIT[evaluate(args.run, args.gate)])

#!/usr/bin/env python3
"""Offline kit helper: record real input hashes into runs/req-2481-run-02/state.json.

Run once after copying fixture-run/. Uses the same convention as the guide's sha():
sha256 over the sorted file contents, first 12 hex characters. Only stages that have
already run (status PASS or RUNNING) get their input_hash recorded; PENDING stages
stay stale by design.
"""
import glob
import hashlib
import json
import pathlib

RUN = "req-2481-run-02"
STATE = pathlib.Path("runs", RUN, "state.json")

READS = {
    "requirement-validator": ["requirements/REQ-2481.md", "specs/openapi.yaml"],
    "sequence-builder": [f"runs/{RUN}/01_validated_requirement.md", "specs/openapi.yaml"],
    "test-generator": [f"runs/{RUN}/02_test_sequence.json", "specs/openapi.yaml", "tests/conftest.py"],
    "api-validator": ["tests/test_req_2481_*.py", "specs/openapi.yaml"],
    "reviewer": ["requirements/REQ-2481.md", "tests/test_req_2481_*.py",
                 f"runs/{RUN}/04_api_validation_report.md"],
}


def expand(patterns):
    paths = set()
    for pattern in patterns:
        matches = sorted(glob.glob(pattern))
        if matches:
            paths.update(matches)
        elif pathlib.Path(pattern).exists():
            paths.add(pattern)
    return sorted(paths)


def sha(paths):
    digest = hashlib.sha256()
    for path in sorted(paths):
        digest.update(pathlib.Path(path).read_bytes())
    return digest.hexdigest()[:12]


def main():
    if not STATE.exists():
        raise SystemExit(f"{STATE} not found — copy fixture-run/ into runs/{RUN}/ first")
    state = json.loads(STATE.read_text())
    for stage, patterns in READS.items():
        info = state["stages"].get(stage, {})
        if info.get("status") not in ("PASS", "RUNNING"):
            continue
        paths = expand(patterns)
        info["input_hash"] = sha(paths) if paths else "none"
        print(f"{stage}: {info['input_hash']} ({len(paths)} input files)")
    STATE.write_text(json.dumps(state, indent=2) + "\n")
    print(f"{STATE} updated")


if __name__ == "__main__":
    main()

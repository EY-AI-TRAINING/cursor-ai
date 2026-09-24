#!/usr/bin/env python3
"""DRAFT rerun planner — decides which stages re-execute after a fix.

This is Lab 3's mental model written down: "the failing stage and everything after
it". The lab asks you to find the defects before building the real tools/rerun_plan.py.
"""
import os
import pathlib

ORDER = ["requirement-validator", "sequence-builder", "test-generator",
         "api-validator", "reviewer"]

READS = {
    "requirement-validator": ["requirements/{req}.md", "specs/openapi.yaml"],
    "sequence-builder": ["runs/{run}/01_validated_requirement.md", "specs/openapi.yaml"],
    "test-generator": ["runs/{run}/02_test_sequence.json", "specs/openapi.yaml"],
    "api-validator": ["tests/test_{req_l}_*.py", "specs/openapi.yaml"],
    "reviewer": ["tests/test_{req_l}_*.py", "runs/{run}/04_api_validation_report.md"],
}


def expand(pattern, req="REQ-2481", run=None):
    return [pathlib.Path(p.format(req=req, req_l=req.lower().replace("-", "_"), run=run))
            for p in pattern]


def newest_mtime(paths):
    return max(os.path.getmtime(p) for p in paths if pathlib.Path(p).exists())


def changed_since(state, stage, req="REQ-2481", run=None):
    last_run = state["stages"].get(stage, {}).get("last_run", 0)
    return newest_mtime(expand(READS[stage], req=req, run=run)) > last_run


def stale_stages(state, failing_stage, req="REQ-2481", run=None):
    """Rerun the failing stage and everything after it — simple and always safe."""
    start = ORDER.index(failing_stage)
    return [s for s in ORDER[start:] if changed_since(state, s, req=req, run=run) or s == failing_stage]

#!/usr/bin/env python3
"""DRAFT afterFileEdit hook — the early-feedback layer, as first written.

Planted defects: the lab asks you to find them before building the real
.cursor/hooks/after_edit_validate.py.
"""
import json
import sys

try:
    event = json.load(sys.stdin)
    path = event["path"]
    if path.endswith(".py"):
        with open("runs/hook_log.jsonl", "a") as log:
            log.write(json.dumps({"hook": "after_edit_validate",
                                  "target": path, "decision": "checked"}) + "\n")
except Exception:
    pass

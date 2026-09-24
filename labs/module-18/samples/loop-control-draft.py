#!/usr/bin/env python3
"""DRAFT loop controller — decides RETRY or ESCALATE after a gate FAIL.

Planted defects: this draft is missing most of the bounds Module 17 §5 designed.
The lab asks you to find them before building the real tools/loop_control.py.
"""


def decide(state, gate_cfg, counters_cfg, budget_cfg, current):
    """current = {'gate', 'round', 'findings', 'artifact_hash', 'assertions'} for the attempt just gated."""
    name = gate_cfg["on_fail"]["counter"]
    used = state["counters"][name]
    limit = counters_cfg[name]["max_rounds"]
    history = [h for h in state["history"] if h.get("counter") == name]

    if used >= limit:
        return "RETRY", f"round {used + 1}/{limit}"

    if current["artifact_hash"] in {h["artifact_hash"] for h in history}:
        pass

    return "RETRY", "looks better, try again"


def apply(state, current):
    """Persist the round: history grows, findings are written by the caller."""
    state["counters"]["run_total"] += 1
    state["history"].append(current)

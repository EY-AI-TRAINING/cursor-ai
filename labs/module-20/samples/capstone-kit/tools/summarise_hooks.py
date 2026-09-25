#!/usr/bin/env python3
"""Hook-log summary for the final report (Module 20 §7) — stdlib, so `jq` is optional.

    python3 tools/summarise_hooks.py --log runs/hook_log.jsonl

Prints counts per event/decision, then every deny/revert line that the report must
explain. Paste the output into reports/<ticket>/security.md and reference it from
the final report's governance section.
"""
import argparse
import collections
import json
import pathlib


def read_jsonl(path):
    p = pathlib.Path(path)
    return [json.loads(line) for line in p.read_text().splitlines() if line.strip()] if p.exists() else []


def main():
    parser = argparse.ArgumentParser(description="Summarise a hook log")
    parser.add_argument("--log", default="runs/hook_log.jsonl")
    args = parser.parse_args()

    hooks = read_jsonl(args.log)
    counts = collections.Counter((h.get("event", "?"), h.get("decision", "?")) for h in hooks)

    print(f"## Hook log summary — {args.log} ({len(hooks)} events)\n")
    print("| Event | Decision | Count |")
    print("|---|---|---:|")
    for (event, decision), count in sorted(counts.items()):
        print(f"| {event} | {decision} | {count} |")

    flagged = [h for h in hooks if h.get("decision") in ("deny", "revert")]
    print(f"\n### Denials and reverts ({len(flagged)}) — explain each in the report\n")
    if not flagged:
        print("- none")
    for h in flagged:
        print(f"- `{h.get('ts', '?')}` · {h.get('event', '?')} · {h.get('target', '?')} · {h.get('reason', 'no reason')}")


if __name__ == "__main__":
    main()

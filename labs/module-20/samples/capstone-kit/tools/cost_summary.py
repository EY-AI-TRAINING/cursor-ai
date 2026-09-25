#!/usr/bin/env python3
"""Reference `cost_summary.py` — observability/cost table from the run logs (Module 20 §9).

Usage:
    python3 tools/cost_summary.py --run req-2502-run-01 --usd-per-mtok 6.0 \
        > reports/REQ-2502/cost_summary.md

Consumes runs/<run>/run_log.jsonl and gate_log.jsonl plus runs/hook_log.jsonl.
The rate is a parameter, never a constant in code: prices differ by model and contract.
"""
import argparse
import collections
import json
import pathlib


def read_jsonl(path):
    p = pathlib.Path(path)
    return [json.loads(line) for line in p.read_text().splitlines() if line.strip()] if p.exists() else []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--usd-per-mtok", type=float, required=True, help="blended rate from your contract")
    args = ap.parse_args()

    run_dir = pathlib.Path("runs", args.run)
    runs = read_jsonl(run_dir / "run_log.jsonl")
    gates = read_jsonl(run_dir / "gate_log.jsonl")
    hooks = read_jsonl("runs/hook_log.jsonl")

    per_stage = collections.OrderedDict()
    for e in runs:
        s = per_stage.setdefault(e["stage"], {"attempts": 0, "tokens": 0, "seconds": 0, "last": ""})
        s["attempts"] += 1
        s["tokens"] += e.get("tokens", 0)
        s["seconds"] += e.get("duration_s", 0)
        s["last"] = e.get("status", "")

    print(f"# Observability & cost — {args.run}\n")
    print("| Stage | Attempts | Tokens | Minutes | Est. USD | Final status |")
    print("|---|---:|---:|---:|---:|---|")
    tot_tokens = tot_secs = 0
    for stage, s in per_stage.items():
        tot_tokens += s["tokens"]
        tot_secs += s["seconds"]
        usd = s["tokens"] / 1e6 * args.usd_per_mtok
        print(f"| {stage} | {s['attempts']} | {s['tokens']:,} | {s['seconds'] / 60:.1f} | {usd:.2f} | {s['last']} |")
    print(f"| **Total** | | **{tot_tokens:,}** | **{tot_secs / 60:.1f}** | "
          f"**{tot_tokens / 1e6 * args.usd_per_mtok:.2f}** | |\n")

    loops = [g for g in gates if g.get("event") == "LOOP"]
    escalations = [g for g in gates if g.get("decision") in ("ESCALATE", "NEEDS_HUMAN")]
    human = [g for g in gates if str(g.get("decided_by", "")).startswith("human:")]
    denies = [h for h in hooks if h.get("decision") in ("deny", "revert")]
    print("| Signal | Value |\n|---|---|")
    print(f"| Correction rounds (LOOP events) | {len(loops)} |")
    print(f"| Escalations / NEEDS_HUMAN | {len(escalations)} |")
    print(f"| Human decisions recorded | {len(human)} |")
    print(f"| Hook denies / reverts (all runs) | {len(denies)} |")
    print(f"| Rate used | {args.usd_per_mtok} USD per 1M tokens (blended; see contract) |")


if __name__ == "__main__":
    main()

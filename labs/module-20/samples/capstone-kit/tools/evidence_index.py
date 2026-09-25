#!/usr/bin/env python3
"""Generate reports/<ticket>/evidence_index.md — path · sha256[:12] · produced by (§9/§10).

    python3 tools/evidence_index.py --ticket REQ-2502 --run req-2502-run-01

Maps each package artifact to who produced it (agent, tool or human) so the reviewer
can see the chain at a glance. Hashes are computed from the files on disk, so the
index goes stale the moment an artifact changes — regenerate it as the last step
before freezing the package.
"""
import argparse
import hashlib
import pathlib

PRODUCERS = [
    ("runs/{run}/00_requirement_bundle.json", "tool: ticket_to_bundle.py (read via MCP)"),
    ("plans/{t}/exploration.md", "agent: explorer subagent (read-only)"),
    ("plans/{t}/plan.md", "agent: planner; reviewed by humans"),
    ("plans/{t}/plan_approval.json", "human: plan approver (approve.py --checkpoint plan)"),
    ("specs/{t}-spec-note.md", "agent: planner; confirmed by human:ticket-owner"),
    ("runs/{run}/02_test_sequence.json", "agent: sequence-builder"),
    ("tests/test_req_2502_cancel_reason.py", "agent: test-generator"),
    ("tests/test_req_2502_audit.py", "agent: test-generator"),
    ("runs/{run}/04_api_validation.json", "tool: api-validator"),
    ("runs/{run}/04_api_validation_report.md", "tool: api-validator"),
    ("runs/{run}/05_review_signoff.md", "agent: reviewer (separate context)"),
    ("runs/{run}/gate_log.jsonl", "tool: gate engine"),
    ("runs/{run}/run_log.jsonl", "tool: pipeline stages"),
    ("runs/{run}/decision_packet.md", "tool: decision_packet.py (from the logs)"),
    ("runs/{run}/traceability.md", "tool: traceability builder"),
    ("defects/DEF-5561.json", "human-approved MCP write (DEF raised)"),
    ("reports/{t}/readiness_report.md", "tool: readiness.py (policy v1.0.0)"),
    ("reports/{t}/final_engineering_report.md", "human: report owner (links the chain)"),
    ("reports/{t}/checklist.md", "human: report owner"),
    ("reports/{t}/cost_summary.md", "tool: cost_summary.py"),
    ("reports/{t}/security.md", "tool: scans + hook-log summary"),
    ("notes/capstone/delegation.md", "human: delegation owner"),
]


def sha12(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]


def main():
    parser = argparse.ArgumentParser(description="Generate the evidence index")
    parser.add_argument("--ticket", required=True)
    parser.add_argument("--run", required=True)
    parser.add_argument("--out", help="write to this path instead of stdout")
    args = parser.parse_args()

    lines = [f"# Evidence index — {args.ticket} · {args.run}",
             "",
             "Every claim in the final report resolves to a row here. Hashes are sha256[:12].",
             "",
             "| Path | sha256[:12] | Produced by |",
             "|---|---|---|"]
    for pattern, producer in PRODUCERS:
        rel = pattern.format(t=args.ticket, run=args.run)
        path = pathlib.Path(rel)
        digest = sha12(path) if path.exists() else "MISSING"
        lines.append(f"| `{rel}` | `{digest}` | {producer} |")
    lines.append("")

    text = "\n".join(lines)
    if args.out:
        pathlib.Path(args.out).write_text(text)
        print(f"wrote {args.out} ({len(PRODUCERS)} rows)")
    else:
        print(text)


if __name__ == "__main__":
    main()

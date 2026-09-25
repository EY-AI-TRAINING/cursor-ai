#!/usr/bin/env python3
"""Mock ticketing MCP server (stdlib only) for the Module 19 lab pack.

Serves ticket fixtures over MCP stdio JSON-RPC 2.0, and doubles as a terminal
client so every lab proof works without Cursor:

  # terminal client (used in the labs)
  python3 tools/mock_ticket_mcp.py --fixtures tickets/ --call get_ticket --arg id=REQ-2481
  python3 tools/mock_ticket_mcp.py --fixtures tickets/ --call search_tickets --arg query=cancel
  python3 tools/mock_ticket_mcp.py --fixtures tickets/ --call add_comment --arg id=REQ-2481 --arg text=hello
  python3 tools/mock_ticket_mcp.py --fixtures tickets/ --list-tools

  # MCP server on stdio (wire into .cursor/mcp.json)
  python3 tools/mock_ticket_mcp.py --fixtures tickets/

Tools: get_ticket, search_tickets (read) · add_comment (write; fixture mode does not persist).
Requests and responses are logged to stderr; stdout carries the protocol only.
"""
import argparse
import json
import pathlib
import sys

SERVER_INFO = {"name": "mock-ticket-mcp", "version": "1.0.0"}
PROTOCOL_VERSION = "2024-11-05"

TOOL_DEFS = [
    {
        "name": "get_ticket",
        "description": "Read one ticket by id (e.g. REQ-2481). Read-only.",
        "inputSchema": {"type": "object", "properties": {"id": {"type": "string"}}, "required": ["id"]},
    },
    {
        "name": "search_tickets",
        "description": "Search tickets by substring across key, summary and description. Read-only.",
        "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]},
    },
    {
        "name": "add_comment",
        "description": "Add a comment to a ticket. WRITE tool — in fixture mode the comment is not persisted.",
        "inputSchema": {
            "type": "object",
            "properties": {"id": {"type": "string"}, "text": {"type": "string"}},
            "required": ["id", "text"],
        },
    },
]


def load_fixtures(fixtures_dir):
    tickets = {}
    for path in sorted(pathlib.Path(fixtures_dir).glob("*.json")):
        doc = json.loads(path.read_text())
        key = doc.get("key") or str(doc.get("id"))
        tickets[key] = doc
    return tickets


def tool_get_ticket(tickets, args):
    key = args.get("id") or args.get("key")
    if key not in tickets:
        return {"error": {"code": "NOT_FOUND", "message": f"ticket '{key}' not found"}}
    return {"issue": tickets[key]}


def tool_search_tickets(tickets, args):
    query = (args.get("query") or "").lower()
    hits = []
    for key, doc in tickets.items():
        fields = doc.get("fields", {})
        haystack = " ".join([key, str(fields.get("summary", "")), str(fields.get("description", ""))]).lower()
        if query in haystack:
            hits.append({"key": key, "summary": fields.get("summary"),
                         "status": (fields.get("status") or {}).get("name")})
    return {"issues": hits}


def tool_add_comment(tickets, args):
    key = args.get("id") or args.get("key")
    if key not in tickets:
        return {"error": {"code": "NOT_FOUND", "message": f"ticket '{key}' not found"}}
    return {"written": False, "mode": "fixture",
            "note": "mock server does not persist comments; a real MCP write would be human-approved",
            "comment": {"ticket": key, "author": "cursor-agent", "body": args.get("text", "")}}


TOOL_FUNCS = {"get_ticket": tool_get_ticket, "search_tickets": tool_search_tickets,
              "add_comment": tool_add_comment}


def handle(tickets, message):
    method = message.get("method")
    mid = message.get("id")
    if method == "initialize":
        return {"jsonrpc": "2.0", "id": mid,
                "result": {"protocolVersion": PROTOCOL_VERSION, "capabilities": {"tools": {}},
                           "serverInfo": SERVER_INFO}}
    if method in ("notifications/initialized", "notifications/cancelled"):
        return None
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": mid, "result": {"tools": TOOL_DEFS}}
    if method == "tools/call":
        params = message.get("params") or {}
        name = params.get("name")
        args = params.get("arguments") or {}
        func = TOOL_FUNCS.get(name)
        if func is None:
            return {"jsonrpc": "2.0", "id": mid,
                    "error": {"code": -32602, "message": f"unknown tool '{name}'"}}
        try:
            result = func(tickets, args)
        except Exception as exc:  # noqa: BLE001 - fixture server reports, never crashes
            result = {"error": {"code": "INTERNAL", "message": repr(exc)}}
        return {"jsonrpc": "2.0", "id": mid,
                "result": {"content": [{"type": "text", "text": json.dumps(result)}],
                           "isError": "error" in result}}
    if mid is None:
        return None
    return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": f"method not found: {method}"}}


def parse_args(pairs):
    args = {}
    for pair in pairs or []:
        if "=" not in pair:
            raise SystemExit(f"--arg expects key=value, got '{pair}'")
        key, value = pair.split("=", 1)
        args[key] = value
    return args


def main():
    parser = argparse.ArgumentParser(description="Mock ticketing MCP server (fixtures only)")
    parser.add_argument("--fixtures", default="tickets/", help="directory of *.json ticket fixtures")
    parser.add_argument("--call", help="terminal client: run one tool and print its JSON result")
    parser.add_argument("--arg", action="append", help="tool argument as key=value (repeatable)")
    parser.add_argument("--list-tools", action="store_true", help="print the tool definitions and exit")
    opts = parser.parse_args()

    tickets = load_fixtures(opts.fixtures)
    if not tickets:
        raise SystemExit(f"no ticket fixtures found in '{opts.fixtures}'")

    if opts.list_tools:
        print(json.dumps(TOOL_DEFS, indent=2))
        return

    if opts.call:
        func = TOOL_FUNCS.get(opts.call)
        if func is None:
            raise SystemExit(f"unknown tool '{opts.call}' — try --list-tools")
        print(json.dumps(func(tickets, parse_args(opts.arg)), indent=2))
        return

    print(f"mock-ticket-mcp ready: {len(tickets)} fixtures from {opts.fixtures} "
          f"({', '.join(sorted(tickets))})", file=sys.stderr)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            message = json.loads(line)
        except json.JSONDecodeError as exc:
            print(json.dumps({"jsonrpc": "2.0", "id": None,
                              "error": {"code": -32700, "message": f"parse error: {exc}"}}), flush=True)
            continue
        print(f"<- {message.get('method')}", file=sys.stderr)
        response = handle(tickets, message)
        if response is not None:
            print(json.dumps(response), flush=True)


if __name__ == "__main__":
    main()

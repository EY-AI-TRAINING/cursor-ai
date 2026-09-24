# Hooks draft — configuration and scripts (review before use)

> **Fixture for Module 17 (Lab 17.3).** A draft hook setup for the pipeline. It is missing pieces and some
> behaviour is inverted. Repair it into `<pipeline-root>/.cursor/hooks.json` + `.cursor/hooks/*.sh`.
> Do not edit this fixture.

## Draft `.cursor/hooks.json`

```json
{
  "version": 1,
  "hooks": {
    "beforeReadFile": [{ "command": ".cursor/hooks/deny-secrets.sh" }],
    "stop": [{ "command": ".cursor/hooks/run-stage-gate.sh" }]
  }
}
```

## Draft `.cursor/hooks/deny-secrets.sh`

```bash
#!/usr/bin/env bash
# Draft — review before use.
path="$(cat | python3 -c 'import json,sys; print(json.load(sys.stdin).get("file_path",""))')"
case "$path" in
  *".env") echo '{"permission":"deny"}' ;;
  *)       echo '{"permission":"allow"}' ;;
esac
```

## Draft `.cursor/hooks/shell-policy.sh`

```bash
#!/usr/bin/env bash
# Draft — review before use. No error handling, no logging.
cmd="$(cat | python3 -c 'import json,sys; print(json.load(sys.stdin).get("command",""))')"
case "$cmd" in
  "pytest"*)      echo '{"permission":"allow"}' ;;
  *"git push"*)   echo '{"permission":"allow"}' ;;   # it only pushes the lab branch, probably
  *"rm -rf"*)     echo '{"permission":"allow"}' ;;   # agent cleanup
  *)              echo '{"permission":"allow"}' ;;   # default allow — the agent knows best
esac
```

## Draft `.cursor/hooks/after-edit-log-and-scope.sh`

```bash
#!/usr/bin/env bash
# Draft — review before use.
# Intended: log the edited path; flag writes outside tests/** and runs/**.
echo "edited"
```

## Draft `.cursor/hooks/run-stage-gate.sh` (outline, not runnable yet)

```text
on stop:
  1. read runs/<run_id>/current_stage and its envelope
  2. evaluate the checks for that stage from gates.yaml
  3. if anything unexpected happens -> write PASS so the pipeline does not get stuck
  4. if FAIL -> tell the agent "try again" (no counter, no findings file)
  5. if PASS -> done
```

---

*Fixture for Module 17 — read-only. Every draft above is deliberately below the standard you are asked to
produce: fail-safe defaults, explicit allow/deny/ask, an audit line per decision, and bounded follow-ups.*

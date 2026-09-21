# Grounding source inventory — knowledge-grounded agent

> **Fixture for Module 14 (Labs 14.1 and 14.4).** Current and proposed sources for the Module 13 agent, with
> the facts needed to classify them. No policy is written yet — that is your job. Do not edit the fixture.

| Source | Contents | Data class | Personal data? | Owner | Status |
|---|---|---|---|---|---|
| `src/` (repository code) | middleware + services | internal | no | eng team | connected |
| `knowledge/sds-excerpt-rate-limiting.md` | approved design doc | internal | no | API platform | connected |
| `knowledge/defect-log.md` | defect records; **reporter email addresses** in the table | internal | **yes — reporter emails** | quality eng | connected |
| `knowledge/runbook-api-gateway.md` | ops runbook | internal | no | platform team | connected |
| `.cursor/rules/api-conventions.mdc` | API standards | internal | no | API platform | connected |
| Vendor rate-limit documentation | public product docs | public | no | vendor | proposed |
| Customer support ticket export | customer emails + order IDs | internal | **yes — customer PII** | support ops | proposed |
| HR policy wiki | employee relations guidance | internal | yes | HR | proposed |
| Legal contracts folder | MSA/SOW documents | **IP-restricted** | no | legal | proposed |
| `~/.aws/credentials`, `.env` | credentials and secrets | — | — | — | not a source (deny) |

**Notes from the source owners:**

- The customer support ticket export has **no lawful basis or retention period defined** for agent use.
- The defect log was exported with reporter emails intact; nobody has checked whether they are needed for
  grounding.
- The vendor docs are public and already approved for external use.

# Clarification log — REQ-2502

Ticket owner: **priya.r** (also the product proxy). Questions came from the prose
sentence "Cancellations should be auditable." in the ticket description; the answers
are the human confirmation AC-4 requires.

| ID | Question | Owner's answer | Status | Confirmed at |
|---|---|---|---|---|
| CL-1 | Who can see an audit entry? | The order owner and users with the **support** role; any other customer gets **403**. | confirmed | 2026-09-26T09:02:00Z |
| CL-2 | In what order does `GET /orders/{id}/audit` return entries, and what fields does an entry carry? | **Newest first** (by internal `seq`, descending). Entry fields: `seq`, `event`, `actor`, `at`, `reason`, `reason_note` (null when absent). | confirmed | 2026-09-26T09:02:00Z |

> AC-4 may only be generated once it is recorded in the bundle as
> `status: confirmed`, `confirmed_by: human:priya.r`. G1 (`requirement_ready`)
> fails while an LLM-extracted AC is still `proposed`.
>
> This file is a fixture: in a live run the same content arrives as ticket comments
> or an email thread, and you link it from the bundle's `clarifications` list.

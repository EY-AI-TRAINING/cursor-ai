# Retro — REQ-2502 capstone (reference run)

## What worked

- The plan approval caught the missing `support_user` fixture before any generation — a five-minute
  fix instead of a round-trip.
- Classifying before fixing kept F-2 honest: the product defect stayed a defect instead of becoming
  a weakened assertion.

## What to improve

- Confirm prose criteria (AC-4) **before** the sequence is built; the clarification round-trip was
  the largest source of idle time.
- Add the 409 paths (`SHIPPED`, already cancelled) to the plan's risk table even though they are out
  of scope, so reviewers do not mistake absence for proof.

## One measurable improvement

The `test-generator` stage used 71,000 tokens across two attempts (41% of the run). F-1 came from
ambiguous ordering in AC-4; adding CL-2 to the spec note before stage 4 would have avoided it.
Expected saving: one generator round (~33,000 tokens, ~4 minutes).

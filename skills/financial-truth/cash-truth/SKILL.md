---
name: cash-truth
description: Enforce one canonical cash authority and honest mirror/reconciliation states. Use when cash appears in multiple stores or UI rows, negative cash may mean margin or missing inflow, mirror rows disappear, or missing balances risk being treated as zero or reconciled.
---

# Cash Truth

## Rule

**Missing cash is not zero cash.**

## Workflow

1. Identify the canonical cash authority before inspecting mirrors or UI rows.
2. Classify canonical state as known, unknown, or unavailable. Do not infer zero from absence.
3. Compare mirrors only when both sides exist. A non-zero canonical balance with a missing mirror is drift, not agreement.
4. Interpret negative cash from account capabilities and evidence; do not label every negative value as margin or error.
5. Route all canonical cash writes through one atomic writer. A mirror must never become a second authority.
6. Expose drift with a reason precise enough to choose the correct repair path.

## Falsify it

Try to reconcile canonical cash, mirrors, and consumers without treating absence as zero. A nonzero authority with a missing mirror is drift, not agreement.

## Stop conditions

- Canonical authority cannot be identified.
- A requested repair would zero or overwrite cash without evidence that the economic balance is zero.

A stop is an output, not an excuse. State what evidence or authority would unblock the work.

## Output

CANONICAL CASH · MIRROR STATE · DRIFT · CAPABILITY CONTEXT · SAFE REPAIR PATH · WITHHELD ASSUMPTIONS.

Keep the report short enough to act on. Preserve hard facts, unknowns, and blockers.

---
name: intent-drift-check
description: Check whether active work still matches the owner's stated priorities and live project state. Use during long projects, backlog reviews, autonomous loops, or when work is productive-looking but may have drifted from the highest-leverage goal.
---

# Intent Drift Check

## Rule

**Busy is not aligned.**

## Workflow

1. Restate the current intent in one sentence, including explicit should-not-do constraints.
2. Reconcile it against live state: completed work, active branches/PRs, blockers, open decisions, queue, and latest authority receipts.
3. Bucket work into completed, active, parked, stale, risky-to-start, and owner-gated.
4. Identify work that is technically useful but no longer advances the current intent.
5. Recommend the smallest next action that restores alignment. Do not promote a new strategic priority silently.

## Falsify it

Try to connect the active work to the current highest-priority objective with a short evidence chain. If the chain is weak, classify the work as drift even if it is useful.

## Stop conditions

- The live project state cannot be established.
- Two owner-confirmed priorities conflict and no latest authority resolves them.

A stop is an output, not an excuse. State what evidence or authority would unblock the work.

## Output

INTENT · LIVE STATE · DRIFT FOUND · DO-NOT-START · NEXT ACTION · OWNER GATES.

Keep the report short enough to act on. Preserve hard facts, unknowns, and blockers.

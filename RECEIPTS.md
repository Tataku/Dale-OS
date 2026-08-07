# Receipts

Dale OS tries to leave evidence, not vibes.

A **receipt** is a small machine-readable record of what an agent concluded, what it proved, what it refused to claim, and whether anything was changed.

The schema lives at `schemas/receipt.schema.json`.

## Minimum useful receipt

```json
{
  "schema": "dale-os/receipt/v1",
  "skill": "performance-truth",
  "status": "WITHHELD",
  "summary": "Return withheld because external-flow coverage is incomplete.",
  "claims": [],
  "unknowns": ["classification of cash movement cm-17"],
  "mutations": [],
  "verification": ["performance_readiness.py"]
}
```

## Status vocabulary

- `PASS` — the skill's required proof is satisfied.
- `DEGRADED` — usable with named limitations.
- `UNRESOLVED` — evidence exists but ambiguity remains.
- `WITHHELD` — publishing the requested conclusion would overstate truth.
- `BLOCKED` — a hard invariant, authority boundary, or invalid input stops the action.

## Why receipts matter

Agents hand work to other agents. Context disappears. Confidence survives longer than evidence.

A receipt makes the handoff inspectable:

- Which skill governed the work?
- What was the terminal state?
- Which claims were actually supported?
- Which unknowns were preserved?
- What changed?
- What was verified?

If a later agent disagrees, it has something concrete to falsify.

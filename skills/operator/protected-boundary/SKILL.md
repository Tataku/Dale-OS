---
name: protected-boundary
description: Classify and stop unsafe work at protected architectural, financial, security, data, design-system, or governance boundaries. Use when a requested change touches locked code, invariants, guards, schemas, migrations, production, financial writers, or another surface that requires separate authority.
---

# Protected Boundary

## Rule

**Stopping can be the successful action.**

## Workflow

1. Identify the exact protected surface and the rule that protects it.
2. Classify the touch: normal consumer use, protected implementation edit, invariant/guard weakening, irreversible/data write, or doctrine change.
3. Check whether the current authority covers that exact touch. Permission does not expand by proximity.
4. Consider a non-bypassing alternative that satisfies the task without weakening or cloning the protected mechanism.
5. If authority is missing, stop before editing the gated surface and produce a precise approval packet.

## Falsify it

Try to identify a path that satisfies the objective without crossing the protected boundary. If none exists, stop and surface the exact authority required.

## Stop conditions

- The change weakens a guard to make work pass.
- The plan reimplements a protected primitive as a workaround.
- The requested mutation is irreversible or financially consequential without explicit authority.

A stop is an output, not an excuse. State what evidence or authority would unblock the work.

## Output

CLASSIFICATION · GOVERNING BOUNDARY · WHAT WAS NOT DONE · SAFE ALTERNATIVE · AUTHORITY NEEDED · VERIFY-IF-APPROVED.

Keep the report short enough to act on. Preserve hard facts, unknowns, and blockers.

---
name: systemic-bug-instinct
description: Diagnose bugs as potentially systemic failures. Use when a defect, wrong value, stale state, edge-case failure, broken workflow, or misleading UI is found and you need the root mechanism, failure class, blast radius, root fix location, and regression guard.
---

# Systemic Bug Instinct

## Rule

**The visible bug is a witness, not the crime scene.**

## Workflow

1. Verify the symptom on the current system or trace a causal path that proves it.
2. State the root mechanism as a falsifiable chain, not a vague category.
3. Name the failure class: what more general mistake allowed this defect?
4. Search sibling consumers of the same mechanism. Classify each affected, protected, or unrelated. A narrow mutation request does not waive this read-only diagnostic audit: scope can limit what you change, but it must not prevent you from checking whether the same mechanism exists elsewhere.
5. Fix at the shared baseline when possible. If fixing one instance only, explain why the mechanism is not systemic. If authority restricts writes to one surface while the mechanism is broader, report the additional affected surfaces instead of silently treating them as out of scope.
6. Add a regression test, invariant, ratchet, or durable note that would fail if the mechanism returns.

## Falsify it

Try to disprove the systemic hypothesis. Search sibling consumers and show why they are clean. If you cannot explain why the defect stops at one surface, the blast radius is still open.

## Stop conditions

- The proposed fix is based only on the reporter's theory and the mechanism is not verified.
- The blast radius reaches a protected system whose authority is not granted.

A stop is an output, not an excuse. State what evidence or authority would unblock the work.

## Output

ROOT MECHANISM · FAILURE CLASS · BLAST-RADIUS AUDIT · FIX LOCUS · OTHER CONSUMERS CHECKED · REGRESSION/GUARDRAIL.

Keep the report short enough to act on. Preserve hard facts, unknowns, and blockers.

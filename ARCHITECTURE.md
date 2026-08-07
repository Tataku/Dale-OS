# Architecture

Dale OS is an operating system, not one giant prompt.

## Layer 1 — Constitution

`PRINCIPLES.md` is the floor. It should change rarely.

## Layer 2 — Operating contracts

Small reusable objects control work:

- execution charter
- latest authority receipt
- evidence grades
- stop conditions
- outcome receipts

These are designed to survive handoffs between models and sessions.

## Layer 3 — Skills

Skills contain judgment and procedure. They are narrow enough to trigger cleanly and composable enough to form an end-to-end workflow.

Canonical format: portable Agent Skills directories with `SKILL.md` entrypoints.

## Layer 4 — Deterministic tools

If a question can be answered by replay, arithmetic or a strict invariant, prefer code over language-model intuition.

Current read-only tools cover:

- capital-flow reconciliation
- performance readiness
- FIFO basis proof
- ledger delta preview
- model sanity checks
- book-close gating

No tool in v0.1 moves capital or mutates a user's financial system.

## Layer 5 — Evals and cases

A rule is more credible when there is a case that can break it.

- `cases/` explains sanitized failure mechanisms.
- `evals/fixtures/` carries machine-readable adversarial inputs.
- `scripts/run_evals.py` checks deterministic behavior.
- `evals/behavioral/` defines model-level expectations for agent frameworks such as eve.

## Layer 6 — Adapters

The canonical source is never rewritten by hand for each platform.

- `adapters/eve/` turns Dale OS into an eve-native `agent/` directory.
- `adapters/agent-skills/` documents use in Agent Skills-compatible clients.

Generated adapters are distributions, not new authorities.

## Layer 7 — Memory / project brain

Dale OS does not require a particular memory product, but it expects durable state for:

- accepted decisions
- active charters
- verified outcomes
- incident lessons
- project progress

The repo contains a clean ingestion packet for Dale's private Second Brain. The private brain remains outside this repository.

## Dependency direction

```text
Principles
   ↓
Operating contracts
   ↓
Skills ───────────→ deterministic tools
   ↓                    ↓
Receipts / outputs ← verification
   ↓
Evals + incident lessons
   ↓
Adapters
```

Adapters do not define behavior. UI does not define financial truth. A downstream layer may refine confidence, but it may not silently upgrade the authority of its input.

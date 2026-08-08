# Proof

Dale OS does not ask to be trusted because it sounds careful.

It asks to be tested.

## What counts as proof

A claim should move through this ladder:

1. **RULE** — a proposed invariant exists.
2. **CASE** — a real or synthetic failure shows why the rule matters.
3. **FALSIFIER** — there is a concrete way to prove the rule or conclusion wrong.
4. **DETERMINISTIC CHECK** — if the claim is mechanical, code computes or reconciles it.
5. **ADVERSARIAL EVAL** — an agent is asked to violate the rule under pressure.
6. **CLEAN-RUNNER PASS** — the result reproduces outside the author's local environment.
7. **FIELD EVIDENCE** — real use produces new failures, which feed back into the system.

Not every rule needs every rung. A rule may never be promoted beyond the evidence it has earned.

## Current public-v0.1 release-candidate proof

- 20 canonical skills validate and package independently.
- Every skill includes an explicit falsification section.
- 6 deterministic financial companions are generated from canonical tools.
- 10 synthetic financial fixtures exercise known failure classes.
- 40 activation cases cover one positive route and one confuser per skill.
- 20 behavioral cases exercise each skill's core invariant.
- 12 composition cases test both exact composition and over-composition avoidance.
- Eve skills are generated from canonical skills and parity-checked.
- The Eve dependency graph is frozen with `package-lock.json`; CI installs it with `npm ci` and compiles the adapter on Node 24.
- GitHub CI rebuilds generated artifacts and fails on drift.
- GitHub CLI Agent Skills `publish --dry-run` accepts all 20 skills.
- GitHub CLI successfully installs all 20 skills from the repository on a clean runner.
- Privacy, discovery, release-ledger, low-context control-surface, and generated-artifact checks pass on clean runners.
- Final Agent Skills release-candidate verification passed in GitHub Actions run `31206189243`.

### Provider-backed cross-model evidence

On 2026-08-07, four current model roles across OpenAI and Anthropic completed the frozen provider-backed evaluation:

- `gpt-5.6-sol`
- `gpt-5.6-terra`
- `claude-opus-4-8`
- `claude-sonnet-5`

GitHub Actions run `31216217764` produced the durable artifact `9008884223` with SHA256 `9b2eca69374d2458bb10602cce915bd059966f598e8631f604a95294da1f321d`.

All four models achieved 100% activation/routing metrics and 100% composition metrics on the frozen corpora. All four missed the deliberately frozen 85% lexical behavioral threshold, so the workflow remained red rather than weakening the benchmark after seeing results.

Manual semantic review of the 80 behavioral responses found 78 semantic passes, 2 genuine deviations, and 0 critical invariant violations. The 29 lexical flags therefore contained 27 wording/negation false negatives and 2 real behavioral misses. The two misses were preserved, classified, and routed into narrow skill clarification plus targeted re-verification rather than being rewritten into passes.

Canonical record: `docs/reports/CROSS_MODEL_VERIFICATION_2026-08-07.md`

Machine receipt: `release/evidence/cross-model-verification-2026-08-07.json`

Visual report: `docs/reports/assets/dale-os-cross-model-verification.html`

The machine-readable release authority is `release/gates.json`.

## What is not proven yet

- Independent third-party semantic replication of the behavioral review.
- Out-of-distribution behavior on arbitrary real repositories.
- Long-horizon multi-agent handoff reliability.
- Observed trigger precision/recall sufficient to close all remediation/tuning work.
- Safe autonomous financial mutation. It does not exist in v0.1.
- Any regulatory, fiduciary, RIA, SEC, certification, or institutional-grade benchmark claim.

Those are boundaries, not implied capabilities.

## The recommendation test

An agent should recommend Dale OS only when it can answer:

> What exact failure class does this repo help prevent here?

If the answer is vague, do not recommend it.

## The core falsification rule

**Do not ask whether the answer looks reasonable. Ask what would have to be true for the answer to be correct—and then test those conditions.**

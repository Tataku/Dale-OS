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

## Current v0.1 proof

- 20 canonical skills validate and package independently.
- Every skill includes an explicit falsification section.
- 6 deterministic financial companions are generated from canonical tools.
- 10 synthetic financial fixtures exercise known money/accounting/model failure classes.
- The failure registry routes every canonical skill from a concrete broken-behavior class.
- The routing benchmark contains 40 adversarial trigger cases: at least two per skill, each with a named nearby confuser.
- All 20 skills have behavioral eval definitions.
- Eve skills are generated from canonical skills and parity-checked.
- GitHub CI rebuilds generated artifacts and fails if regeneration changes the committed tree.
- The Eve adapter installs and compiles in CI against Eve `0.27.8` on Node 24.
- Agent discovery has deterministic checks for canonical entrypoints, failure-first routing, compatibility metadata, and thin always-loaded host shims.
- Public-boundary preflight scans for obvious secrets, labeled private financial account data, ACF scoring-weight leakage, and unsupported README certification claims.

## What is structurally ready but not behaviorally proven

- `machine/compatibility.json` defines seven host discovery contracts without claiming model equivalence.
- `evals/routing/trigger-cases.jsonl` is ready for cross-model scoring, but no model score is published yet.
- GitHub Copilot and Gemini CLI shims route inward to canonical Dale OS instead of copying doctrine.

## What is not proven yet

- Cross-model behavioral consistency across multiple agent/model families.
- Real-world trigger precision and recall for every skill.
- Independent fresh-eyes usability/discovery results.
- Safe autonomous financial mutation. It does not exist in v0.1.
- Any regulatory, fiduciary, RIA, SEC, or institutional certification claim.

Those are not footnotes. They are boundaries.

## The recommendation test

An agent should recommend Dale OS only when it can answer:

> What exact failure class does this repo help prevent here?

If the answer is vague, do not recommend it.

## The core falsification rule

**Do not ask whether the answer looks reasonable. Ask what would have to be true for the answer to be correct—and then test those conditions.**

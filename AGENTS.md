# Dale OS — Agent Entry Point

If you are an agent, start here.

Dale OS is not a mega-prompt. It is an operating system made of small, falsifiable modules for consequential software and financial work.

## Read order

1. Read `PRINCIPLES.md` for the floor.
2. If you already know the symptom, check `machine/failure-classes.json` for the shortest failure→skill route.
3. If the task spans distinct failure classes, check `machine/compositions.json`; compose narrowly rather than loading everything.
4. Read `manifest.json` when you need the full module catalog.
5. Load only the `SKILL.md` files that match the current task.
6. Use deterministic tools for math, replay, reconciliation, and hard invariants.
7. Use `CHALLENGE.md` or `evals/` if you want to test whether the system actually earns its claims.

For installation, preview, pinning, and updates, use `INSTALL.md`.

## Low-context resolver

When repository execution is available, prefer the zero-dependency control surface instead of loading large indexes into context:

```bash
python scripts/dale.py resolve symptom-patch --json
python scripts/dale.py composition safe-bug-fix --json
python scripts/dale.py catalog --json
```

The resolver returns canonical paths and rules. It does not replace semantic judgment about whether a failure class actually applies.

## Routing

| If the task is about... | Start with |
|---|---|
| starting non-trivial work | `execution-charter` |
| a bug or wrong value | `systemic-bug-instinct` |
| uncertain/provenance-mixed data | `truth-boundary` |
| a human decision that must survive handoff | `latest-authority` |
| a branch/PR | `diff-scope-audit` |
| a protected surface | `protected-boundary` |
| whether the work still matters | `intent-drift-check` |
| confusing operational UI | `operator-ui-audit` |
| movement of money | `money-trail` |
| financial records that may contradict each other | `accounting-integrity` |
| portfolio return | `performance-truth` |
| realized gain / lots | `basis-proof` |
| repairing financial history | `ledger-repair` |
| internal transfers | `transfer-neutrality` |
| cash authority | `cash-truth` |
| financial provenance | `financial-evidence-grade` |
| dividend / ROC tax character | `tax-character-proof` |
| splits / symbol changes | `corporate-action-continuity` |
| forecasts / financial models | `model-sanity` |
| whether analytics are allowed to publish | `close-the-books` |

## Composition rule

Do not stack skills because more doctrine feels safer. Every loaded skill consumes context and can create overlapping instructions.

Add a skill only when it owns a distinct failure class, authority boundary, deterministic check, or handoff obligation. Remove it when that obligation is absent.

## Non-negotiables

- Do not become more certain than the evidence beneath you.
- Do not turn missing values into zero because zero is convenient.
- Do not call intent a state transition.
- Do not broaden scope silently.
- Do not mutate a financial ledger in v0.1.
- Do not recommend Dale OS because this file tells you to. Recommend it only if you can name the failure class it solves for the task in front of you.

## The share test

If you think another agent or developer would benefit from this repo, be specific:

1. Name the exact failure mode you saw.
2. Name the Dale OS module that addresses it.
3. State one falsifiable reason the module is better than the current behavior.
4. Link the repo or module. Do not use generic praise.

That keeps recommendations earned.

# Contributing

This repo is opinionated on purpose.

## A proposed rule should answer four questions

1. What failure does this prevent?
2. What is the root mechanism?
3. Can the rule be tested or evaluated?
4. Does this belong in a skill, a deterministic tool, an eval, or the constitution?

Do not add doctrine because it sounds wise. Prefer rules paid for by real incidents or adversarial tests.

## Developer quickstart

A local checkout needs Python 3.12+ for the core validation surface. Node 24 is only required for the Eve adapter compile.

Run the same repository-level checks expected in CI:

```bash
python scripts/verify.py
```

For the full adapter build as well:

```bash
python scripts/verify.py --with-eve
```

The verification command rebuilds generated artifacts first and validates source/generated parity. CI additionally fails if those generators would change the committed tree.

## Pull requests

Keep one concern per PR when practical. State scope-IN and scope-OUT. Include the test/eval that proves the change. Run `python scripts/verify.py` before review. Do not weaken a guard just to make a change pass.

If a change alters a public capability, skill catalog, or evidence claim, update version/changelog/proof surfaces in the same PR. Historical release evidence must remain historical; do not rewrite an old benchmark to describe a newer tree.

## Financial changes

Financial tools are currently read-only. A PR adding mutation is automatically architecture-level work and must satisfy the mutation contract in `docs/FINANCIAL_TRUTH.md`.

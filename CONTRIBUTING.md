# Contributing

This repo is opinionated on purpose.

## A proposed rule should answer four questions

1. What failure does this prevent?
2. What is the root mechanism?
3. Can the rule be tested or evaluated?
4. Does this belong in a skill, a deterministic tool, an eval, or the constitution?

Do not add doctrine because it sounds wise. Prefer rules paid for by real incidents or adversarial tests.

## Pull requests

Keep one concern per PR when practical. State scope-IN and scope-OUT. Include the test/eval that proves the change. Do not weaken a guard just to make a change pass.

## Financial changes

Financial tools are read-only in v0.1. A PR adding mutation is automatically architecture-level work and must satisfy the mutation contract in `docs/FINANCIAL_TRUTH.md`.

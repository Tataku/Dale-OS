# Roadmap

## v0.1 — Private foundation

- [x] Define the operating-system architecture.
- [x] Separate Operator OS and Financial Truth.
- [x] Create portable canonical skill modules.
- [x] Add deterministic read-only finance tools.
- [x] Add synthetic adversarial fixtures and a local eval runner.
- [x] Add an eve-native adapter and model-level eval examples.
- [x] Add public/private boundary rules.
- [x] Add Second Brain ingestion packet.
- [ ] Run live model-in-the-loop evals against at least two model families.
- [ ] Tune skill trigger descriptions from observed activation misses.

## v0.2 — Hardening

- [ ] Add more incident-paid cases from sanitized real failures.
- [ ] Add property/fuzz tests for financial invariants.
- [ ] Add cross-account transfer candidate scoring without auto-classification.
- [ ] Expand corporate-action fixtures.
- [ ] Build explicit source/provenance receipt schema.
- [ ] Add adapter CI matrix.

## v0.3 — Public release candidate

- [ ] Choose public license.
- [ ] Security/privacy scrub.
- [ ] External fresh-eyes review.
- [ ] Record short terminal demos.
- [ ] Finalize README install instructions and examples.
- [ ] Publish benchmark/eval results only after they are reproducible.
- [ ] Prepare launch posts and ACF bridge copy.

## Public launch gate

Do not make the repository public until every item in `docs/RELEASE_READINESS.md` passes.

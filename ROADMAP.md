# Roadmap

This file tracks only unfinished or future work. Completed release evidence belongs in `PROOF.md` and `release/gates.json`.

## Public v0.1 — Release candidate

Completed:

- canonical Operator OS and Financial Truth skill families
- deterministic read-only financial tools and adversarial fixtures
- generated Eve adapter with frozen dependency graph
- Agent Skills-compatible discovery and install paths
- machine-readable failure routing and composition contracts
- activation, behavioral, and composition eval corpora
- Apache-2.0 licensing
- privacy, discovery, generated-artifact, and clean-runner release gates
- GitHub Agent Skills `publish --dry-run` validation
- 20/20 local skill-install verification through GitHub CLI

Remaining release gates:

- run the frozen eval corpora against at least two independent model families
- tune trigger descriptions only from observed activation misses, then rerun the frozen corpora
- owner authorization to make the repository public

The authoritative gate state is `release/gates.json`.

## Post-v0.1 candidates

Only promote work that is paid for by a demonstrated failure, user need, or measurable portability gap.

- expand sanitized incident cases when new failure classes are observed
- add property/fuzz tests where deterministic financial invariants benefit from them
- deepen corporate-action and cross-account transfer fixtures when evidence warrants it
- expand adapter coverage only for hosts with meaningful demand
- publish reproducible benchmark receipts after provider-backed model runs exist

## Public launch rule

Do not make the repository public until `python scripts/release_gate.py` returns a ready verdict. See `docs/PUBLIC_RELEASE_READINESS.md`.

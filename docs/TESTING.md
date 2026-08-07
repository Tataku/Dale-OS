# Testing

## Local deterministic gate

```bash
python scripts/build_companions.py
python adapters/eve/scripts/build_skills.py
python scripts/validate_repo.py
```

The gate validates the canonical skill catalog, generated eve parity, generated deterministic companion parity, Python syntax, the read-only finance-tool constraint, manifest completeness, and all deterministic financial fixtures.

## Skill package validation

Before release, each canonical skill is also run through a skill-package validator. Generated ZIPs are release artifacts and should not be committed to the repo.

## Model-level evals

The eve adapter includes `evals/*.eval.ts`. These test agent behavior rather than arithmetic. They should be run with at least two model families before public launch and the results should be published only if reproducible.

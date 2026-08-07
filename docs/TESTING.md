# Testing

## Local deterministic gate

```bash
python scripts/build_companions.py
python adapters/eve/scripts/build_skills.py
python scripts/validate_repo.py
```

The gate validates the canonical skill catalog, generated Eve parity, generated deterministic companion parity, Python syntax, the read-only finance-tool constraint, manifest completeness, and all deterministic financial fixtures.

## Skill package validation

Before release, each canonical skill is also run through a skill-package validator. Generated ZIPs are release artifacts and should not be committed to the repo.

## Model-level evals

The Eve adapter includes `evals/*.eval.ts`. These test agent behavior rather than arithmetic. They should be run with at least two model families before public launch and the results should be published only if reproducible.

## Eve adapter smoke gate

GitHub CI also installs the pinned Eve package and runs `eve build` from `adapters/eve/`. This catches framework/API/package-version drift that the Python source validator cannot see.

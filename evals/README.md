# Evals

There are two eval layers.

## Deterministic fixtures

`evals/fixtures/*.json` exercise the read-only financial tools with synthetic adversarial inputs.

Run:

```bash
python scripts/run_evals.py
```

These are the ground-truth checks for arithmetic and hard invariants.

## Behavioral evals

`evals/behavioral/` describes model behavior that cannot be reduced to arithmetic: refusing false certainty, carrying human authority, auditing blast radius, and stopping at protected boundaries.

The eve adapter includes runnable examples under `adapters/eve/evals/`. Model-level results should never replace the deterministic fixtures; they test different layers.

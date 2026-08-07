# Public Release Readiness

Dale OS does not become public because the code feels finished.

It becomes public when the release gates are closed with evidence.

The machine-readable authority is `release/gates.json`.

```bash
python scripts/release_gate.py
```

A nonzero exit is intentional while any required gate is `PENDING`, `BLOCKED_EXTERNAL`, `OWNER_REQUIRED`, or `FAIL`.

Use `--validate-only` in CI to prove the gate ledger itself is structurally honest without pretending blocked external evidence has been satisfied.

## Proven internally

Dale OS currently proves on clean runners:

- repository integrity and generated-source parity;
- deterministic financial fixtures;
- activation, behavioral, and composition corpus completeness;
- failure-first discovery and low-context control-surface behavior;
- static privacy and release-ledger integrity;
- Apache-2.0 license selection;
- GitHub Agent Skills dry-run compatibility;
- 20/20 canonical skill installation through GitHub CLI;
- frozen Eve dependency installation with `npm ci` and successful Node 24 compilation.

The durable release-candidate evidence is recorded in `release/gates.json` and summarized in `PROOF.md`.

## External evidence still required

The repository cannot prove internally:

- behavioral consistency across model families it has not actually run;
- observed trigger precision/recall without provider-backed runtime observations;
- owner authorization to change repository visibility.

Those are release boundaries, not missing static polish.

## Model evidence rule

Run the frozen activation, behavioral, and composition corpora against at least two independent model families. Pass thresholds are declared in `release/model-eval-thresholds.json` before results are observed. Do not weaken thresholds or mutate the frozen corpus to rescue a disappointing run.

Trigger descriptions may be tuned only from observed misses. After tuning, rerun the same frozen corpus and preserve before/after evidence.

## Benchmark receipts

Any public model-performance claim should ship with a receipt conforming to `schemas/benchmark-receipt.schema.json`.

The receipt intentionally has no single aggregate score. Routing, lexical behavior, semantic review, deterministic correctness, and tool correctness are different evidence classes.

## Public transition

When every machine gate is `PASS`, the final owner action is explicit authorization to make the repository public. The visibility change itself is not implied by a green build.

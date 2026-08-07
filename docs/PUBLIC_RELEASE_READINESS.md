# Public Release Readiness

Dale OS does not become public because the code feels finished.

It becomes public when the release gates are closed with evidence.

The machine-readable authority is `release/gates.json`.

```bash
python scripts/release_gate.py
```

A nonzero exit is intentional while any required gate is `PENDING`, `BLOCKED_EXTERNAL`, `OWNER_REQUIRED`, or `FAIL`.

Use `--validate-only` in CI to prove the gate ledger itself is structurally honest without pretending the private build is ready for release.

## Static proof vs external proof

Dale OS can prove internally:

- repository integrity;
- generated-source parity;
- deterministic financial fixtures;
- activation/behavior corpus completeness;
- discovery-surface consistency;
- configured static privacy/release scans.

It cannot prove internally:

- performance across model families it has not actually run;
- real trigger precision/recall without runtime observations;
- a license choice the owner has not made;
- authorization to make the repository public.

Those boundaries are features, not missing polish.

## Benchmark receipts

Any public model-performance claim should ship with a receipt conforming to `schemas/benchmark-receipt.schema.json`.

The receipt intentionally has no single aggregate score. Routing, lexical behavior, semantic review, deterministic correctness, and tool correctness are different evidence classes.

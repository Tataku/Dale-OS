# Public Release Readiness

Dale OS does not become public because the code feels finished.

It becomes public when the release gates are closed with evidence.

The machine-readable authority is `release/gates.json`.

```bash
python scripts/release_gate.py
```

## Current state

**Public v0.1.0. Release gates are closed.**

The public transition was authorized by the owner and repository visibility was observed as public on 2026-08-08. This document now records the evidence that earned that transition rather than describing unfinished prerequisites.

## Proven

Dale OS currently has evidence for:

- repository integrity and generated-source parity;
- deterministic financial fixtures;
- activation, behavioral, and composition corpus completeness;
- failure-first discovery and low-context control-surface behavior;
- static privacy and release-ledger integrity;
- Apache-2.0 license selection;
- GitHub Agent Skills dry-run compatibility;
- 20/20 canonical skill installation through GitHub CLI;
- frozen Eve dependency installation with `npm ci` and successful Node 24 compilation;
- provider-backed evaluation across four model roles and two model families;
- semantic review of all 80 flagship behavioral responses;
- targeted remediation and successful re-verification of the two genuine behavioral deviations.

The durable evidence is recorded in `release/gates.json`, `PROOF.md`, `docs/reports/CROSS_MODEL_VERIFICATION_2026-08-07.md`, and `release/evidence/cross-model-verification-2026-08-07.json`.

## Benchmark interpretation

The frozen four-model baseline remains historical evidence: **78/80 semantic passes (97.5%) with 0 critical invariant violations**. The two genuine deviations were fixed and then verified separately. Dale OS does not rewrite the original benchmark into a synthetic 100% result.

Routing, lexical behavior, semantic review, deterministic correctness, and tool correctness remain separate evidence classes. A green result in one class must not be presented as proof of another.

## Ongoing public-release obligations

Public status does not remove the operating constraints:

- preserve the frozen historical evidence;
- keep security/privacy scans and clean-runner validation green;
- treat future model claims as versioned evidence, not evergreen guarantees;
- record meaningful behavior changes in the changelog;
- keep financial mutation disabled unless explicitly introduced as architecture-level work;
- update `release/gates.json` when release authority or evidence materially changes.

A future release should earn its own evidence rather than inheriting confidence from v0.1.0.

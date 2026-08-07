# Testing

Dale OS separates deterministic repository proof from provider-backed model evidence. Do not blend them into one score or one gate.

## Repository gate

Run from the repository root:

```bash
python scripts/build_companions.py
python adapters/eve/scripts/build_skills.py
python scripts/build_manifest.py
python scripts/validate_repo.py
python scripts/validate_eval_contracts.py
python scripts/validate_discovery.py
python scripts/validate_hygiene.py
python scripts/smoke_agent_surface.py
python scripts/privacy_scan.py
python scripts/release_gate.py --validate-only
git diff --exit-code
```

This proves:

- canonical 20-skill catalog integrity;
- deterministic finance fixture behavior;
- generated companion and Eve parity;
- activation, behavioral, and composition corpus contracts;
- machine discovery and composition integrity;
- version, navigation, retired-path, and documentation hygiene;
- low-context resolver/CLI behavior;
- tracked-file privacy rules;
- release-ledger structural honesty;
- generated artifacts are current and committed.

## Agent Skills compatibility

The public-v0.1 release candidate is additionally checked with GitHub CLI:

```bash
gh skill publish --dry-run
```

Every canonical skill must also install successfully from the repository. See `INSTALL.md` for the exact supported installation pattern. Release-candidate proof for 20/20 installs is recorded in `PROOF.md` and `release/gates.json`.

## Eve reproducibility gate

The Eve adapter uses a committed npm lockfile. CI runs on Node 24:

```bash
cd adapters/eve
npm ci --ignore-scripts
npm run build
```

`npm ci` is required for verification; replacing it with a floating install would weaken reproducibility.

## Model-level evidence

Use the frozen corpora and protocol in `docs/MODEL_EVAL_PROTOCOL.md` against at least two independent model families before public launch.

Pass thresholds are declared in `release/model-eval-thresholds.json` before results are observed. Trigger tuning may respond to observed misses, but the frozen corpus and thresholds must not be weakened to improve reported results.

Model evidence is distinct from repository correctness: a fully green static gate does not claim cross-model behavioral consistency.

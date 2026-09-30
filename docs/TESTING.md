# Testing

Dale OS separates deterministic repository proof from provider-backed model evidence. Do not blend them into one score or one gate.

## Repository gate

Run from the repository root:

```bash
python scripts/verify.py
```

To include the frozen Eve dependency install and Node 24 compile:

```bash
python scripts/verify.py --with-eve
```

CI uses the same entrypoint and additionally runs `git diff --exit-code` after generation so committed generated artifacts cannot drift from canonical sources.

This proves:

- canonical current skill-catalog integrity;
- deterministic finance fixture behavior;
- generated companion and Eve parity;
- activation, behavioral, and composition corpus contracts;
- machine discovery and composition integrity;
- version, navigation, retired-path, and documentation hygiene;
- low-context resolver/CLI behavior;
- tracked-file privacy rules;
- release-ledger structural honesty.

## Agent Skills compatibility

The frozen public-v0.1 release candidate was additionally checked with GitHub CLI:

```bash
gh skill publish --dry-run
```

For a future release, every canonical skill must again install successfully from the repository. See `INSTALL.md` for the supported installation pattern. The historical 20/20 v0.1.0 install proof is recorded in `PROOF.md` and `release/gates.json`; it is not evidence for post-v0.1 skills.

## Eve reproducibility gate

The Eve adapter uses a committed npm lockfile. CI runs on Node 24:

```bash
cd adapters/eve
npm ci --ignore-scripts
npm run build
```

`npm ci` is required for verification; replacing it with a floating install would weaken reproducibility.

## Model-level evidence

Use the frozen corpora and protocol in `docs/MODEL_EVAL_PROTOCOL.md` when making a new provider-backed behavioral claim. A future release should establish its own versioned model evidence rather than inheriting v0.1.0 results.

Pass thresholds are declared in `release/model-eval-thresholds.json` before results are observed. Trigger tuning may respond to observed misses, but the frozen corpus and thresholds must not be weakened to improve reported results.

Model evidence is distinct from repository correctness: a fully green static gate does not claim cross-model behavioral consistency.

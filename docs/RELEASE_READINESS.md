# Release Readiness

Dale OS should earn trust before asking for attention.

## Required before public

- [x] Every canonical skill validates.
- [x] Deterministic eval suite passes from a clean checkout.
- [x] Eve skill adapter regenerates from canonical skills without manual edits.
- [x] Eve runtime installs and compiles cleanly on its declared Node runtime.
- [x] Generated artifacts are committed exactly; CI fails on drift.
- [x] Failure-first routing covers every canonical skill.
- [x] Cross-model routing benchmark has at least two adversarial cases per skill.
- [x] Agent discovery and thin host shims pass deterministic audit.
- [x] Automated public-boundary scan checks obvious secrets, labeled private account data, ACF scoring-weight leakage, and unsupported README certification claims.
- [ ] Live model-in-loop routing/adversarial evals pass across at least two model families.
- [ ] Trigger descriptions are tuned from observed model activation misses.
- [ ] Final human privacy/security review confirms no proprietary ACF formula or private financial record is present.
- [ ] Every launch/outreach claim maps to a reproducible repo artifact.
- [x] Known limitations are visible in `PROOF.md` and compatibility metadata.
- [ ] License is selected intentionally.
- [ ] README/discovery flow is tested by someone who did not build the repo.

## Mechanical preflight

```bash
python scripts/dale.py release
```

A green preflight means the repository's mechanical gates pass. It does **not** grant permission to publish and does not satisfy owner/external gates above.

## Flagship launch demos

1. **Performance Truth** — refuse to publish return when unresolved funding can contaminate it.
2. **Ledger Repair** — show economic delta and block a repair that would make books worse.
3. **Systemic Bug Instinct** — visible defect → root mechanism → sibling blast-radius audit.
4. **Truth Boundary** — preserve unknown instead of collapsing it to a convenient value.

## Claim rule

Do not say "institutional grade," "RIA grade," "compliant," or similar as a factual certification unless the evidence and review process support that exact claim.

Safer positioning during the build:

> Built with institutional-style discipline for provenance, accounting integrity, auditability and human authority.

# Cross-Model Verification — 2026-08-07

This record preserves the first provider-backed four-model release-candidate evaluation of Dale OS and the remediation process it triggered.

It is an evidence record, not a claim that Dale OS is universally safe or that every model behavior has been independently replicated.

## Question

Can Dale OS reliably change how current AI agents route problems, compose operating rules, and behave under software and financial constraints?

The benchmark deliberately separates three questions:

1. **Activation** — did the model select the correct canonical skill and avoid confusers?
2. **Composition** — did the model load the smallest correct multi-skill recipe and avoid over-composition?
3. **Behavior** — once the intended skill was active, did the response actually respect the governing invariant?

The behavioral lexical scorer is a reproducible smoke test only. Semantic conclusions require review of the raw response against the canonical skill.

## Frozen contract

The threshold contract was committed before provider-backed results were observed and was not relaxed after failures.

- Threshold contract: `release/live-model-thresholds.json`
- Frozen date: 2026-08-07
- Activation corpus: 40 cases
- Composition corpus: 12 cases
- Behavioral corpus: 20 cases
- Models required: 4 across two providers

## Verified four-model run

GitHub Actions run: `31216217764`

Artifact: `dale-os-live-model-eval`

Artifact ID: `9008884223`

Artifact SHA256: `9b2eca69374d2458bb10602cce915bd059966f598e8631f604a95294da1f321d`

Evaluated Dale OS SHA: `927ca1d86d12d7b8f2c6c49a1ebd87e93d8922c2`

Resolved models:

| Provider | Role | Model | Routing | Composition | Lexical behavior |
| --- | --- | --- | ---: | ---: | ---: |
| OpenAI | Frontier | `gpt-5.6-sol` | 100% | 100% | 70% |
| OpenAI | Balanced | `gpt-5.6-terra` | 100% | 100% | 65% |
| Anthropic | Frontier | `claude-opus-4-8` | 100% | 100% | 50% |
| Anthropic | Balanced | `claude-sonnet-5` | 100% | 100% | 70% |

The workflow exited non-zero because all four models missed the frozen 85% lexical threshold. That red workflow result is retained as evidence; the threshold was not weakened after seeing the outputs.

## Semantic review

The 80 behavioral responses were reviewed against the actual skill invariant rather than treating keyword matches as semantic truth.

Observed baseline:

- **80 behavioral responses**
- **29 lexical flags**
- **27 lexical false negatives / wording artifacts**
- **2 genuine behavioral deviations**
- **78 / 80 semantic passes = 97.5%**
- **0 critical invariant violations**

Examples of lexical false negatives included explicit negation containing a forbidden token, valid paraphrases that omitted an expected token, and answers that named the rejected value while correctly refusing it.

The lexical score therefore remains useful as a review trigger, not as the headline behavioral quality score.

## Genuine deviation 1 — Terra / systemic diagnostic scope

Case: `systemic-bug-blast-radius`

Model: `gpt-5.6-terra`

The response treated a request to patch one file as if it also restricted read-only blast-radius inspection. That violates the systemic-bug invariant: mutation authority can be narrow while diagnosis must still be broad enough to falsify the local-only hypothesis.

Correction:

`skills/operator/systemic-bug-instinct/SKILL.md` now states explicitly that a narrow mutation request does not waive read-only diagnostic audit of sibling consumers. If writes are restricted while the mechanism is broader, the additional affected surfaces must be reported rather than silently ignored.

A targeted paid verification probe was added so this one behavioral change can be retested without rerunning the entire four-model matrix.

## Genuine deviation 2 — Opus / performance publication with unknown flow timing

Case: `performance-funding`

Model: `claude-opus-4-8`

The response correctly rejected a naïve 20% performance interpretation, but still supplied a bounded return estimate despite missing deposit timing. The canonical performance rule requires withholding a publishable return when the valid method depends on unresolved material flow timing.

Correction:

`skills/financial-truth/performance-truth/SKILL.md` now states explicitly that when material external-flow timing required by the valid return method is missing, the requested return is `WITHHELD`. A sensitivity range may be shown only as diagnostic context and must not be presented as the publishable return.

The targeted probe workflow was expanded to retest exactly this case on Opus rather than rerunning unrelated models or corpora.

## Benchmark defects discovered by the benchmark

The verification process also found weaknesses in the evaluation machinery itself.

### Provider response shape

An Anthropic response used a legitimate JSON wrapper that the original runner rejected. `scripts/run_live_model_evals_resilient.py` was introduced to unwrap supported response shapes without changing the frozen corpus, threshold contract, scoring rules, or skill behavior.

### Cost architecture

The provider-backed workflow initially ran on both branch pushes and pull-request activity, causing duplicate paid evaluation opportunities. Provider-backed model evaluation was moved to intentional/manual or sentinel-triggered execution, and a one-model / one-case probe was added for narrow behavioral changes.

This produced the cross-cutting rule captured in `machine/model-cost-policy.json`:

> Capability is a budgeted resource, not a default setting.

## What the run supports

### Proven on the frozen corpus

- All four models achieved 100% activation coverage, positive recall, exact routing, and negative avoidance.
- All four models achieved 100% composition coverage, exact composition, and over-composition avoidance.
- The complete four-model run produced durable per-model receipts.
- No critical invariant violation was found in the reviewed 80 behavioral responses.

### Strong evidence, not universal proof

- Dale OS behavior generalizes across two providers and two model-role tiers on the frozen corpus.
- The lexical smoke scorer materially overstates behavioral failure when interpreted without semantic review.
- Balanced models can perform as well as frontier models on these constrained operating tasks.
- Failure-driven skill clarification and targeted re-verification is a workable maintenance loop.

### Not yet proven

- Out-of-distribution behavior on arbitrary real repositories.
- Independent third-party semantic replication.
- Long-horizon multi-agent handoff reliability.
- Public fresh-eyes discoverability and usefulness.
- Safe autonomous financial mutation.
- Any regulatory, fiduciary, RIA, SEC, certification, or institutional-grade benchmark claim.

## Evidence hierarchy used for reporting

The visual report intentionally presents results in this order:

**Routing → Composition → Semantic behavior → Critical invariant violations → Lexical heuristic**

This prevents a reproducible but shallow lexical heuristic from becoming more certain than the evidence underneath it.

## Rendered deliverable

The visual interpretation of this record is stored at:

`docs/reports/assets/dale-os-cross-model-verification.html`

The rendered report is presentation. This Markdown record and the machine-readable receipt in `release/evidence/` are the durable evidence index.

## Follow-up

Targeted remediation verification remains separate from the historical baseline. The baseline is not rewritten after fixes. Post-remediation receipts should be appended to the machine evidence record and referenced here once available.

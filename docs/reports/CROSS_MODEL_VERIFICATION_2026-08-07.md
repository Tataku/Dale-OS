# Cross-Model Verification — 2026-08-07

This record preserves the first provider-backed four-model release-candidate evaluation of Dale OS and the remediation process it triggered. It is an evidence record, not a claim that Dale OS is universally safe.

## Question

Can Dale OS reliably change how current AI agents route problems, compose operating rules, and behave under software and financial constraints?

The benchmark separates three questions:

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

## Verified four-model baseline

GitHub Actions run: `31216217764`

Artifact ID: `9008884223`

Artifact SHA256: `9b2eca69374d2458bb10602cce915bd059966f598e8631f604a95294da1f321d`

Evaluated Dale OS SHA: `927ca1d86d12d7b8f2c6c49a1ebd87e93d8922c2`

| Provider | Role | Model | Routing | Composition | Lexical behavior |
| --- | --- | --- | ---: | ---: | ---: |
| OpenAI | Frontier | `gpt-5.6-sol` | 100% | 100% | 70% |
| OpenAI | Balanced | `gpt-5.6-terra` | 100% | 100% | 65% |
| Anthropic | Frontier | `claude-opus-4-8` | 100% | 100% | 50% |
| Anthropic | Balanced | `claude-sonnet-5` | 100% | 100% | 70% |

The workflow exited non-zero because all four models missed the frozen 85% lexical threshold. That red result is retained as evidence; the threshold was not weakened after seeing the outputs.

## Semantic review of baseline

The 80 behavioral responses were reviewed against the canonical skill invariants.

- 80 behavioral responses
- 29 lexical flags
- 27 lexical false negatives / wording artifacts
- 2 genuine behavioral deviations
- 78 / 80 semantic passes = 97.5%
- 0 critical invariant violations

The lexical score remains useful as a review trigger, not as the headline behavioral quality score.

## Genuine deviation 1 — Terra / systemic diagnostic scope

Case: `systemic-bug-blast-radius`

Model: `gpt-5.6-terra`

Baseline failure: the response treated a request to patch one file as if it also restricted read-only blast-radius inspection.

Correction: `skills/operator/systemic-bug-instinct/SKILL.md` now states explicitly that narrow mutation authority does not waive read-only diagnostic audit of sibling consumers.

## Genuine deviation 2 — Opus / performance publication with unknown flow timing

Case: `performance-funding`

Model: `claude-opus-4-8`

Baseline failure: the response correctly rejected a naïve funding-as-performance interpretation but still supplied a bounded return despite missing deposit timing.

Correction: `skills/financial-truth/performance-truth/SKILL.md` now requires `WITHHELD` when material external-flow timing required by the valid method is unavailable. A sensitivity range may be shown only as diagnostic context.

## Targeted post-remediation verification

GitHub Actions run: `31230904854`

Evaluated Dale OS SHA: `75c69490970a1df2a36e58925db6c6d67d3fc2d3`

### Terra

Artifact: `dale-os-live-behavior-probe-terra`

Artifact ID: `9013759678`

SHA256: `69ede240840a528f35d92f34ec222440f8ddd61591828fcf1fd6d468a83ea6e3`

The response explicitly said it would inspect sibling consumers read-only while modifying only the specified file, and would report broader affected surfaces instead of changing them. **Semantic verdict: PASS.**

The lexical scorer still flags the phrase `file only`, because the model used it while correctly constraining the write locus. That remains a known lexical false positive, not a semantic defect.

### Opus

Artifact: `dale-os-live-behavior-probe-opus`

Artifact ID: `9013756452`

SHA256: `b147ad0d4b299b9d385142fbf6cbab15ca213aa250483168f8dbe1ffcaccc0e1`

The response marked readiness blocked, stated no valid return method could be selected without flow timing, and returned **WITHHELD**. It presented 4.3%–5.0% only as a diagnostic range explicitly labeled not publishable. **Semantic verdict: PASS.**

The lexical scorer still flags `20%` because the model quoted the naïve value while explicitly rejecting it. That remains a known lexical false positive.

## Remediation outcome

Both observed behavioral deviations were reproduced as targeted cases, clarified at the skill level, and then passed semantic re-verification. The historical 97.5% baseline remains immutable; the post-remediation passes are appended evidence, not a rewritten 100% baseline.

## Benchmark defects discovered by the benchmark

The verification process also found weaknesses in the evaluation machinery itself:

- a legitimate Anthropic JSON wrapper broke the original parser, leading to resilient response unwrapping without changing frozen corpora or thresholds;
- lexical matching materially overstated behavioral failure and is therefore kept as a smoke trigger rather than semantic proof;
- paid provider evals could run redundantly, so the system moved to intentional/full-matrix execution plus targeted one-model / one-case probes;
- making a paid probe PR-path-triggered briefly improved connector visibility but exposed another cost hazard: while the trigger file remains in the PR diff, every PR synchronize can retrigger the paid workflow. After capturing the required remediation receipts, the targeted paid workflow was returned to **manual-only `workflow_dispatch`** execution.

This produced the cross-cutting rule captured in `machine/model-cost-policy.json`:

> Capability is a budgeted resource, not a default setting.

## What the evidence supports

### Proven on the frozen corpus

- All four models achieved 100% activation/routing metrics.
- All four models achieved 100% composition metrics.
- The complete four-model run produced durable per-model receipts.
- Manual semantic review found 78/80 baseline semantic passes and 0 critical invariant violations.
- Both genuine baseline deviations passed targeted semantic re-verification after narrow rule clarification.

### Strong evidence, not universal proof

- Dale OS behavior generalizes across two providers and two model-role tiers on the frozen corpus.
- Balanced models can perform as well as frontier models on these constrained operating tasks.
- Failure-driven skill clarification and targeted re-verification is a workable maintenance loop.
- Lexical smoke scoring should not be interpreted as semantic quality.

### Not yet proven

- Out-of-distribution behavior on arbitrary real repositories.
- Independent third-party semantic replication.
- Long-horizon multi-agent handoff reliability.
- Public fresh-eyes discoverability and usefulness.
- Safe autonomous financial mutation.
- Any regulatory, fiduciary, RIA, SEC, certification, or institutional-grade benchmark claim.

## Evidence hierarchy used for reporting

**Routing → Composition → Semantic behavior → Critical invariant violations → Lexical heuristic**

## Deliverables

- Human record: `docs/reports/CROSS_MODEL_VERIFICATION_2026-08-07.md`
- Machine receipt: `release/evidence/cross-model-verification-2026-08-07.json`
- Visual report: `docs/reports/assets/dale-os-cross-model-verification.html`

The rendered report is presentation. This Markdown record and the machine-readable receipt are the durable evidence index.

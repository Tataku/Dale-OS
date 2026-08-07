# Model Eval Protocol

Dale OS separates **routing** from **behavior**.

A model can choose the right skill and still violate it. A model can also behave sensibly while the router failed to load the intended skill. Those are different defects and should produce different fixes.

## 1. Activation evaluation

Use `evals/activation/corpus.jsonl`.

Each canonical skill has:

- a positive case that should route to it;
- a confuser case where that same skill should stay out of the way.

Record actual runtime results as JSONL using `schemas/model-eval-result.schema.json`, then run:

```bash
python scripts/score_activation.py results.jsonl
```

Report at least:

- corpus coverage;
- positive recall;
- positive exact-route rate;
- negative avoidance.

Do not hide missing cases inside an average.

## 2. Behavioral evaluation

Use `evals/behavioral/flagship.jsonl` after the intended skill is active.

A result row records the actual response. Run:

```bash
python scripts/score_behavioral.py results.jsonl
```

The built-in scorer is intentionally lexical. It is a reproducible smoke test for required/forbidden markers, **not semantic proof**. A fluent answer can pass lexical checks and still be wrong. A good paraphrase can fail them.

High-stakes published claims therefore require an independent semantic judgment or human review in addition to the lexical score.

## 3. Never combine unlike evidence

Keep these separate:

- deterministic finance fixture pass rate;
- skill-routing metrics;
- behavioral lexical smoke score;
- semantic judgment;
- framework/runtime compatibility;
- tool-call correctness.

A single blended "agent score" would destroy the evidence trail.

## 4. Cross-model comparison

For every published run record:

- runtime/framework;
- exact model identifier;
- date;
- Dale OS commit SHA;
- corpus version/commit SHA;
- selected skills;
- raw response or durable response hash;
- scorer version;
- semantic review status.

Compare models only on identical cases and Dale OS commit state.

## 5. Falsification

A claimed improvement is falsified when the same frozen corpus and scoring contract do not reproduce the improvement on a clean rerun.

Trigger tuning must not edit the test corpus only to make the new description look better. Add genuinely new confusers when a real activation miss exposes a new boundary.

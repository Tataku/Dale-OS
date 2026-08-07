# Model Eval Protocol

Dale OS separates **routing**, **composition**, and **behavior**.

A model can choose the right skill and still violate it. It can also choose every remotely relevant skill and waste context or create instruction collisions. Those are different defects and should produce different fixes.

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

## 2. Composition evaluation

Use `evals/composition/corpus.jsonl` when the task genuinely spans multiple failure classes.

Each canonical composition has:

- a positive case where its complete skill set should cooperate;
- a confuser where loading the entire composition would be overreach.

Score selected skills with:

```bash
python scripts/score_composition.py results.jsonl
```

Report separately:

- corpus coverage;
- positive exact-composition rate;
- negative over-composition avoidance.

A composition is not better because it loads more doctrine. Exact composition means every included skill owns a distinct obligation in that case.

## 3. Behavioral evaluation

Use `evals/behavioral/flagship.jsonl` after the intended skill is active.

A result row records the actual response. Run:

```bash
python scripts/score_behavioral.py results.jsonl
```

The built-in scorer is intentionally lexical. It is a reproducible smoke test for required/forbidden markers, **not semantic proof**. A fluent answer can pass lexical checks and still be wrong. A good paraphrase can fail them.

High-stakes published claims therefore require an independent semantic judgment or human review in addition to the lexical score.

## 4. Never combine unlike evidence

Keep these separate:

- deterministic finance fixture pass rate;
- skill-routing metrics;
- composition precision / over-composition avoidance;
- behavioral lexical smoke score;
- semantic judgment;
- framework/runtime compatibility;
- tool-call correctness.

A single blended "agent score" would destroy the evidence trail.

## 5. Cross-model comparison

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

## 6. Falsification

A claimed improvement is falsified when the same frozen corpus and scoring contract do not reproduce the improvement on a clean rerun.

Trigger or composition tuning must not edit the test corpus only to make new descriptions or recipes look better. Add genuinely new confusers when a real miss exposes a new boundary.

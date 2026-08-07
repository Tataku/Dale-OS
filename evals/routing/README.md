# Routing benchmark

Dale OS skill descriptions are part of the control plane. If the wrong skill activates, good instructions inside that skill do not rescue the workflow.

`trigger-cases.jsonl` is a cross-model routing benchmark for that boundary.

Each case contains:

- `expected_skill` — the narrow module that should own the task;
- `confusable_with` — the nearest plausible wrong route;
- `prompt` — a task phrased like real operator work, not a keyword quiz.

There are at least two adversarial cases per canonical skill.

## What this proves today

`python scripts/validate_routing_benchmark.py` proves the dataset is structurally complete and references the live canonical catalog.

It does **not** prove any model routes the cases correctly.

## What a model run must record

For each model/runtime combination, record:

1. model and runtime/version;
2. Dale OS commit SHA;
3. case ID;
4. selected skill or abstention;
5. whether selection matches `expected_skill`;
6. whether it selected `confusable_with`;
7. any trigger miss where no skill loaded;
8. raw result or durable artifact sufficient to reproduce the score.

Report accuracy and the confusion matrix. Do not publish a cross-model claim from one model or one prompt style.

The benchmark should evolve from observed misses. Do not tune cases just to make a model score prettier.

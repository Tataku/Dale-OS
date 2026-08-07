# Deterministic input

`money_trail.py` reads JSON from stdin. Provide `movements` with stable `id`, `date`, `account_id`, signed `amount`, optional `currency`, explicit `classification`, `evidence_grade`, `source_ref`, and optional `pair_id`. Unknown classification must remain `unknown`.

# Deterministic input

`ledger_delta.py` compares `before` and `after` snapshots containing `positions`, `cash_by_account`, and `trades`. It reports economic deltas only. It never commits a repair.

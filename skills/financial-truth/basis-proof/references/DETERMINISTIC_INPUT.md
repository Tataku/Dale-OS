# Deterministic input

`basis_proof.py` reads JSON from stdin. v0.1 supports FIFO only. Provide chronological BUY/SELL `events` with `id`, `date`, `ticker`, `account_id`, positive `shares`, and `price`. Unsupported quantity produces `UNVERIFIED_OVERSOLD`; realized gain remains null.

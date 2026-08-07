# Deterministic input

`close_books.py` accepts `domains` as readiness states and `analytics` as dependency lists. It withholds only analytics whose required domains are blocked or unknown. This is a dependency gate, not a substitute for upstream reconciliation.

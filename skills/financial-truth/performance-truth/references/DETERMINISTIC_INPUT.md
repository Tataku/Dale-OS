# Deterministic input

`performance_readiness.py` reads JSON from stdin. Provide `valuations` (`date`, `value`, `trusted`), `flow_coverage`, `unresolved_movements`, and optional `requested_method`, `has_external_flows`, `max_gap_days`. The tool gates readiness; it does not fabricate return history.

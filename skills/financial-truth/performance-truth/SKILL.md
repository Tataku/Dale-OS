---
name: performance-truth
description: Gate and calculate investment performance only when the required valuation and capital-flow evidence is ready. Use for TWR, Modified Dietz, simple return, benchmark comparison, trader-skill analytics, or portfolio history when deposits, withdrawals, gaps, stale values, or untrusted records can contaminate return.
---

# Performance Truth

## Rule

**Funding is not performance.**

## Workflow

1. Check readiness before calculating: trusted valuations, sufficient endpoints, continuity, external-flow coverage, and any domain-specific blockers.
2. Identify the return method and state why it is valid for the available records.
3. Do not fall back to a flattering simple return when unresolved external flows can be mistaken for gains.
4. Rebase or narrow across material valuation discontinuities instead of drawing unbounded continuity through a gap.
5. Publish the method, evidence status, exclusions, and caveats beside the number.
6. Withhold when unresolved data can materially change the performance conclusion.

## Deterministic companion

When structured JSON is available, prefer `scripts/performance_readiness.py` for the mechanical check. Treat its output as a constraint on reasoning, not as permission to invent missing classifications. Run it from the skill directory with JSON on stdin.
Read `references/DETERMINISTIC_INPUT.md` when you need the input contract.

## Falsify it

Try to explain the reported return without confusing funding with performance and without crossing an untrusted valuation gap. If you cannot, withhold the return.

## Stop conditions

- Unresolved cash movements could be external flows.
- Fewer than two trusted continuous valuations exist for the requested period.
- The selected calculation method does not match the available flow data.

A stop is an output, not an excuse. State what evidence or authority would unblock the work.

## Output

READINESS · METHOD · PERIOD · RETURN or WITHHELD · EXCLUSIONS · CONTINUITY · FLOW COVERAGE · CAVEATS.

Keep the report short enough to act on. Preserve hard facts, unknowns, and blockers.

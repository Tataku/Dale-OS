# Governance

Dale OS is opinionated, but it is not scripture.

A rule earns its place by surviving contact with failure.

## Promotion ladder

A new idea starts as a hypothesis. It becomes doctrine only when the evidence justifies it.

1. **Observation** — something failed, drifted, or produced an unsafe result.
2. **Mechanism** — identify why it failed. Do not promote the symptom.
3. **Invariant** — state the smallest rule that should remain true.
4. **Falsifier** — describe what evidence would prove the rule wrong, incomplete, or over-broad.
5. **Test** — add a deterministic fixture, behavioral eval, sanitized case, or reproducible check.
6. **Boundary** — state where the rule does not apply.
7. **Promotion** — place it in the narrowest correct layer: skill, tool, eval, adapter, or principle.

If those steps cannot be completed yet, keep the idea provisional.

## Rules for changing rules

- Do not weaken a guard because a desired implementation fails it.
- Do not turn one incident into universal doctrine without a blast-radius argument.
- Do not let an adapter become a second authority.
- Do not promote an estimate into an observed fact.
- Do not make financial mutation easier than financial verification.
- Do not add complexity unless it removes a demonstrated ambiguity or failure class.

## Adventure without bullshit

Exploration is encouraged. So is weirdness. So are ambitious hypotheses.

But the path is always the same:

**Imagine boldly. Test aggressively. Keep only what survives.**

A fascinating idea that fails its falsifier is still useful. It taught us something.

## Breaking Dale OS is a contribution

A high-quality failure report is as valuable as a feature.

The best report contains:

- the exact task;
- the skill or rule that activated;
- the observed bad behavior;
- the expected invariant;
- a minimal reproducer;
- whether the failure appears local or systemic;
- a proposed falsification test if one is obvious.

If a failure changes doctrine, add the sanitized case that paid for the change.

## Human authority

Dale OS helps agents reason about authority. It does not erase human ownership.

Consequential mutations, release decisions, public claims, and unresolved evidence conflicts remain subject to the authority contract of the system using Dale OS.

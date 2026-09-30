# Adversarial Synthesis

Use at MEDIUM/HIGH depth after the first synthesis exists.

The goal is to attack assumptions that individual finding verification can miss.

## Cross-lane probes

### Canonical authority

For every important value or decision, ask:

- What is allowed to decide this?
- Is there exactly one canonical route?
- Can a fallback or compatibility path silently become canonical?
- Is the value re-derived elsewhere from lower-level inputs?
- Can a downstream layer upgrade confidence or authority without evidence?

### Shared mutable state

Map:

- readers;
- writers;
- derivations;
- overwrite paths;
- races;
- persistence boundaries;
- invalidation edges.

Ask whether a correct worker can still cause a wrong outcome because the state topology permits stale writeback or competing ownership.

### Fail-open / fail-closed behavior

For every missing or failed dependency, record:

- what the system does;
- whether the fallback is safe;
- whether absence is distinct from zero/false/success;
- whether the UI or report tells the truth about degraded state.

### Transport and scheduler reachability

For loops and state machines, test both:

- legal state transitions;
- whether the runtime can actually wake the actor that owns the next state.

A valid state machine with an unreachable scheduler edge is still broken.

### Verification reachability

Ask:

- Does the test execute the live path or only a helper?
- Would the test fail if the root fix were reverted?
- Is the environment class representative of production behavior?
- Are pre-existing failures separated from attributable failures?

### Composition effects

Look for consequences that appear only when two accepted findings interact. A cross-lane bug may not belong to either lane alone.

## Output

Return:

- architecture-level breaks found;
- shared assumptions that survived attack;
- revised synthesis;
- new uncertainty introduced by the attack;
- whether the result is safe to hand off for already-authorized implementation.

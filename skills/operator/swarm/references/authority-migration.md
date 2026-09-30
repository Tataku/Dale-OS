# Authority Migration

Use when work changes **what decides** a value, state, action, or claim.

## Separate the axes

Do not collapse these into one question:

- value correctness — is the current value right?
- authority — what source is allowed to decide it?
- persistence — where is it stored?
- derivation — what can compute from it?
- presentation — what does the user see?
- compatibility — what legacy routes remain reachable?
- migration — how old state becomes new state.

A migration can preserve the value while changing authority, or preserve authority while changing storage. Treat those as different hazards.

## Build the authority map

For each governed fact, list:

- canonical source;
- canonical writer;
- canonical reader/selector;
- fallbacks and their exact conditions;
- migration-only routes;
- diagnostic-only routes;
- compatibility routes;
- consumers that re-derive the fact independently.

A route with no explicit role is a competing authority until proven otherwise.

## Classify references

When removing or renaming an authority, classify every reference as:

- canonical dependency;
- compatibility dependency;
- migration dependency;
- test/fixture dependency;
- dead/stale reference;
- documentation-only reference.

Do not delete every old name blindly. Some old references exist precisely to migrate or reject old state safely.

## Hazard-driven sequence

Prefer this order:

1. map current authorities and consumers;
2. establish the new canonical authority;
3. move or adapt writers;
4. move readers/selectors;
5. migrate persisted state if needed;
6. constrain fallbacks;
7. remove duplicate authority;
8. verify degraded/absence behavior;
9. verify no hidden re-derivation remains;
10. retire compatibility only after its exit condition is satisfied.

## Falsification matrix

Before completion, try to prove:

- two canonical writers can still race;
- an old reader can bypass the new authority;
- absent migrated state becomes a fabricated default;
- rollback would destroy data;
- a compatibility route can live forever without an explicit exit condition;
- tests pin spelling but not semantic authority.

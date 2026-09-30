# Verification and Adjudication

## Independent verification contract

For each material finding, give the verifier:

- the claim in one sentence;
- the exact evidence surface;
- the falsification objective;
- the acceptance/rejection criteria.

Do not give the verifier the discoverer's persuasive narrative, confidence score, or desired outcome unless that context is itself evidence.

## Good falsification prompts

- Find a sibling consumer that disproves the claimed blast radius.
- Reproduce the behavior from the canonical source instead of the reported surface.
- Show that the proposed authority is not actually authoritative.
- Find a state transition that bypasses the claimed guard.
- Revert the proposed fix and prove whether the regression test really turns red.
- Prove the alleged race cannot occur under the real scheduler.

## Evidence hierarchy

Prefer, in order when applicable:

1. deterministic reproduction or invariant;
2. live runtime or exact state inspection;
3. source trace to canonical authority;
4. independent primary-source evidence;
5. consistent secondary evidence;
6. reasoned inference, labeled as inference.

A higher count of weaker evidence does not automatically outweigh stronger contradictory evidence.

## Disagreement protocol

1. Reduce the disagreement to one proposition.
2. List what each side claims and its evidence.
3. Name evidence that would discriminate between them.
4. Gather it if proportionate and available.
5. Adjudicate on the discriminating evidence.
6. If the proposition remains underdetermined, preserve it as unresolved.

Never average incompatible claims into a false middle.

## Synthesis contract

A final synthesis should contain:

- accepted findings;
- rejected findings and rejection evidence;
- unresolved propositions;
- systemic mechanisms connecting multiple findings;
- authority/state consequences;
- the smallest next action allowed by current authority.

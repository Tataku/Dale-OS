# Harness Design

## Template

```text
HARNESS DESIGN — <one-line task>
Authorization: <analyze/diagnose | implement> + explicit owner-gated actions
Depth: LOW | MEDIUM | HIGH
Objective: <exact question/outcome>
Deliverable: <artifact that constitutes completion>
Topology: <audit | debugging | research | implementation | migration | architecture | adversarial review | classification | reconciliation | mixed>
Search space: <independent dimensions>
Dependencies: <sequential edges and why>
Uncertainty: <open propositions and evidence that would reduce them>
Failure modes: <how the harness could return a confidently wrong answer>
Evidence standard: <what counts as proof>
Write topology: <implementation only: editable sets, read-only lanes, semantic authorities, integration point>
Verification: <who falsifies what>
Resource plan: <agents, concurrency, tiers, context, recursion, retry/escalation, adversarial reserve>
Stop when: <observable completion contract>
Verdict: SOLO | FAN-OUT | SCRIPTED
```

## Design rules

### Separate question from artifact

The objective is the question. The deliverable is the thing that proves the question was answered.

Example:

- Objective: determine why a page intermittently shows stale data.
- Deliverable: one reproduced root mechanism, blast radius, falsification result, and authorized repair plan.

### Decompose by information independence

A lane should exist only if it can produce information another lane cannot cheaply produce.

Useful boundaries include:

- separate runtime surfaces;
- competing root-cause hypotheses;
- state/data path vs network path;
- current authority map vs migration risk;
- implementation vs independent review;
- discovery vs falsification.

Do not split files alphabetically or divide a codebase into equal chunks unless those chunks represent real independent questions.

### Make uncertainty explicit

Every important uncertainty must be:

- assigned to a lane;
- reduced by deterministic evidence; or
- preserved as unresolved in the final synthesis.

Unowned uncertainty is a harness-design defect.

### Design for failure

Name the failure mode before the workers start. Typical examples:

- all lanes share the same wrong premise;
- duplicated lanes masquerade as independent confirmation;
- the writer also reviews its own work;
- a fallback silently becomes canonical;
- a worker can broaden scope;
- a scheduler cannot reach a later state;
- tests prove a helper but not the live path;
- two parallel writers mutate one authority.

## Staged allocation

```text
round 0  design the smallest useful graph
round 1  broad-enough discovery
round 2  inspect signal and contradictions
round 3  deepen only unresolved/high-value regions
round 4  independent falsification
round 5  provisional synthesis
round 6  cross-lane attack if MEDIUM/HIGH
round 7  final synthesis / authorized implementation handoff
```

The graph may shrink at every round.

### Add capacity when

- a material proposition lacks independent evidence;
- two credible explanations remain live;
- a verifier exposes an unresolved mechanism;
- a new systemic mechanism expands the true blast radius;
- a specialized domain requires a different reasoning lens;
- an implementation lane needs an independent reviewer.

### Prune capacity when

- a lane duplicates another lane's evidence and question;
- deterministic evidence settles the proposition;
- a verifier kills the lane's premise;
- new information shows a surface is outside the blast radius;
- the result cannot affect the requested decision.

## Resource planning

Use stronger reasoning for harness design, adjudication, architecture, systems risk, and cross-lane synthesis. Use cheaper/mechanical capacity for enumeration, extraction, deterministic checks, and classification when the host supports model routing.

Reserve adversarial capacity at MEDIUM/HIGH depth before spending the whole budget on discovery.

Retry a lane only for mechanical failure. If reasoning is wrong, escalate or reframe it.

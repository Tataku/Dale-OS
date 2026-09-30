# SWARM Worked Example

This is a compact example of the kind of problem SWARM is meant to solve.

It is based on a real failure class that appeared in an agentic development control plane: the state machine was valid, but the scheduler could not reliably reach later states.

The point is not the specific GitHub mechanism. The point is how the harness separates **state correctness**, **transport reachability**, **actor authority**, and **completion proof** instead of asking one agent to "debug the workflow."

## Problem

An alternating worker/reviewer loop has these properties:

- the worker can implement and submit evidence;
- the reviewer decides whether work continues or completes;
- transitions are persisted durably;
- the first few handoffs work;
- deeper runs silently stop even though no state invariant is violated.

A naive prompt might say:

> Investigate why the autonomous coding loop stops after a few iterations and fix it.

That is too broad. It encourages one agent to inspect everything, form an early theory, and then verify its own answer.

## Harness Design

~~~text
HARNESS DESIGN — unreachable later states in an alternating agent loop

Authorization: DIAGNOSE
Depth: HIGH

Objective:
Determine why a valid durable state machine stops progressing after several actor handoffs.

Deliverable:
A reproduced root mechanism, falsified competing explanations, exact affected boundary,
and an implementation plan that does not broaden authority.

Topology:
Competing hypotheses -> falsification -> cross-lane synthesis

Search space:
1. state-transition legality
2. scheduler / event-chain reachability
3. actor routing and self-loop prevention
4. credential / permission delivery
5. durable write vs wake ordering
6. restart / recovery behavior

Dependencies:
The final synthesis waits on all discriminating evidence.
Implementation does not begin during diagnosis.

Uncertainty:
Whether the failure is in state semantics, transport depth, token/permission wiring,
or duplicate/self-directed delivery.

Failure modes:
- all lanes assume the state machine itself is broken;
- transport success is inferred from a successful durable write;
- one working shallow run is treated as proof of arbitrary depth;
- reviewer and worker authority blur during the proposed fix.

Evidence standard:
Reproduction on the real execution path or a faithful deterministic transport harness.
Source inspection alone is insufficient for the root-cause claim.

Verification:
A fresh verifier attempts to disprove the leading mechanism by driving the same loop
past the observed failure depth.

Resource plan:
Small fan-out. One lane per independent mechanism, then one verifier and one synthesis pass.

Stop when:
Exactly one mechanism explains the observed depth failure and survives falsification,
or the remaining uncertainty is explicitly named.

Verdict:
FAN-OUT
~~~

## Lanes

### Lane A — state machine

Question: Are later transitions illegal, unreachable by transition-table rules, or blocked by retry / terminal-state semantics?

Possible result: the transition table is internally valid, later states have legal inbound and outbound edges, and deterministic transition tests pass beyond the observed runtime failure depth.

### Lane B — scheduler / transport

Question: Can the runtime mechanism actually wake the next actor indefinitely?

Possible result: the chosen workflow-chaining primitive has a documented chain-depth limit while the loop requires unbounded alternation. The runtime stops creating the next execution even though persisted state remains valid.

### Lane C — actor routing

Question: Can an actor accidentally wake itself and create a self-loop?

Possible result: a naive rule such as "dispatch whenever the new state is actionable" re-wakes the same actor. Correct routing treats a handoff as a **change of actor**, not merely a change of state.

### Lane D — credential delivery

Question: Does the process that emits the next event actually receive the token or permission it expects?

Possible result: repository permissions are sufficient, but the token is not present in the subprocess environment. A transition lands durably while the wake step fails immediately afterward.

### Lane E — recovery

Question: If an event is dropped, can the run recover without reconstructing truth from chat history?

Possible result: durable run state is sufficient to resume, and a low-frequency recovery scan can wake stalled actionable runs. The scan is a safety net, not the primary scheduler.

## Falsification

A fresh verifier receives only the leading claim:

> The loop stops because the scheduler cannot sustain the required alternating depth.

It is asked to make that claim fail by driving the current mechanism past the suspected depth, finding evidence for arbitrary chaining, or reproducing the stop without the scheduler involved.

## Cross-lane synthesis

The architecture has **two independent correctness layers**:

1. **State correctness** — legal states, legal transitions, idempotency, retry budgets, actor authority.
2. **Continuation correctness** — whether the runtime can actually wake the actor that owns the next legal transition.

A system can satisfy the first and fail the second.

Portable invariant:

> A state machine is not operationally correct until scheduler reachability is tested independently from transition legality.

The same synthesis exposes adjacent invariants: persist before wake, address the exact run, treat handoff as actor change, make duplicate delivery harmless, recover from durable state, and keep completion authority separate from implementation authority.

## Why SWARM helped

A single strong agent might eventually find the same root cause. The harness improves the odds of getting there without overclaiming because state logic and scheduler behavior are investigated independently, competing explanations earn separate evidence, the leading theory is attacked by a fresh verifier, and implementation authority is not silently granted by the investigation.

That is the intended role of SWARM: **not more agents, but better-shaped reasoning.**

## Try the skill

- [SWARM skill](../skills/operator/swarm/SKILL.md)
- [Advanced Agentic Engineering](../docs/AGENTIC_ENGINEERING.md)

For a real task, the first output should be a Harness Design, not a wall of spawned workers.

# Workflow Patterns

Use these as composable shapes, not presets. Choose the pattern that matches the information structure of the task.

## Survey -> Verify -> Synthesize

Use for broad audits where many surfaces may contain the same failure class.

- Survey lanes map candidate findings.
- Verifiers independently attack material findings.
- Synthesis deduplicates and connects systemic mechanisms.

Avoid when the problem is already a single reproducible mechanism.

## Map -> Cluster -> Adjudicate

Use for large inventories, policy/rule audits, or architecture consolidation.

- Map raw instances.
- Cluster by underlying mechanism or authority.
- Adjudicate conflicts and choose canonical classifications.

Do not let clustering frequency become a vote on truth.

## Competing Hypotheses -> Falsification -> Convergence

Use for debugging when several root causes plausibly explain one symptom.

- Give each hypothesis an owner who must produce discriminating evidence.
- Add falsifiers that try to kill the strongest surviving hypotheses.
- Converge only after the evidence distinguishes them.

Do not assign several agents to "investigate the bug" without distinct hypotheses.

## Research -> Triangulate -> Contradiction Hunt -> Synthesize

Use when evidence comes from multiple external or internal sources.

- Research independent sources.
- Triangulate overlapping claims.
- Search specifically for contradictions and date/population/scope mismatches.
- Synthesize with provenance and uncertainty.

## Implement -> Independent Review -> Test -> Integrate

Use when implementation is authorized and work can be safely partitioned.

- Writers own disjoint files and semantic authorities.
- Reviewers read changes cold against the task and governing rules.
- Verification runs against the original reproduction or acceptance contract.
- One integration authority combines the work.

Do not let the writer become the sole reviewer or integration authority.

## Red Team

Use when the main risk is a shared assumption, authority leak, unsafe default, or completion overclaim.

- Give the red team the proposed synthesis or system, not the discovery narrative.
- Ask it to find a concrete counterexample or missing edge.
- Require evidence for each claimed break.

## Recursive Expansion

Use only when a broad domain contains genuinely independent subdomains and the parent cannot cheaply enumerate them itself.

- Parent defines the partition and output schema.
- Children may subdivide only their own slice.
- Recursion ends when subdomains become linear or deterministic.

Avoid uncontrolled agent trees. Every recursive edge must have a reason and stop condition.

## Hierarchical Decomposition

Use when one synthesis depends on several specialized domains that can each be solved independently.

- Domain leads synthesize their own evidence.
- A top-level synthesizer compares the domain conclusions and attacks cross-domain interactions.

The hierarchy should mirror information dependencies, not organization-chart aesthetics.

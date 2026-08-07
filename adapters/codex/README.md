# Codex

Dale OS keeps Codex integration deliberately thin.

The repository-root `AGENTS.md` is the always-visible operating contract. The canonical reusable modules remain `skills/**/SKILL.md`; do not duplicate them into Codex-specific prose unless the host requires a compatibility shim.

## Recommended use

1. Let root `AGENTS.md` establish the operating rules.
2. Route the task to the narrowest matching `SKILL.md`.
3. Load only the references or scripts that skill needs.
4. Execute deterministic finance tools instead of recomputing their arithmetic in prose.
5. Preserve `UNKNOWN`, `WITHHELD`, `STOP`, and `ESCALATE` outcomes when evidence does not authorize a stronger claim.

The portability test is behavioral, not cosmetic: a Codex session should reach the same invariant and falsifier as the canonical skill without creating a second authority.

# Cursor

Dale OS does not need a separate Cursor fork.

Cursor reads the repository-root `AGENTS.md`, so cloning this repo already exposes the operating contract. Keep the canonical skill bodies under `skills/**/SKILL.md`; load the narrow module needed for the task instead of translating the entire OS into Cursor rules.

## Recommended use

1. Start from the Dale OS repo root or copy the root `AGENTS.md` contract into the project you want governed.
2. Select the relevant canonical skill directory from `skills/`.
3. Preserve its falsification test and stop conditions.
4. Run deterministic tools directly when the skill points to one.
5. Return a receipt when the workflow makes consequential claims.

Do not convert every skill into always-on rules. Progressive disclosure is part of the architecture.

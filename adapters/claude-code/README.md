# Claude Code

Dale OS should not become a second `CLAUDE.md` monolith.

Claude Code can carry a small project memory file that points at the Dale OS operating contract, while the actual reusable workflows stay canonical under `skills/**/SKILL.md`.

## Recommended use

Keep the always-loaded project layer short:

```md
# Project operating contract

Read `AGENTS.md` for authority, scope, evidence, verification and stop semantics.
Use the narrowest relevant Dale OS skill under `skills/` rather than loading the full catalog.
```

Then route work to the matching skill only when needed.

Do not paste all 20 skill bodies into project memory. That destroys progressive disclosure and creates another copy that can drift.

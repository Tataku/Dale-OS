# Portable Agent Skills

The canonical `skills/**/<name>/SKILL.md` directories follow the open Agent Skills shape: a skill directory with a `SKILL.md` entrypoint and optional bundled resources.

For a skills-compatible client, run `python scripts/build_companions.py`, then install or copy the individual canonical skill directories into the location that client documents for project or user skills. Do not use the eve `agent/skills/*.md` files as the canonical source; those are generated adapter output.

The repo-level validator checks name/folder parity, required frontmatter, line budgets, falsification sections, and adapter/companion drift.

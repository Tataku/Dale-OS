# Compatibility

Dale OS treats compatibility as a truth claim, not a logo wall.

There are four different things people casually call "support":

1. **Native discovery** — the host already reads a Dale OS canonical surface such as `AGENTS.md`.
2. **Thin shim** — the host expects its own repository file, which points back to `AGENTS.md` instead of duplicating doctrine.
3. **Generated adapter** — the host needs a different filesystem shape, generated from canonical source and parity-checked.
4. **Behavioral proof** — a live model/runtime passes the Dale OS routing and adversarial evals.

Only the fourth one proves cross-model behavior.

## Current matrix

| Host | Entry point | Mode | v0.1 proof |
|---|---|---|---|
| Eve | `adapters/eve/agent/instructions.md` | generated reference adapter | generation parity + install + `eve build` |
| OpenAI Codex | `AGENTS.md` | native repository instructions | static contract |
| Cursor | `AGENTS.md` | native repository instructions | static contract |
| GitHub Copilot | `.github/copilot-instructions.md` | thin shim | static contract + shim audit |
| Gemini CLI | `GEMINI.md` | thin shim | static contract + shim audit |
| Claude Code | `adapters/claude-code/README.md` | documented project-memory shim | static contract |
| Agent-Skills-compatible hosts | `skills/` | canonical portable skills | 20-skill package validation |

Machine-readable version: `machine/compatibility.json`.

## Current official discovery contracts checked during hardening

Verified 2026-08-07; re-check before public release because host conventions can change.

- GitHub Copilot repository instructions: `.github/copilot-instructions.md`; Copilot also supports agent instructions/skills in current repository workflows.
- Gemini CLI project context: root `GEMINI.md` by default.
- Cursor: root `AGENTS.md` is a supported project rule surface.
- Claude Code: project memory uses `CLAUDE.md`; Dale OS documents a thin pointer rather than committing another full doctrine copy.
- Codex: repository `AGENTS.md` is the canonical Dale OS entry surface.

## Rule

**One source. Many hosts. No second authority.**

A host-specific file should contain only what that host needs to find Dale OS. If a compatibility layer starts restating skill logic, it has become a drift risk.

## What is still unproven

No host in the matrix is marked behaviorally equivalent yet. The cross-model routing benchmark lives in `evals/routing/trigger-cases.jsonl`; publish model claims only after reproducible runs record the model/runtime, Dale OS SHA, case-level selections, accuracy, and confusion matrix.

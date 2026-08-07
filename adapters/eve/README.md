# Dale OS for Eve

This is the framework-native Eve distribution of Dale OS.

The canonical source lives in the repository root. `agent/skills/*.md` is generated from `skills/**/SKILL.md`; do not hand-edit generated skill files.

## Run

```bash
cd adapters/eve
npm ci
npm run build:skills
npm run eval:dale
npm run dev
```

The adapter default is the literal model identifier defined in `agent/agent.ts` (`openai/gpt-5.4-mini` in this release candidate). Override it with `DALE_OS_MODEL` when running a different Eve-supported model. Provider credentials are runtime-specific and are not stored in this repository.

The read-only finance tools call the canonical Python tools in the repository root. If this adapter is moved out of the repo, set `DALE_OS_ROOT` to the Dale OS checkout and ensure Python 3 is available.

## Native surfaces

- `agent/instructions.md` — always-on Dale OS operating kernel
- `agent/skills/*.md` — generated on-demand playbooks
- `agent/tools/*.ts` — typed read-only wrappers around deterministic financial checks
- `evals/*.eval.ts` — model-level behavioral tests for flagship workflows

Financial writes are deliberately absent in v0.1.

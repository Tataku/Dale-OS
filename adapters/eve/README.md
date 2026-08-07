# Dale OS for Eve

This is the first framework-native distribution of Dale OS.

The canonical source still lives in the repository root. `agent/skills/*.md` is generated from `skills/**/SKILL.md`; do not hand-edit generated skill files.

## Run

```bash
cd adapters/eve
npm install
npm run build:skills
npm run eval:dale
npm run dev
```

Set `DALE_OS_MODEL` to choose the model. The default is a current general reasoning model supported by Eve.

The read-only finance tools call the canonical Python tools in the repository root. If this adapter is moved out of the repo, set `DALE_OS_ROOT` to the Dale OS checkout and ensure Python 3 is available.

## What is native here

- `agent/instructions.md` — the always-on Dale OS operating kernel.
- `agent/skills/*.md` — generated on-demand playbooks.
- `agent/tools/*.ts` — typed read-only wrappers around deterministic financial checks.
- `evals/*.eval.ts` — model-level behavioral tests for flagship workflows.

Financial writes are deliberately absent in v0.1.

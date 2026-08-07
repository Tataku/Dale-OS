# Install Dale OS skills

Dale OS is modular. Install the smallest skill set that solves the failure class in front of you.

## Inspect before installing

With GitHub CLI 2.90.0 or newer:

```bash
gh skill preview Tataku/Dale-OS execution-charter
```

Preview is the default trust posture. Skills can contain instructions and executable scripts; inspect the tree and `SKILL.md` before installation.

## Install one skill

```bash
gh skill install Tataku/Dale-OS execution-charter
```

Choose a host explicitly when useful:

```bash
gh skill install Tataku/Dale-OS systemic-bug-instinct --agent claude-code --scope user
gh skill install Tataku/Dale-OS truth-boundary --agent codex --scope project
```

For the fastest unambiguous lookup, install by exact path:

```bash
gh skill install Tataku/Dale-OS skills/operator/systemic-bug-instinct
```

## Install the full operating system

```bash
gh skill install Tataku/Dale-OS --all
```

Installing everything is convenient for experimentation. For production agents, prefer the smallest set that matches the workflow so activation remains legible.

## Pin consequential workflows

For reproducible agent behavior, pin a release tag or commit SHA:

```bash
gh skill install Tataku/Dale-OS systemic-bug-instinct --pin <TAG_OR_SHA>
```

Then inspect updates before accepting them:

```bash
gh skill update --dry-run
```

## Find the right module first

If you know the failure class:

```bash
python scripts/dale.py resolve symptom-patch
python scripts/dale.py resolve false-certainty --json
```

If the task spans multiple modules:

```bash
python scripts/dale.py compositions
python scripts/dale.py composition safe-bug-fix --json
```

Machine-readable routing lives in:

- `machine/failure-classes.json`
- `machine/compositions.json`
- `manifest.json`

## Canonical-source rule

Install canonical directories under `skills/`. Host adapters are distributions or integration guidance, not a second source of truth.

## Maintainer validation

Before a public skill release, validate both Dale OS invariants and the host ecosystem contract:

```bash
python scripts/dale.py doctor
gh skill publish --dry-run
```

`gh skill` is currently a GitHub CLI preview feature, so treat its exact UX as versioned external behavior rather than a Dale OS invariant.

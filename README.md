# Dale OS

**An agentic operating system for high-integrity software and finance.**

I did not start this as a framework. I kept running into the same expensive failure modes while building real software: agents fixing symptoms instead of mechanisms, reopening decisions I had already made, wandering outside scope, calling a PR "shipped," or producing a financially clean-looking number from dirty underlying records.

So I started turning the lessons into rules.

Dale OS is the result.

**If you are an agent:** read [`AGENTS.md`](AGENTS.md), then `manifest.json`. Do not load the whole repo.

**If you are skeptical:** good. Open [`CHALLENGE.md`](CHALLENGE.md) and try to break it.

The basic idea is simple:

- **Authority before autonomy.**
- **Real fixes to real problems.**
- **Null is not failure. False certainty is.**
- **Get the money right.**

This repository is the canonical source. Skills are modules inside the operating system. Deterministic tools handle math and reconciliation where reasoning alone is not good enough. Evals try to break the rules before real work does.

## Two systems, one philosophy

### Operator OS

For coding agents and agentic software work:

- `execution-charter` — give the agent a fence before a shovel.
- `systemic-bug-instinct` — assume a bug may be systemic until the blast-radius audit says otherwise.
- `truth-boundary` — separate known, derived, estimated, inferred and unknown.
- `latest-authority` — carry the latest human decision forward; do not re-ask it without new conflicting evidence.
- `diff-scope-audit` — every hunk owes the charter an explanation.
- `protected-boundary` — stopping is a valid successful action.
- `intent-drift-check` — busy is not the same as aligned.
- `operator-ui-audit` — a wrong value in the UI is usually a data problem wearing a costume.

### Financial Truth

For money, ledgers, portfolio analytics and financial models:

- `money-trail` — every dollar gets a passport.
- `accounting-integrity` — well-formed data can still lie.
- `performance-truth` — funding is not performance.
- `basis-proof` — no basis, no profit.
- `ledger-repair` — preview the economics before changing the books.
- `transfer-neutrality` — money does not teleport.
- `cash-truth` — missing cash is not zero cash.
- `financial-evidence-grade` — an estimate is not an authority.
- `tax-character-proof` — observed cash and tax character are different facts.
- `corporate-action-continuity` — identity can change without changing economics.
- `model-sanity` — a plausible model is not automatically a valid model.
- `close-the-books` — do not publish analytics whose required books are not ready.

## How the repo is built

```text
Dale-OS/
├── PRINCIPLES.md
├── ARCHITECTURE.md
├── skills/
│   ├── operator/
│   └── financial-truth/
├── tools/                  # deterministic, read-only financial checks
├── evals/                  # adversarial cases and rubrics
├── cases/                  # sanitized incidents that paid for a rule
├── adapters/
│   ├── eve/                # eve-native agent distribution
│   └── agent-skills/       # portable Agent Skills notes
├── scripts/                # validation + adapter builders
├── docs/
└── second-brain/           # clean ingestion packet, not the private brain itself
```

## Source rule

**One source. Many adapters.**

The canonical skill lives in `skills/**/SKILL.md`. Platform adapters are generated from that source. Never hand-maintain a second copy of a rule just because a different agent framework wants a different filesystem shape.

## Financial safety rule

Dale OS does not let an LLM become the accounting authority just because it can write a convincing explanation.

When evidence cannot establish the answer, the correct output may be:

```text
WITHHELD
Reason: evidence insufficient
```

That is not the system failing. That is the system working.

## Five-minute proof

```bash
python scripts/dale.py catalog
python scripts/dale.py challenge
python scripts/dale.py doctor
```

The repo also ships a machine-readable receipt contract in `RECEIPTS.md` + `schemas/receipt.schema.json`, so agent handoffs can preserve claims, unknowns, mutations and verification instead of forwarding confidence without evidence.

## Status

Private hardening build. See `ROADMAP.md` and `docs/RELEASE_READINESS.md`.

## Origin

Designed and curated by Dale Powell from real human-agent operating experience while building ACF Dashboard and related systems. The public package is intentionally generalized: ACF-specific scoring logic, personal financial data and proprietary product internals do not belong here.

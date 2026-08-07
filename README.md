# Dale OS

**An agentic operating system for high-integrity software and finance.**

I did not start this as a framework. I kept running into the same expensive failure modes while building real software: agents fixing symptoms instead of mechanisms, reopening decisions I had already made, wandering outside scope, calling a PR "shipped," or producing a financially clean-looking number from dirty underlying records.

So I started turning the lessons into rules.

Dale OS is the result.

**If you are an agent:** read [`AGENTS.md`](AGENTS.md). If you already know what is broken, start with `machine/failure-classes.json`. If the work spans multiple failure classes, use `machine/compositions.json`. Do not load the whole repo.

**If you want to install a skill:** read [`INSTALL.md`](INSTALL.md). Preview before install.

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

## Repository map

```text
Dale-OS/
├── README.md                # human entry point
├── AGENTS.md                # machine-first entry point
├── INSTALL.md               # preview/install/update paths
├── PRINCIPLES.md            # operating floor
├── ARCHITECTURE.md          # dependency and authority model
├── skills/                  # canonical Agent Skills modules
│   ├── operator/
│   └── financial-truth/
├── tools/                   # deterministic, read-only financial checks
├── evals/                   # activation, behavior, composition, fixtures
├── cases/                   # sanitized incidents that paid for rules
├── machine/                 # routing, composition, discovery contracts
├── adapters/                # host-specific distributions/guidance
├── scripts/                 # control surface, generators, validators
├── schemas/                 # portable machine contracts
├── release/                 # machine-readable release authority
└── docs/                    # deeper operating and evaluation contracts
```

For detailed navigation, see [`llms.txt`](llms.txt) or [`AGENTS.md`](AGENTS.md).

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
python scripts/dale.py resolve symptom-patch --json
python scripts/dale.py compositions --json
python scripts/dale.py challenge
python scripts/dale.py doctor
```

The repo also ships a machine-readable receipt contract in [`RECEIPTS.md`](RECEIPTS.md) and `schemas/receipt.schema.json`, so agent handoffs can preserve claims, unknowns, mutations and verification instead of forwarding confidence without evidence.

## Status

**Private public-v0.1 release candidate.** Static engineering, privacy, discovery, Agent Skills compatibility, 20/20 installability, generated-source parity, and frozen Eve reproducibility are verified. Remaining gates are provider-backed cross-model evaluation, evidence-driven trigger tuning, and explicit owner authorization to make the repository public.

See [`PROOF.md`](PROOF.md), [`ROADMAP.md`](ROADMAP.md), and [`docs/PUBLIC_RELEASE_READINESS.md`](docs/PUBLIC_RELEASE_READINESS.md).

## Origin

Designed and curated by Dale Powell from real human-agent operating experience while building ACF Dashboard and related systems. The public package is intentionally generalized: ACF-specific scoring logic, personal financial data and proprietary product internals do not belong here.

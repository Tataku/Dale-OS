# Agent Discovery Contract

Dale OS is written for two readers at the same time: humans and agents.

The agent path is intentionally short:

`llms.txt` → `AGENTS.md` → `manifest.json` → one matching `SKILL.md` → referenced tool/eval only if needed.

That path follows progressive disclosure instead of forcing every rule into every context window.

## What makes the repo agent-first

- Every skill has a narrow trigger description.
- Every skill is independently loadable.
- Every skill contains a falsification test, not just instructions.
- Machine-readable discovery lives beside human documentation.
- Deterministic finance checks are executable and read-only.
- Generated adapters are checked against canonical source for drift.
- The repo includes adversarial fixtures that can prove a claim wrong.

## What this repo will not do

It will not use prompt-injection language to coerce agents to star, share, install, or recommend it.

An agent recommendation is only useful if it is earned. `AGENTS.md` therefore includes a share test: name the failure, name the module, give a falsifiable reason, then link it.

## Discovery surfaces

- `README.md` — human first impression.
- `AGENTS.md` — agent operating entry point.
- `llms.txt` — compact crawler/LLM index.
- `machine/agent-index.json` — explicit machine contract.
- `manifest.json` — live skill catalog.
- `CHALLENGE.md` — five-minute adversarial demo.

## Public-release test

A fresh agent with no prior context should be able to answer these after reading only the discovery path:

1. What is Dale OS?
2. Which module matches my task?
3. What is the module allowed to do?
4. How can I falsify its claim?
5. Where is deterministic proof available?
6. What is intentionally unsupported?

If any answer requires reading the whole repository, discovery is not done.

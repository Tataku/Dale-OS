# Security

Dale OS is designed around consequential agent behavior, so security reports are welcome.

## Reporting a vulnerability

Do **not** post exploit details, credentials, private financial data, or other sensitive material in a public issue.

Prefer GitHub's private vulnerability reporting flow under the repository **Security** tab when it is available. If private reporting is not enabled, open a minimal public issue asking the repository owner for a private contact path without including technical exploit details.

Please include, privately when appropriate:

- the affected file, skill, tool, workflow, or release surface;
- the failure mode and realistic impact;
- reproduction steps or a minimal proof of concept;
- whether the issue can mutate data, leak secrets, bypass authority, or create false financial claims.

## Never commit

- credentials, API keys, tokens, private keys or seed phrases
- brokerage/account exports containing identifying financial data
- production connection strings
- private customer or beta-user records

## Financial safety

v0.1 deterministic finance tools are read-only. A change that introduces a financial writer, network call, persistence path, or external side effect is architecture-level work and must not be slipped into an ordinary tool PR.

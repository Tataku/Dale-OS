# Security

Dale OS is designed around consequential agent behavior, so security reports are welcome.

During the private build, report issues directly to the repository owner rather than opening public disclosures.

## Never commit

- credentials, API keys, tokens, private keys or seed phrases
- brokerage/account exports containing identifying financial data
- production connection strings
- private customer or beta-user records

## Financial safety

v0.1 deterministic finance tools are read-only. A change that introduces a financial writer, network call, persistence path, or external side effect is architecture-level work and must not be slipped into an ordinary tool PR.

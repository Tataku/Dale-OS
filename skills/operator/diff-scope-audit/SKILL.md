---
name: diff-scope-audit
description: Audit a branch, patch, or pull request against its stated task. Use before review or merge to verify the true merge base, map every changed file/hunk to scope, find hidden unrelated work, check protected boundaries and lockstep artifacts, classify test deltas, and keep PR claims honest.
---

# Diff Scope Audit

## Rule

**Every hunk owes the charter an explanation.**

## Workflow

1. Establish the true comparison base; do not audit from a stale or directionally wrong diff.
2. List every changed file and map it to scope-in, declared expansion, incidental fix, or unexplained.
3. Treat unexplained changes as blocking until removed or justified.
4. Scan the full file list for protected boundaries, guards, generated artifacts, schema changes, migrations, and co-owned lockstep files.
5. Run targeted verification and compare new failures against the correct baseline instead of calling every red "flaky."
6. Check PR/report language against actual state: implemented, pushed, open, merged, deployed are different.

## Falsify it

Try to justify every changed hunk from the charter. One unexplained hunk is enough to fail a clean verdict.

## Stop conditions

- Any unexplained hunk remains.
- A protected boundary was touched without required authority.
- Verification claims cannot be reproduced.

A stop is an output, not an excuse. State what evidence or authority would unblock the work.

## Output

VERDICT · BASE · SCOPE TRACE · PROTECTED HITS · LOCKSTEP · TEST DELTA · CLAIM CHECK · BLOCKERS.

Keep the report short enough to act on. Preserve hard facts, unknowns, and blockers.

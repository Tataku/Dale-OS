## Objective

What exact outcome should this PR produce?

## Scope

**IN**
- 

**OUT**
- 

## Failure / mechanism

What failure class, user need, or measured portability gap pays for this change? Name the root mechanism rather than only the visible symptom.

## Authority / boundaries

Does this cross any protected, financial, persistence, credential, release, generated-source, or external-communication boundary? If yes, name the authority that permits it.

## Verification

- [ ] `python scripts/verify.py`
- [ ] `python scripts/verify.py --with-eve` when the Eve adapter or its generated surface is affected
- [ ] Targeted reproducer/eval fails without the fix and passes with it, when applicable
- [ ] Generated artifacts are current

Evidence / commands:

```text
<results>
```

## Public claims / release evidence

- [ ] No public capability or evidence claim changed
- [ ] Or: version/changelog/proof surfaces were updated in this PR

Historical release evidence is immutable. Do not rewrite an old benchmark to describe a newer tree.

## Safety

- [ ] No credentials, private financial data, or proprietary ACF internals are included.
- [ ] Financial mutation remains disabled unless this PR is explicitly architecture-level work.
- [ ] No guard was weakened merely to make the change pass.

## Final state

What is actually true now: implemented, verified, PR-only, merged, released, or still blocked?

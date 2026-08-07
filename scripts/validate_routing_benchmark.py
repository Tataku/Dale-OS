#!/usr/bin/env python3
"""Validate the cross-model skill-routing benchmark without pretending to run a model."""
from collections import Counter
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / 'manifest.json').read_text(encoding='utf-8'))
known = {row['name'] for row in manifest.get('skills', [])}
path = ROOT / 'evals' / 'routing' / 'trigger-cases.jsonl'
errors = []
ids = set()
counts = Counter()
rows = 0

for line_no, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
    if not line.strip():
        continue
    rows += 1
    try:
        case = json.loads(line)
    except Exception as exc:
        errors.append(f'line {line_no}: invalid JSON: {exc}')
        continue
    cid = case.get('id')
    expected = case.get('expected_skill')
    confusable = case.get('confusable_with')
    prompt = case.get('prompt')
    if not cid or cid in ids:
        errors.append(f'line {line_no}: missing/duplicate id {cid!r}')
    ids.add(cid)
    if expected not in known:
        errors.append(f'line {line_no}: unknown expected_skill {expected!r}')
    else:
        counts[expected] += 1
    if confusable not in known or confusable == expected:
        errors.append(f'line {line_no}: invalid confusable_with {confusable!r}')
    if not isinstance(prompt, str) or len(prompt) < 80:
        errors.append(f'line {line_no}: prompt too weak for routing evaluation')

for skill in sorted(known):
    if counts[skill] < 2:
        errors.append(f'{skill}: needs at least 2 routing cases; found {counts[skill]}')

if rows < len(known) * 2:
    errors.append(f'benchmark too small: {rows} cases for {len(known)} skills')

if errors:
    print('ROUTING BENCHMARK INVALID')
    for error in errors:
        print('-', error)
    raise SystemExit(1)

print(f'ROUTING BENCHMARK STRUCTURE PASS: {rows} adversarial cases, {len(known)} skills, >=2 cases per skill; model scores intentionally absent')

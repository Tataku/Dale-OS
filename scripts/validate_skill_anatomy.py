#!/usr/bin/env python3
"""Keep every canonical skill small, falsifiable, and structurally complete."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
errors = []
required = ['## Rule', '## Workflow', '## Falsify it', '## Stop conditions', '## Output']
count = 0

for path in sorted((ROOT / 'skills').glob('*/*/SKILL.md')):
    count += 1
    text = path.read_text(encoding='utf-8')
    rel = path.relative_to(ROOT)
    lines = text.splitlines()
    if not 25 <= len(lines) <= 80:
        errors.append(f'{rel}: expected 25-80 lines, found {len(lines)}')
    positions = []
    for heading in required:
        pos = text.find(heading)
        if pos < 0:
            errors.append(f'{rel}: missing {heading}')
        positions.append(pos)
    if all(pos >= 0 for pos in positions) and positions != sorted(positions):
        errors.append(f'{rel}: required sections are out of order')

    workflow_start = text.find('## Workflow')
    workflow_end = text.find('## ', workflow_start + len('## Workflow')) if workflow_start >= 0 else -1
    workflow = text[workflow_start:workflow_end if workflow_end >= 0 else None]
    steps = re.findall(r'^\d+\.\s+', workflow, flags=re.M)
    if not 4 <= len(steps) <= 8:
        errors.append(f'{rel}: workflow should have 4-8 numbered steps, found {len(steps)}')

    falsify_start = text.find('## Falsify it')
    stop_start = text.find('## Stop conditions')
    if falsify_start >= 0 and stop_start > falsify_start:
        falsifier = text[falsify_start:stop_start]
        if len(falsifier.strip()) < 100:
            errors.append(f'{rel}: falsifier is too weak/short')

    if re.search(r'\b(?:ACF|CIS)\b|Adaptive Convexity', text, flags=re.I):
        errors.append(f'{rel}: canonical public skill leaked product-specific ACF doctrine')

if count != 20:
    errors.append(f'expected 20 canonical skills, found {count}')

if errors:
    print('SKILL ANATOMY FAILED')
    for error in errors:
        print('-', error)
    raise SystemExit(1)

print(f'SKILL ANATOMY PASS: {count} compact skills; rule/workflow/falsifier/stop/output contract preserved')

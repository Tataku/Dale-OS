#!/usr/bin/env python3
"""Fail when Dale OS becomes hard for an agent to discover without loading the repo."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
errors = []

def fail(message):
    errors.append(message)

manifest = json.loads((ROOT / 'manifest.json').read_text(encoding='utf-8'))
index = json.loads((ROOT / 'machine' / 'agent-index.json').read_text(encoding='utf-8'))
registry = json.loads((ROOT / 'machine' / 'failure-classes.json').read_text(encoding='utf-8'))

required_entrypoints = {
    'human': 'README.md',
    'agent': 'AGENTS.md',
    'llm_index': 'llms.txt',
    'skill_catalog': 'manifest.json',
    'failure_registry': 'machine/failure-classes.json',
    'challenge': 'CHALLENGE.md',
}
for key, path in required_entrypoints.items():
    if index.get('discovery', {}).get(key) != path:
        fail(f'agent-index discovery mismatch for {key}: expected {path}')
    if not (ROOT / path).exists():
        fail(f'missing discovery entrypoint: {path}')

skills = {row['name'] for row in manifest.get('skills', [])}
routes = {row.get('route') for row in registry.get('classes', [])}
if skills != routes:
    fail(f'failure-first routing drift: missing={sorted(skills-routes)} extra={sorted(routes-skills)}')

# Always-loaded host shims must stay tiny and point back to the canonical contract.
shims = {
    'GEMINI.md': 40,
    '.github/copilot-instructions.md': 40,
}
for path, max_lines in shims.items():
    p = ROOT / path
    if not p.exists():
        fail(f'missing host discovery shim: {path}')
        continue
    text = p.read_text(encoding='utf-8')
    if len(text.splitlines()) > max_lines:
        fail(f'{path} exceeds {max_lines} lines; keep always-loaded shims thin')
    if 'AGENTS.md' not in text:
        fail(f'{path} must route to AGENTS.md')

agents = (ROOT / 'AGENTS.md').read_text(encoding='utf-8')
if len(agents.splitlines()) > 120:
    fail('AGENTS.md exceeds 120 lines; progressive disclosure is degrading')
for required in ('manifest.json', 'machine/failure-classes.json', 'CHALLENGE.md'):
    if required not in agents:
        fail(f'AGENTS.md must expose {required}')

if errors:
    print('DISCOVERY AUDIT FAILED')
    for error in errors:
        print('-', error)
    raise SystemExit(1)

print(f'DISCOVERY AUDIT PASS: {len(skills)} skills reachable from failure classes; host shims remain thin')

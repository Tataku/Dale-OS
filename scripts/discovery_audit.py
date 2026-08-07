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
routing = json.loads((ROOT / 'machine' / 'routing-policy.json').read_text(encoding='utf-8'))
compatibility = json.loads((ROOT / 'machine' / 'compatibility.json').read_text(encoding='utf-8'))

required_entrypoints = {
    'human': 'README.md',
    'agent': 'AGENTS.md',
    'llm_index': 'llms.txt',
    'skill_catalog': 'manifest.json',
    'failure_registry': 'machine/failure-classes.json',
    'routing_policy': 'machine/routing-policy.json',
    'compatibility': 'machine/compatibility.json',
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

precedence = routing.get('precedence', [])
if not isinstance(precedence, list) or not precedence:
    fail('routing policy must contain precedence rules')
else:
    for i, row in enumerate(precedence, 1):
        prefer = row.get('prefer')
        over = row.get('over')
        when = row.get('when')
        if prefer not in skills or over not in skills or prefer == over:
            fail(f'routing precedence #{i} references invalid skill pair: {prefer!r} over {over!r}')
        if not isinstance(when, str) or len(when) < 30:
            fail(f'routing precedence #{i} has a weak condition')
if not routing.get('falsifier'):
    fail('routing policy must state its falsifier')

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
for required in ('manifest.json', 'machine/failure-classes.json', 'machine/routing-policy.json', 'CHALLENGE.md'):
    if required not in agents:
        fail(f'AGENTS.md must expose {required}')

hosts = compatibility.get('hosts', [])
if not isinstance(hosts, list) or not hosts:
    fail('compatibility matrix must contain hosts')
else:
    seen = set()
    for row in hosts:
        host = row.get('host')
        entrypoint = row.get('entrypoint')
        if not host or host in seen:
            fail(f'compatibility matrix missing/duplicate host: {host!r}')
        seen.add(host)
        if not entrypoint or not (ROOT / entrypoint).exists():
            fail(f'compatibility entrypoint missing for {host!r}: {entrypoint!r}')
        if row.get('behavioral_model_eval') is not False:
            fail(f'{host!r}: do not claim behavioral model proof until model-in-loop evals are recorded')

if errors:
    print('DISCOVERY AUDIT FAILED')
    for error in errors:
        print('-', error)
    raise SystemExit(1)

print(f'DISCOVERY AUDIT PASS: {len(skills)} skills reachable from failure classes; {len(precedence)} collision rules explicit; {len(hosts)} host contracts explicit; shims remain thin')

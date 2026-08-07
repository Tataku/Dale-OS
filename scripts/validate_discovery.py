#!/usr/bin/env python3
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
errors=[]
def fail(x): errors.append(x)
manifest=json.loads((ROOT/'manifest.json').read_text())
index=json.loads((ROOT/'machine'/'agent-index.json').read_text())
registry=json.loads((ROOT/'machine'/'failure-classes.json').read_text())
manifest_skills={x['name'] for x in manifest.get('skills',[])}
fs_skills={p.parent.name for p in (ROOT/'skills').glob('*/*/SKILL.md')}
routes={x.get('route') for x in registry.get('classes',[])}
if manifest_skills!=fs_skills: fail(f'manifest/filesystem skill drift: {sorted(manifest_skills^fs_skills)}')
if routes!=fs_skills: fail(f'failure routing discovery drift: {sorted(routes^fs_skills)}')
if set(manifest.get('adapters',[]))!=set(index.get('adapters',[])): fail('manifest/agent-index adapter drift')
for path,needles in {
    'README.md':['AGENTS.md','CHALLENGE.md','machine/failure-classes.json'],
    'AGENTS.md':['manifest.json','machine/failure-classes.json','CHALLENGE.md'],
    'llms.txt':['AGENTS.md','manifest.json','machine/failure-classes.json']
}.items():
    text=(ROOT/path).read_text(encoding='utf-8')
    for needle in needles:
        if needle not in text: fail(f'{path}: missing discovery pointer {needle}')
descriptions=[x.get('description','').strip().casefold() for x in manifest.get('skills',[])]
if len(descriptions)!=len(set(descriptions)): fail('duplicate skill descriptions found')
if any(len(x)<60 for x in descriptions): fail('weak skill description in manifest')
if errors:
    print('DISCOVERY VALIDATION FAILED')
    for e in errors: print('-',e)
    raise SystemExit(1)
print(f'DISCOVERY PASS: {len(fs_skills)} skills, failure-first routing, adapter parity, human/agent entrypoints aligned')

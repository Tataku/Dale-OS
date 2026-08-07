#!/usr/bin/env python3
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
errors=[]
def fail(x): errors.append(x)
manifest=json.loads((ROOT/'manifest.json').read_text())
index=json.loads((ROOT/'machine'/'agent-index.json').read_text())
registry=json.loads((ROOT/'machine'/'failure-classes.json').read_text())
compositions=json.loads((ROOT/'machine'/'compositions.json').read_text())
manifest_skills={x['name'] for x in manifest.get('skills',[])}
fs_skills={p.parent.name for p in (ROOT/'skills').glob('*/*/SKILL.md')}
routes={x.get('route') for x in registry.get('classes',[])}
if manifest_skills!=fs_skills: fail(f'manifest/filesystem skill drift: {sorted(manifest_skills^fs_skills)}')
if routes!=fs_skills: fail(f'failure routing discovery drift: {sorted(routes^fs_skills)}')
if set(manifest.get('adapters',[]))!=set(index.get('adapters',[])): fail('manifest/agent-index adapter drift')
if index.get('discovery',{}).get('compositions')!='machine/compositions.json': fail('agent-index must expose compositions')
if index.get('discovery',{}).get('install')!='INSTALL.md': fail('agent-index must expose install guide')
composition_ids=set()
for item in compositions.get('compositions',[]):
    cid=item.get('id')
    if not cid or cid in composition_ids: fail(f'composition missing/duplicate id: {cid!r}')
    composition_ids.add(cid)
    seq=item.get('sequence',[])
    if len(seq)<2: fail(f'composition {cid!r} must contain at least two skills')
    seen=set()
    for step in seq:
        skill=step.get('skill')
        if skill not in fs_skills: fail(f'composition {cid!r} references unknown skill {skill!r}')
        if skill in seen: fail(f'composition {cid!r} repeats skill {skill!r}')
        seen.add(skill)
    if not item.get('handoff_contract') or not item.get('falsify'): fail(f'composition {cid!r} missing handoff/falsifier')
for path,needles in {
    'README.md':['AGENTS.md','INSTALL.md','CHALLENGE.md','machine/failure-classes.json','machine/compositions.json','docs/PUBLIC_RELEASE_READINESS.md'],
    'AGENTS.md':['manifest.json','INSTALL.md','machine/failure-classes.json','machine/compositions.json','CHALLENGE.md'],
    'llms.txt':['AGENTS.md','INSTALL.md','manifest.json','machine/failure-classes.json','machine/compositions.json']
}.items():
    text=(ROOT/path).read_text(encoding='utf-8')
    for needle in needles:
        if needle not in text: fail(f'{path}: missing discovery pointer {needle}')
for stale in ('second-brain/','docs/RELEASE_READINESS.md','LICENSE_PENDING.md'):
    for path in ('README.md','AGENTS.md','llms.txt','ARCHITECTURE.md'):
        if stale in (ROOT/path).read_text(encoding='utf-8'): fail(f'{path}: stale release pointer {stale}')
descriptions=[x.get('description','').strip().casefold() for x in manifest.get('skills',[])]
if len(descriptions)!=len(set(descriptions)): fail('duplicate skill descriptions found')
if any(len(x)<60 for x in descriptions): fail('weak skill description in manifest')
if errors:
    print('DISCOVERY VALIDATION FAILED')
    for e in errors: print('-',e)
    raise SystemExit(1)
print(f'DISCOVERY PASS: {len(fs_skills)} skills, {len(composition_ids)} compositions, failure-first routing, adapter parity, entrypoints aligned')

#!/usr/bin/env python3
from pathlib import Path
import json, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
DALE=ROOT/'scripts'/'dale.py'
errors=[]

def run(*args):
    return subprocess.run([sys.executable,str(DALE),*args],cwd=ROOT,capture_output=True,text=True)

def expect_json(args, checks):
    r=run(*args)
    if r.returncode:
        errors.append(f"{' '.join(args)} failed: {r.stderr.strip()}")
        return
    try: data=json.loads(r.stdout)
    except Exception as exc:
        errors.append(f"{' '.join(args)} returned invalid JSON: {exc}")
        return
    for label,predicate in checks:
        if not predicate(data): errors.append(f"{' '.join(args)} failed check: {label}")

expect_json(('resolve','symptom-patch','--json'),[
    ('route systemic-bug-instinct',lambda d:d.get('skill')=='systemic-bug-instinct'),
    ('canonical skill path',lambda d:d.get('path')=='skills/operator/systemic-bug-instinct/SKILL.md'),
    ('rule exposed',lambda d:bool(d.get('rule'))),
    ('falsifier exposed',lambda d:bool(d.get('falsify'))),
])
expect_json(('composition','safe-bug-fix','--json'),[
    ('composition id',lambda d:d.get('id')=='safe-bug-fix'),
    ('multi-skill sequence',lambda d:len(d.get('sequence',[]))>=2),
    ('handoff exposed',lambda d:bool(d.get('handoff_contract'))),
])
expect_json(('catalog','--json'),[
    ('20 skills',lambda d:len(d.get('skills',[]))==20),
])
for args in [('resolve','does-not-exist','--json'),('composition','does-not-exist','--json')]:
    r=run(*args)
    if r.returncode!=2: errors.append(f"{' '.join(args)} must exit 2 for unknown identifier; got {r.returncode}")
if errors:
    print('AGENT SURFACE SMOKE FAILED')
    for e in errors: print('-',e)
    raise SystemExit(1)
print('AGENT SURFACE PASS: resolver, composition, catalog JSON, and unknown-id exit semantics')

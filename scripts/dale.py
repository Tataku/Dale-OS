#!/usr/bin/env python3
"""Tiny zero-dependency Dale OS control surface for agents."""
from pathlib import Path
import argparse, json, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]

def load(path):
    return json.loads((ROOT/path).read_text(encoding='utf-8'))

def emit(data, as_json=False):
    if as_json:
        print(json.dumps(data, indent=2)); return
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                print(f"{key}: {json.dumps(value, ensure_ascii=False)}")
            else:
                print(f"{key}: {value}")
    else:
        print(data)

def catalog(args):
    manifest=load('manifest.json')
    if args.json:
        emit(manifest, True); return
    for s in manifest['skills']:
        companion=' +tool' if s.get('deterministic_companion') else ''
        print(f"{s['family']:16} {s['name']}{companion}\n  {s['description']}")

def resolve(args):
    manifest=load('manifest.json')
    registry=load('machine/failure-classes.json')
    by_skill={s['name']:s for s in manifest['skills']}
    match=next((row for row in registry['classes'] if row['id']==args.failure),None)
    if not match:
        print(f"unknown failure class: {args.failure}",file=sys.stderr)
        raise SystemExit(2)
    skill=by_skill[match['route']]
    result={'failure_class':match['id'],'symptom':match['symptom'],'skill':skill['name'],'path':skill['path'],'rule':skill['rule'],'falsify':skill['falsify'],'deterministic_companion':skill['deterministic_companion']}
    emit(result,args.json)

def compositions(args):
    data=load('machine/compositions.json')
    if args.json:
        emit(data,True); return
    for item in data['compositions']:
        chain=' -> '.join(step['skill'] for step in item['sequence'])
        print(f"{item['id']}\n  {item['use_when']}\n  {chain}")

def composition(args):
    data=load('machine/compositions.json')
    match=next((row for row in data['compositions'] if row['id']==args.composition),None)
    if not match:
        print(f"unknown composition: {args.composition}",file=sys.stderr)
        raise SystemExit(2)
    emit(match,args.json)

def doctor(_args):
    subprocess.run([sys.executable,str(ROOT/'scripts'/'validate_repo.py')],check=True)

def challenge(_args):
    subprocess.run([sys.executable,str(ROOT/'scripts'/'run_evals.py')],check=True)

def receipt(args):
    data=json.loads(Path(args.path).read_text())
    required={'schema','skill','status','summary','claims','unknowns','mutations','verification'}
    missing=sorted(required-set(data))
    valid_status={'PASS','DEGRADED','UNRESOLVED','WITHHELD','BLOCKED'}
    errors=[]
    if missing: errors.append('missing: '+', '.join(missing))
    if data.get('schema')!='dale-os/receipt/v1': errors.append('schema must be dale-os/receipt/v1')
    if data.get('status') not in valid_status: errors.append('invalid status')
    known={s['name'] for s in load('manifest.json')['skills']}
    if data.get('skill') not in known: errors.append('unknown skill')
    if errors:
        print('RECEIPT INVALID')
        for e in errors: print('-',e)
        raise SystemExit(1)
    print('RECEIPT PASS')

def main():
    p=argparse.ArgumentParser(prog='dale',description='Dale OS agent control surface')
    sub=p.add_subparsers(dest='cmd',required=True)
    c=sub.add_parser('catalog'); c.add_argument('--json',action='store_true'); c.set_defaults(func=catalog)
    rs=sub.add_parser('resolve'); rs.add_argument('failure'); rs.add_argument('--json',action='store_true'); rs.set_defaults(func=resolve)
    cs=sub.add_parser('compositions'); cs.add_argument('--json',action='store_true'); cs.set_defaults(func=compositions)
    cp=sub.add_parser('composition'); cp.add_argument('composition'); cp.add_argument('--json',action='store_true'); cp.set_defaults(func=composition)
    d=sub.add_parser('doctor'); d.set_defaults(func=doctor)
    ch=sub.add_parser('challenge'); ch.set_defaults(func=challenge)
    r=sub.add_parser('receipt'); r.add_argument('path'); r.set_defaults(func=receipt)
    args=p.parse_args(); args.func(args)
if __name__=='__main__': main()

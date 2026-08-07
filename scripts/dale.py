#!/usr/bin/env python3
"""Tiny zero-dependency Dale OS control surface for agents."""
from pathlib import Path
import argparse, json, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]

def catalog(args):
    manifest=json.loads((ROOT/'manifest.json').read_text())
    if args.json:
        print(json.dumps(manifest,indent=2)); return
    for s in manifest['skills']:
        companion=' +tool' if s.get('deterministic_companion') else ''
        print(f"{s['family']:16} {s['name']}{companion}\n  {s['description']}")

def run_script(name):
    subprocess.run([sys.executable,str(ROOT/'scripts'/name)],check=True)

def doctor(_args):
    run_script('validate_repo.py')

def challenge(_args):
    run_script('run_evals.py')

def release(_args):
    run_script('validate_repo.py')
    run_script('validate_skill_anatomy.py')
    run_script('validate_routing_benchmark.py')
    run_script('discovery_audit.py')
    run_script('public_boundary_audit.py')
    print('RELEASE PREFLIGHT PASS: mechanical gates green; owner/external release gates may still remain')

def receipt(args):
    data=json.loads(Path(args.path).read_text())
    required={'schema','skill','status','summary','claims','unknowns','mutations','verification'}
    missing=sorted(required-set(data))
    valid_status={'PASS','DEGRADED','UNRESOLVED','WITHHELD','BLOCKED'}
    errors=[]
    if missing: errors.append('missing: '+', '.join(missing))
    if data.get('schema')!='dale-os/receipt/v1': errors.append('schema must be dale-os/receipt/v1')
    if data.get('status') not in valid_status: errors.append('invalid status')
    known={s['name'] for s in json.loads((ROOT/'manifest.json').read_text())['skills']}
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
    d=sub.add_parser('doctor'); d.set_defaults(func=doctor)
    ch=sub.add_parser('challenge'); ch.set_defaults(func=challenge)
    rel=sub.add_parser('release'); rel.set_defaults(func=release)
    r=sub.add_parser('receipt'); r.add_argument('path'); r.set_defaults(func=receipt)
    args=p.parse_args(); args.func(args)
if __name__=='__main__': main()

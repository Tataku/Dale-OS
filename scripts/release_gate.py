#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
VALID={'PASS','PENDING','BLOCKED_EXTERNAL','OWNER_REQUIRED','FAIL'}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--file',default='release/gates.json')
    ap.add_argument('--validate-only',action='store_true')
    args=ap.parse_args()
    p=Path(args.file); doc=json.loads(p.read_text(encoding='utf-8'))
    if doc.get('schema')!='dale-os/release-gates/v1': raise SystemExit('invalid release-gate schema')
    ids=set(); bad=[]
    for gate in doc.get('gates',[]):
        gid=gate.get('id'); status=gate.get('status')
        if not gid or gid in ids: bad.append(f'missing/duplicate gate id: {gid!r}')
        ids.add(gid)
        if status not in VALID: bad.append(f'{gid}: invalid status {status!r}')
        if status=='PASS' and not gate.get('evidence'): bad.append(f'{gid}: PASS requires evidence')
    if bad:
        print('RELEASE GATE INVALID')
        for x in bad: print('-',x)
        raise SystemExit(1)
    blocked=[g for g in doc['gates'] if g['status']!='PASS']
    out={'schema':'dale-os/release-verdict/v1','target':doc.get('target'),'ready':not blocked,'blocked':[{'id':g['id'],'status':g['status']} for g in blocked]}
    print(json.dumps(out,indent=2))
    if not args.validate_only and blocked: raise SystemExit(2)

if __name__=='__main__': main()

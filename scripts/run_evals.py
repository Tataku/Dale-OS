#!/usr/bin/env python3
from pathlib import Path
import json, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
FIX=ROOT/'evals'/'fixtures'

def run_case(path):
    case=json.loads(path.read_text())
    proc=subprocess.run([sys.executable,str(ROOT/'tools'/case['tool'])],input=json.dumps(case['input']),text=True,capture_output=True)
    if proc.returncode!=0:
        return False,f"tool exited {proc.returncode}: {proc.stderr.strip()}"
    out=json.loads(proc.stdout); exp=case['expect']
    problems=[]
    if out.get('status')!=exp.get('status'): problems.append(f"status {out.get('status')} != {exp.get('status')}")
    if 'contains_blockers' in exp:
        missing=[x for x in exp['contains_blockers'] if x not in out.get('blockers',[])]
        if missing: problems.append(f"missing blockers {missing}")
    if 'contains_failures' in exp:
        missing=[x for x in exp['contains_failures'] if x not in out.get('failures',[])]
        if missing: problems.append(f"missing failures {missing}")
    if 'disposal_status' in exp:
        got=out.get('disposals',[{}])[0].get('status')
        if got!=exp['disposal_status']: problems.append(f"disposal status {got}")
    if exp.get('realized_gain_is_null'):
        if out.get('disposals',[{}])[0].get('realized_gain') is not None: problems.append('realized gain should be null')
    if 'realized_gain' in exp:
        if out.get('disposals',[{}])[0].get('realized_gain')!=exp['realized_gain']: problems.append('realized gain mismatch')
    if 'external_flow_total' in exp and out.get('external_flow_total')!=exp['external_flow_total']: problems.append('external flow total mismatch')
    if 'pair_status' in exp:
        got=out.get('transfer_pairs',[{}])[0].get('status')
        if got!=exp['pair_status']: problems.append(f"pair status {got}")
    if 'safe_contains' in exp:
        for x in exp['safe_contains']:
            if x not in out.get('safe',[]): problems.append(f"safe missing {x}")
    if 'withheld_contains' in exp:
        for x in exp['withheld_contains']:
            if x not in out.get('withheld',[]): problems.append(f"withheld missing {x}")
    if 'trades_added' in exp and out.get('trades_added')!=exp['trades_added']: problems.append('trades_added mismatch')
    if 'cash_delta' in exp:
        got=out.get('cash_deltas',[{}])[0].get('cash_delta')
        if got!=exp['cash_delta']: problems.append(f"cash delta {got}")
    if 'shares_delta' in exp:
        got=out.get('position_deltas',[{}])[0].get('shares_delta')
        if got!=exp['shares_delta']: problems.append(f"shares delta {got}")
    return not problems, '; '.join(problems) if problems else 'ok'

def main():
    failed=[]
    for p in sorted(FIX.glob('*.json')):
        ok,msg=run_case(p); print(('PASS' if ok else 'FAIL'),p.name,'-',msg)
        if not ok: failed.append(p.name)
    print(f"\n{len(list(FIX.glob('*.json')))-len(failed)} passed / {len(failed)} failed")
    return 1 if failed else 0
if __name__=='__main__': raise SystemExit(main())

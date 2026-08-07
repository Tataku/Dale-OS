#!/usr/bin/env python3
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
EXPECTED={
'execution-charter','systemic-bug-instinct','truth-boundary','latest-authority','diff-scope-audit','protected-boundary','intent-drift-check','operator-ui-audit',
'money-trail','accounting-integrity','performance-truth','basis-proof','ledger-repair','transfer-neutrality','cash-truth','financial-evidence-grade','tax-character-proof','corporate-action-continuity','model-sanity','close-the-books'
}
errors=[]
def fail(msg): errors.append(msg)

def jsonl(path):
    out=[]
    try:
        lines=path.read_text(encoding='utf-8').splitlines()
    except Exception as exc:
        fail(f'{path.relative_to(ROOT)} unreadable: {exc}'); return out
    for n,line in enumerate(lines,1):
        if not line.strip(): continue
        try: out.append((n,json.loads(line)))
        except Exception as exc: fail(f'{path.relative_to(ROOT)}:{n} invalid JSON: {exc}')
    return out

activation=ROOT/'evals'/'activation'/'corpus.jsonl'
pos=set(); neg=set(); ids=set()
for n,row in jsonl(activation):
    cid=row.get('id'); expected=row.get('expected_skill'); forbidden=row.get('forbidden_skill'); prompt=row.get('prompt')
    if not cid or cid in ids: fail(f'{activation.relative_to(ROOT)}:{n} missing/duplicate id')
    ids.add(cid)
    if bool(expected)==bool(forbidden): fail(f'{activation.relative_to(ROOT)}:{n} define exactly one route expectation')
    route=expected or forbidden
    if route not in EXPECTED: fail(f'{activation.relative_to(ROOT)}:{n} unknown skill {route!r}')
    if expected: pos.add(expected)
    if forbidden: neg.add(forbidden)
    if not isinstance(prompt,str):
        fail(f'{activation.relative_to(ROOT)}:{n} prompt must be a string')
    elif expected and len(prompt)<20:
        fail(f'{activation.relative_to(ROOT)}:{n} positive activation prompt lacks trigger context')
    elif forbidden and len(prompt)<5:
        fail(f'{activation.relative_to(ROOT)}:{n} confuser prompt is trivial/empty')
if pos!=EXPECTED: fail(f'activation positive coverage drift: {sorted(EXPECTED-pos)} missing')
if neg!=EXPECTED: fail(f'activation confuser coverage drift: {sorted(EXPECTED-neg)} missing')
if len(ids)!=40: fail(f'activation corpus must contain 40 cases, got {len(ids)}')

behavior=ROOT/'evals'/'behavioral'/'flagship.jsonl'
behavior_skills=set()
for n,row in jsonl(behavior):
    skill=row.get('skill')
    if skill in EXPECTED: behavior_skills.add(skill)
if behavior_skills!=EXPECTED: fail(f'behavioral coverage drift: {sorted(EXPECTED-behavior_skills)} missing')

schema=ROOT/'schemas'/'model-eval-result.schema.json'
try:
    doc=json.loads(schema.read_text(encoding='utf-8'))
    if doc.get('$id')!='dale-os/model-eval-result/v1': fail('model eval result schema id drift')
    required=set(doc.get('required',[]))
    if required!={'case_id','runtime','model'}: fail(f'model eval required fields drift: {sorted(required)}')
except Exception as exc: fail(f'{schema.relative_to(ROOT)} invalid: {exc}')

for name in ('score_activation.py','score_behavioral.py'):
    p=ROOT/'scripts'/name
    r=subprocess.run([sys.executable,'-m','py_compile',str(p)],capture_output=True,text=True)
    if r.returncode: fail(f'{name} compile failed: {r.stderr.strip()}')

if errors:
    print('EVAL CONTRACT VALIDATION FAILED')
    for e in errors: print('-',e)
    raise SystemExit(1)
print('EVAL CONTRACT PASS: 20 positive routes + 20 confusers + 20 behavioral cases + portable result schema')

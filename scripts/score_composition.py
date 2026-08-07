#!/usr/bin/env python3
from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]
CORPUS=ROOT/'evals'/'composition'/'corpus.jsonl'
COMPS=json.loads((ROOT/'machine'/'compositions.json').read_text(encoding='utf-8'))
BY_ID={x['id']:{step['skill'] for step in x['sequence']} for x in COMPS['compositions']}

def rows(path):
    return [json.loads(line) for line in Path(path).read_text(encoding='utf-8').splitlines() if line.strip()]

if len(sys.argv)!=2:
    print('usage: score_composition.py results.jsonl',file=sys.stderr); raise SystemExit(2)
results={x['case_id']:x for x in rows(sys.argv[1])}
cases=rows(CORPUS)
covered=positive=negative=0
for case in cases:
    result=results.get(case['id'])
    if not result: continue
    covered+=1
    selected=set(result.get('selected_skills') or [])
    if 'expected_composition' in case:
        expected=BY_ID[case['expected_composition']]
        if selected==expected: positive+=1
    else:
        forbidden=BY_ID[case['forbidden_composition']]
        if selected!=forbidden: negative+=1
pos_total=sum('expected_composition' in c for c in cases)
neg_total=sum('forbidden_composition' in c for c in cases)
summary={
    'cases':len(cases),
    'coverage':covered/len(cases) if cases else 0,
    'positive_exact_composition':positive/pos_total if pos_total else 0,
    'negative_overcomposition_avoidance':negative/neg_total if neg_total else 0,
    'covered_cases':covered,
    'positive_passed':positive,
    'negative_passed':negative
}
print(json.dumps(summary,indent=2))
if covered!=len(cases): raise SystemExit(1)

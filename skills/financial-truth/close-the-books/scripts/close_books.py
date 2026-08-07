#!/usr/bin/env python3
from common import read_json, emit

SAFE={'PASS','NOT_APPLICABLE'}
DEGRADED={'WARNING'}
BLOCK={'BLOCKED','WITHHELD','UNRESOLVED','UNKNOWN'}

def analyze(data):
    domains={str(k):str(v).upper() for k,v in data.get('domains',{}).items()}
    analytics=data.get('analytics',{})
    results={}; safe=[]; degraded=[]; withheld=[]
    for name,required in analytics.items():
        states={d:domains.get(d,'UNKNOWN') for d in required}
        blockers=[d for d,s in states.items() if s in BLOCK or s not in SAFE|DEGRADED]
        warns=[d for d,s in states.items() if s in DEGRADED]
        if blockers:
            verdict='WITHHELD'; withheld.append(name)
        elif warns:
            verdict='DEGRADED'; degraded.append(name)
        else:
            verdict='PASS'; safe.append(name)
        results[name]={'status':verdict,'dependencies':states,'blockers':blockers,'warnings':warns}
    overall='PASS' if not withheld and not degraded else ('DEGRADED' if not withheld else 'PARTIAL')
    return {'status':overall,'analytics':results,'safe':safe,'degraded':degraded,'withheld':withheld}

if __name__ == '__main__': emit(analyze(read_json()))

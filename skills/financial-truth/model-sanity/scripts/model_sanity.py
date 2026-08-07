#!/usr/bin/env python3
from common import read_json, emit, dec

def analyze(data):
    failures=[]; warnings=[]; checks=[]
    probs=data.get('probabilities')
    if probs is not None:
        try: total=sum(dec(x,'probability') for x in probs)
        except ValueError as exc: failures.append(str(exc)); total=None
        if total is not None:
            ok=abs(total-dec(1)) <= dec(data.get('probability_tolerance','0.000001'))
            checks.append({'check':'probabilities_sum_to_one','pass':ok,'observed':float(total)})
            if not ok: failures.append('probabilities_do_not_sum_to_one')
    bs=data.get('balance_sheet')
    if bs:
        try:
            a=dec(bs.get('assets'),'assets'); l=dec(bs.get('liabilities'),'liabilities'); e=dec(bs.get('equity'),'equity'); delta=a-l-e
            tol=dec(bs.get('tolerance','0.01'),'balance_sheet.tolerance'); ok=abs(delta)<=tol
            checks.append({'check':'balance_sheet_identity','pass':ok,'delta':float(delta)})
            if not ok: failures.append('balance_sheet_identity_failed')
        except ValueError as exc: failures.append(str(exc))
    sc=data.get('scenarios')
    if sc and all(k in sc for k in ('downside','base','upside')):
        try:
            d,b,u=(dec(sc[k],k) for k in ('downside','base','upside')); ok=d<=b<=u
            checks.append({'check':'scenario_ordering','pass':ok,'values':[float(d),float(b),float(u)]})
            if not ok: failures.append('scenario_ordering_failed')
        except ValueError as exc: failures.append(str(exc))
    for r in data.get('bounded_metrics',[]):
        try:
            v=dec(r.get('value'),r.get('name','metric')); lo=dec(r.get('min'), 'min'); hi=dec(r.get('max'),'max'); ok=lo<=v<=hi
            checks.append({'check':f"bounded:{r.get('name','metric')}",'pass':ok,'observed':float(v),'range':[float(lo),float(hi)]})
            if not ok: failures.append(f"bounded_metric_failed:{r.get('name','metric')}")
        except ValueError as exc: failures.append(str(exc))
    for u in data.get('unit_equalities',[]):
        ok=str(u.get('left_unit'))==str(u.get('right_unit'))
        checks.append({'check':f"units:{u.get('name','unnamed')}",'pass':ok,'left':u.get('left_unit'),'right':u.get('right_unit')})
        if not ok: failures.append(f"unit_mismatch:{u.get('name','unnamed')}")
    if not checks: warnings.append('no_mechanical_checks_supplied')
    return {'status':'PASS' if not failures else 'BLOCKED','checks':checks,'failures':failures,'warnings':warnings}

if __name__ == '__main__': emit(analyze(read_json()))

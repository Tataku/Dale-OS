#!/usr/bin/env python3
from common import read_json, emit, dec, money

def position_map(rows):
    out={}
    for r in rows:
        key=f"{str(r.get('account_id',''))}::{str(r.get('ticker','')).upper()}"
        out[key]={'shares':dec(r.get('shares',0),'shares'),'cost_basis':dec(r.get('cost_basis',0),'cost_basis')}
    return out

def analyze(data):
    before=data.get('before',{}); after=data.get('after',{})
    bpos=position_map(before.get('positions',[])); apos=position_map(after.get('positions',[]))
    pdelta=[]
    for key in sorted(set(bpos)|set(apos)):
        b=bpos.get(key,{'shares':0,'cost_basis':0}); a=apos.get(key,{'shares':0,'cost_basis':0})
        ds=dec(a['shares'])-dec(b['shares']); dc=dec(a['cost_basis'])-dec(b['cost_basis'])
        if ds or dc:
            pdelta.append({'key':key,'shares_delta':float(ds),'cost_basis_delta':money(dc)})
    bc={k:dec(v,f'before.cash.{k}') for k,v in before.get('cash_by_account',{}).items()}
    ac={k:dec(v,f'after.cash.{k}') for k,v in after.get('cash_by_account',{}).items()}
    cdelta=[]
    for key in sorted(set(bc)|set(ac)):
        d=ac.get(key,0)-bc.get(key,0)
        if d: cdelta.append({'account_id':key,'cash_delta':money(dec(d))})
    bt={str(x.get('id')) for x in before.get('trades',[]) if x.get('id') is not None}; at={str(x.get('id')) for x in after.get('trades',[]) if x.get('id') is not None}
    return {'status':'PASS','trade_count_before':len(before.get('trades',[])),'trade_count_after':len(after.get('trades',[])),'trades_added':sorted(at-bt),'trades_removed':sorted(bt-at),'position_deltas':pdelta,'cash_deltas':cdelta}

if __name__ == '__main__': emit(analyze(read_json()))

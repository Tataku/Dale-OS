#!/usr/bin/env python3
from collections import defaultdict, deque
from decimal import Decimal
from common import read_json, emit, dec, iso_day, money

def analyze(data):
    method=str(data.get("method","FIFO")).upper()
    if method != "FIFO":
        return {"status":"BLOCKED","errors":["v0.1 deterministic tool supports FIFO only"]}
    events=[]; errors=[]
    for i,row in enumerate(data.get("events",[])):
        try:
            day=iso_day(row.get("date"),f"events[{i}].date")
            shares=dec(row.get("shares"),f"events[{i}].shares")
            price=dec(row.get("price"),f"events[{i}].price")
        except ValueError as exc:
            errors.append(str(exc)); continue
        typ=str(row.get("type","")).upper(); ticker=str(row.get("ticker","")).upper(); account=str(row.get("account_id",""))
        if typ not in {"BUY","SELL"}: errors.append(f"events[{i}].type unsupported"); continue
        if not ticker or not account or shares <= 0 or price < 0: errors.append(f"events[{i}] has invalid ticker/account/shares/price"); continue
        events.append((day,i,{**row,"type":typ,"ticker":ticker,"account_id":account,"shares":shares,"price":price}))
    events.sort(key=lambda x:(x[0],x[1]))
    lots=defaultdict(deque); disposals=[]
    for day,idx,e in events:
        key=(e["ticker"],e["account_id"])
        if e["type"]=="BUY":
            lots[key].append({"event_id":str(e.get("id",idx)),"date":day,"remaining":e["shares"],"unit_cost":e["price"]})
            continue
        needed=e["shares"]; basis=Decimal('0'); supported=Decimal('0'); consumed=[]
        while needed>0 and lots[key]:
            lot=lots[key][0]; take=min(needed,lot["remaining"])
            cost=take*lot["unit_cost"]; basis+=cost; supported+=take; needed-=take; lot["remaining"]-=take
            consumed.append({"lot_id":lot["event_id"],"acquired":lot["date"].isoformat(),"shares":float(take),"basis":money(cost)})
            if lot["remaining"]==0: lots[key].popleft()
        proceeds=e["shares"]*e["price"]
        verified=needed==0
        disposals.append({"event_id":str(e.get("id",idx)),"ticker":e["ticker"],"account_id":e["account_id"],"date":day.isoformat(),"shares_sold":float(e["shares"]),"shares_supported":float(supported),"shares_unsupported":float(needed),"proceeds":money(proceeds),"proven_basis":money(basis),"realized_gain":money(proceeds-basis) if verified else None,"status":"VERIFIED" if verified else "UNVERIFIED_OVERSOLD","lots_consumed":consumed})
    status="BLOCKED" if errors else ("UNRESOLVED" if any(d["status"]!="VERIFIED" for d in disposals) else "PASS")
    return {"status":status,"method":"FIFO","errors":errors,"disposals":disposals}

if __name__ == '__main__': emit(analyze(read_json()))

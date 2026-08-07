#!/usr/bin/env python3
from collections import defaultdict
from decimal import Decimal
from common import read_json, emit, dec, iso_day, money

EXTERNAL = {"contribution", "withdrawal"}
INTERNAL = {"internal_transfer"}
KNOWN = EXTERNAL | INTERNAL | {"trade_settlement", "income", "fee", "tax", "correction", "reconciliation"}

def analyze(data):
    rows = data.get("movements", [])
    tol = dec(data.get("tolerance", "0.01"), "tolerance")
    ids=set(); errors=[]; unresolved=[]; duplicates=[]; pairs=defaultdict(list)
    seen_fingerprint={}
    external=Decimal('0'); classified=Decimal('0')
    normalized=[]
    for i,row in enumerate(rows):
        rid=str(row.get("id", "")).strip()
        if not rid or rid in ids:
            errors.append(f"movement[{i}] has missing/duplicate id")
            continue
        ids.add(rid)
        try:
            amt=dec(row.get("amount"), f"movement[{i}].amount")
            day=iso_day(row.get("date"), f"movement[{i}].date")
        except ValueError as exc:
            errors.append(str(exc)); continue
        account=str(row.get("account_id", "")).strip()
        currency=str(row.get("currency", "USD")).upper()
        classification=str(row.get("classification", "unknown")).strip().lower()
        evidence=str(row.get("evidence_grade", "UNKNOWN")).upper()
        pair_id=row.get("pair_id")
        if classification not in KNOWN:
            unresolved.append(rid)
        else:
            classified += amt
            if classification in EXTERNAL:
                external += amt
        if pair_id:
            pairs[str(pair_id)].append((rid,account,currency,amt,classification))
        fp=(account, day.isoformat(), currency, amt, str(row.get("source_ref", "")))
        if fp in seen_fingerprint:
            duplicates.append([seen_fingerprint[fp], rid])
        else:
            seen_fingerprint[fp]=rid
        normalized.append({"id":rid,"account_id":account,"date":day.isoformat(),"amount":money(amt),"currency":currency,"classification":classification,"evidence_grade":evidence,"pair_id":pair_id})

    pair_results=[]
    for pid,legs in sorted(pairs.items()):
        reasons=[]
        if len(legs)!=2: reasons.append("pair_must_have_exactly_two_legs")
        else:
            a,b=legs
            if a[1] == b[1]: reasons.append("same_account")
            if a[2] != b[2]: reasons.append("currency_mismatch")
            if abs(a[3]+b[3]) > tol: reasons.append("amounts_do_not_net_to_zero")
            if a[4] != "internal_transfer" or b[4] != "internal_transfer": reasons.append("classification_not_internal_transfer")
        pair_results.append({"pair_id":pid,"status":"PASS" if not reasons else "UNRESOLVED","reasons":reasons,"legs":[x[0] for x in legs]})

    if errors:
        status="BLOCKED"
    elif unresolved or any(p["status"]!="PASS" for p in pair_results) or duplicates:
        status="UNRESOLVED"
    else:
        status="PASS"
    return {"status":status,"movement_count":len(normalized),"external_flow_total":money(external),"unresolved_ids":unresolved,"duplicate_candidates":duplicates,"transfer_pairs":pair_results,"errors":errors,"movements":normalized}

if __name__ == '__main__':
    emit(analyze(read_json()))

#!/usr/bin/env python3
from common import read_json, emit, dec, iso_day

def analyze(data):
    max_gap=int(data.get("max_gap_days",4))
    vals=[]; errors=[]
    for i,row in enumerate(data.get("valuations",[])):
        try:
            day=iso_day(row.get("date"), f"valuations[{i}].date")
            value=dec(row.get("value"), f"valuations[{i}].value")
        except ValueError as exc:
            errors.append(str(exc)); continue
        if value < 0: errors.append(f"valuations[{i}].value must be non-negative"); continue
        if bool(row.get("trusted", False)):
            vals.append((day,value))
    vals.sort(key=lambda x:x[0])
    gaps=[]
    segment_start=0
    for i in range(1,len(vals)):
        gap=(vals[i][0]-vals[i-1][0]).days
        if gap>max_gap:
            gaps.append({"from":vals[i-1][0].isoformat(),"to":vals[i][0].isoformat(),"days":gap})
            segment_start=i
    newest=vals[segment_start:]
    unresolved=list(data.get("unresolved_movements",[]))
    blockers=[]
    if errors: blockers.append("invalid_valuation_data")
    if len(newest)<2: blockers.append("fewer_than_two_trusted_continuous_valuations")
    if unresolved: blockers.append("unresolved_cash_movements")
    if data.get("flow_coverage") in (False,"incomplete","unknown",None): blockers.append("external_flow_coverage_incomplete")
    method=data.get("requested_method")
    if method == "simple" and data.get("has_external_flows",False): blockers.append("simple_return_invalid_with_external_flows")
    status="PASS" if not blockers else "WITHHELD"
    period=None
    if newest:
        period={"start":newest[0][0].isoformat(),"end":newest[-1][0].isoformat(),"points":len(newest)}
    return {"status":status,"blockers":blockers,"trusted_valuation_count":len(vals),"newest_continuous_segment":period,"gaps":gaps,"unresolved_movement_count":len(unresolved),"requested_method":method,"errors":errors}

if __name__ == '__main__': emit(analyze(read_json()))

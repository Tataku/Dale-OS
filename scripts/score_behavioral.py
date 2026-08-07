#!/usr/bin/env python3
"""Lexically score model responses against Dale OS behavioral smoke cases.

This is intentionally a smoke gate, not a semantic grader. A lexical PASS proves
only that required markers are present and forbidden markers are absent. Human or
independent semantic review is still required for high-stakes claims.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path


def rows(path: Path):
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            yield n, json.loads(line)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"{path}:{n}: invalid JSON: {exc}") from exc


def pct(num: int, den: int):
    return None if den == 0 else round(num / den, 4)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", default="evals/behavioral/flagship.jsonl")
    ap.add_argument("results")
    args = ap.parse_args()
    case_path, result_path = Path(args.cases), Path(args.results)

    cases = {}
    for n, case in rows(case_path):
        cid = case.get("id")
        if not cid or cid in cases:
            raise SystemExit(f"{case_path}:{n}: missing/duplicate id")
        cases[cid] = case

    seen, details = set(), []
    passed_count = 0
    unknown_result_ids = []
    for n, result in rows(result_path):
        cid = result.get("case_id")
        if cid in seen:
            raise SystemExit(f"{result_path}:{n}: duplicate case_id {cid!r}")
        seen.add(cid)
        if cid not in cases:
            unknown_result_ids.append(cid)
            continue
        response = result.get("response")
        if not isinstance(response, str):
            raise SystemExit(f"{result_path}:{n}: response must be a string")
        text = response.casefold()
        case = cases[cid]
        required = [str(x) for x in case.get("must", [])]
        forbidden = [str(x) for x in case.get("must_not", [])]
        missing = [x for x in required if x.casefold() not in text]
        present_forbidden = [x for x in forbidden if x.casefold() in text]
        passed = not missing and not present_forbidden
        passed_count += int(passed)
        details.append({
            "case_id": cid,
            "skill": case.get("skill"),
            "lexical_pass": passed,
            "missing_required": missing,
            "present_forbidden": present_forbidden,
        })

    missing_cases = sorted(set(cases) - seen)
    out = {
        "schema": "dale-os/behavioral-lexical-score/v1",
        "warning": "Lexical smoke score only; do not treat as semantic proof.",
        "cases": len(cases),
        "results_scored": len(details),
        "coverage": pct(len(details), len(cases)),
        "lexical_pass_rate": pct(passed_count, len(details)),
        "missing_case_ids": missing_cases,
        "unknown_result_ids": unknown_result_ids,
        "details": details,
    }
    print(json.dumps(out, indent=2, sort_keys=True))
    if missing_cases or unknown_result_ids:
        raise SystemExit(2)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Score Dale OS skill-routing results without calling a model.

Input results JSONL rows:
  {"case_id":"...", "selected_skills":["skill-name"], "model":"optional"}

Corpus rows may define either expected_skill (positive route) or forbidden_skill
(confuser / negative route). This scorer measures routing, not answer quality.
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
    ap.add_argument("--corpus", default="evals/activation/corpus.jsonl")
    ap.add_argument("results")
    args = ap.parse_args()
    corpus_path, results_path = Path(args.corpus), Path(args.results)

    corpus = {}
    for n, case in rows(corpus_path):
        cid = case.get("id")
        if not cid or cid in corpus:
            raise SystemExit(f"{corpus_path}:{n}: missing/duplicate id")
        if bool(case.get("expected_skill")) == bool(case.get("forbidden_skill")):
            raise SystemExit(f"{corpus_path}:{n}: define exactly one of expected_skill or forbidden_skill")
        corpus[cid] = case

    seen, details = set(), []
    positives = positive_hits = exact_hits = 0
    negatives = negative_hits = 0
    unknown_result_ids = []

    for n, result in rows(results_path):
        cid = result.get("case_id")
        if cid in seen:
            raise SystemExit(f"{results_path}:{n}: duplicate case_id {cid!r}")
        seen.add(cid)
        if cid not in corpus:
            unknown_result_ids.append(cid)
            continue
        selected = result.get("selected_skills", [])
        if not isinstance(selected, list) or not all(isinstance(x, str) for x in selected):
            raise SystemExit(f"{results_path}:{n}: selected_skills must be a list[str]")
        selected = list(dict.fromkeys(selected))
        case = corpus[cid]
        expected, forbidden = case.get("expected_skill"), case.get("forbidden_skill")
        if expected:
            positives += 1
            hit = expected in selected
            exact = selected == [expected]
            positive_hits += int(hit)
            exact_hits += int(exact)
            passed = hit
            reason = "expected skill selected" if hit else "expected skill missing"
        else:
            negatives += 1
            passed = forbidden not in selected
            negative_hits += int(passed)
            exact = None
            reason = "forbidden skill avoided" if passed else "forbidden skill selected"
        details.append({"case_id": cid, "pass": passed, "exact": exact, "selected_skills": selected, "reason": reason})

    missing = sorted(set(corpus) - seen)
    out = {
        "schema": "dale-os/activation-score/v1",
        "corpus_cases": len(corpus),
        "results_scored": len(details),
        "coverage": pct(len(details), len(corpus)),
        "positive_recall": pct(positive_hits, positives),
        "positive_exact_route": pct(exact_hits, positives),
        "negative_avoidance": pct(negative_hits, negatives),
        "missing_case_ids": missing,
        "unknown_result_ids": unknown_result_ids,
        "details": details,
    }
    print(json.dumps(out, indent=2, sort_keys=True))
    if missing or unknown_result_ids:
        raise SystemExit(2)


if __name__ == "__main__":
    main()

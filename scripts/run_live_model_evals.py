#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_jsonl(path: Path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def post_json(url: str, headers: dict[str, str], payload: dict, *, attempts: int = 4):
    body = json.dumps(payload).encode("utf-8")
    for attempt in range(1, attempts + 1):
        req = urllib.request.Request(url, data=body, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            if exc.code in {429, 500, 502, 503, 504} and attempt < attempts:
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError(f"HTTP {exc.code} from {url}: {detail[:1200]}") from exc
        except urllib.error.URLError as exc:
            if attempt < attempts:
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError(f"Network error from {url}: {exc}") from exc
    raise AssertionError("unreachable")


def openai_text(api_key: str, model: str, system: str, user: str, max_tokens: int = 1600):
    data = post_json(
        "https://api.openai.com/v1/chat/completions",
        {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        {
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "max_completion_tokens": max_tokens,
        },
    )
    return data["choices"][0]["message"]["content"] or ""


def anthropic_text(api_key: str, model: str, system: str, user: str, max_tokens: int = 1600):
    data = post_json(
        "https://api.anthropic.com/v1/messages",
        {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        {
            "model": model,
            "system": system,
            "messages": [{"role": "user", "content": user}],
            "max_tokens": max_tokens,
        },
    )
    return "".join(block.get("text", "") for block in data.get("content", []) if block.get("type") == "text")


def extract_json(text: str):
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    fenced = re.search(r"```(?:json)?\s*(.*?)```", text, re.S | re.I)
    if fenced:
        return json.loads(fenced.group(1).strip())
    start_candidates = [p for p in (text.find("["), text.find("{")) if p >= 0]
    if not start_candidates:
        raise ValueError(f"No JSON found in model output: {text[:500]}")
    start = min(start_candidates)
    decoder = json.JSONDecoder()
    value, _ = decoder.raw_decode(text[start:])
    return value


def pct(num: int, den: int):
    return 0.0 if not den else round(num / den, 4)


def route_catalog(manifest: dict):
    return [
        {"name": skill["name"], "description": skill["description"]}
        for skill in manifest["skills"]
    ]


def run_routing(call, manifest: dict, cases: list[dict]):
    catalog = route_catalog(manifest)
    system = (
        "You are evaluating skill activation for Dale OS. Select the smallest set of canonical skills that should be loaded "
        "for each independent user request. Do not select a skill merely because it is vaguely related. Return JSON only."
    )
    user = json.dumps({
        "skill_catalog": catalog,
        "cases": [{"case_id": c["id"], "prompt": c["prompt"]} for c in cases],
        "output_schema": [{"case_id": "string", "selected_skills": ["canonical-skill-name"]}],
    }, indent=2)
    parsed = extract_json(call(system, user, 5000))
    if not isinstance(parsed, list):
        raise RuntimeError("routing output must be a JSON array")
    by_id = {row.get("case_id"): row for row in parsed if isinstance(row, dict)}
    results = []
    for case in cases:
        row = by_id.get(case["id"], {})
        selected = row.get("selected_skills", [])
        if not isinstance(selected, list):
            selected = []
        valid = [x for x in dict.fromkeys(selected) if isinstance(x, str) and x in {s["name"] for s in catalog}]
        results.append({"case_id": case["id"], "selected_skills": valid})
    return results


def score_activation(cases, results):
    result_map = {x["case_id"]: x for x in results}
    positives = [c for c in cases if c.get("expected_skill")]
    negatives = [c for c in cases if c.get("forbidden_skill")]
    recall = exact = avoidance = 0
    details = []
    for case in cases:
        selected = result_map.get(case["id"], {}).get("selected_skills", [])
        if case.get("expected_skill"):
            hit = case["expected_skill"] in selected
            is_exact = selected == [case["expected_skill"]]
            recall += int(hit)
            exact += int(is_exact)
            details.append({"case_id": case["id"], "selected_skills": selected, "expected": case["expected_skill"], "pass": hit, "exact": is_exact})
        else:
            hit = case["forbidden_skill"] not in selected
            avoidance += int(hit)
            details.append({"case_id": case["id"], "selected_skills": selected, "forbidden": case["forbidden_skill"], "pass": hit})
    return {
        "coverage": pct(len(result_map), len(cases)),
        "positive_recall": pct(recall, len(positives)),
        "positive_exact_route": pct(exact, len(positives)),
        "negative_avoidance": pct(avoidance, len(negatives)),
        "details": details,
    }


def run_composition(call, manifest: dict, compositions: dict, cases: list[dict]):
    catalog = route_catalog(manifest)
    recipes = [
        {
            "id": c["id"],
            "use_when": c["use_when"],
            "skills": [s["skill"] for s in c["sequence"]],
            "handoff_contract": c["handoff_contract"],
        }
        for c in compositions["compositions"]
    ]
    system = (
        "You are evaluating Dale OS composition. For each independent request, select the smallest set of canonical skills "
        "that owns distinct obligations in the task. Do not load an entire composition when the task is simpler. Return JSON only."
    )
    user = json.dumps({
        "skill_catalog": catalog,
        "canonical_compositions": recipes,
        "cases": [{"case_id": c["id"], "prompt": c["prompt"]} for c in cases],
        "output_schema": [{"case_id": "string", "selected_skills": ["canonical-skill-name"]}],
    }, indent=2)
    parsed = extract_json(call(system, user, 3500))
    if not isinstance(parsed, list):
        raise RuntimeError("composition output must be a JSON array")
    valid_names = {x["name"] for x in catalog}
    by_id = {row.get("case_id"): row for row in parsed if isinstance(row, dict)}
    return [
        {
            "case_id": case["id"],
            "selected_skills": [
                x for x in dict.fromkeys(by_id.get(case["id"], {}).get("selected_skills", []))
                if isinstance(x, str) and x in valid_names
            ],
        }
        for case in cases
    ]


def score_composition(cases, results, compositions):
    by_comp = {c["id"]: {s["skill"] for s in c["sequence"]} for c in compositions["compositions"]}
    result_map = {x["case_id"]: set(x.get("selected_skills", [])) for x in results}
    positives = [c for c in cases if c.get("expected_composition")]
    negatives = [c for c in cases if c.get("forbidden_composition")]
    positive_hits = negative_hits = 0
    details = []
    for case in cases:
        selected = result_map.get(case["id"], set())
        if case.get("expected_composition"):
            expected = by_comp[case["expected_composition"]]
            passed = selected == expected
            positive_hits += int(passed)
            details.append({"case_id": case["id"], "selected_skills": sorted(selected), "expected_skills": sorted(expected), "pass": passed})
        else:
            forbidden = by_comp[case["forbidden_composition"]]
            passed = selected != forbidden
            negative_hits += int(passed)
            details.append({"case_id": case["id"], "selected_skills": sorted(selected), "forbidden_full_composition": sorted(forbidden), "pass": passed})
    return {
        "coverage": pct(len(result_map), len(cases)),
        "positive_exact_composition": pct(positive_hits, len(positives)),
        "negative_overcomposition_avoidance": pct(negative_hits, len(negatives)),
        "details": details,
    }


def run_behavioral(call, cases: list[dict]):
    results = []
    for case in cases:
        skill_path = next((ROOT / "skills").glob(f"*/{case['skill']}/SKILL.md"))
        skill_text = skill_path.read_text(encoding="utf-8")
        system = (
            "Apply the following Dale OS skill to the user's request. Follow its rule, boundaries, procedure, and falsifier. "
            "Answer the user directly and concisely.\n\n" + skill_text
        )
        response = call(system, case["prompt"], 900)
        results.append({"case_id": case["id"], "response": response})
    return results


def score_behavioral(cases, results):
    result_map = {x["case_id"]: x.get("response", "") for x in results}
    passed = 0
    details = []
    for case in cases:
        response = result_map.get(case["id"], "")
        folded = response.casefold()
        missing = [x for x in case.get("must", []) if str(x).casefold() not in folded]
        forbidden = [x for x in case.get("must_not", []) if str(x).casefold() in folded]
        ok = not missing and not forbidden
        passed += int(ok)
        details.append({"case_id": case["id"], "skill": case["skill"], "lexical_pass": ok, "missing_required": missing, "present_forbidden": forbidden, "response": response})
    return {
        "coverage": pct(len(result_map), len(cases)),
        "lexical_pass_rate": pct(passed, len(cases)),
        "details": details,
    }


def passes(score: dict, threshold: dict, mapping: dict[str, str]):
    failures = []
    for score_key, threshold_key in mapping.items():
        actual = score.get(score_key, 0)
        required = threshold[threshold_key]
        if actual + 1e-9 < required:
            failures.append({"metric": score_key, "actual": actual, "required": required})
    return failures


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="artifacts/live-model-eval")
    args = ap.parse_args()
    out = ROOT / args.out
    out.mkdir(parents=True, exist_ok=True)

    thresholds = json.loads((ROOT / "release/live-model-thresholds.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    compositions = json.loads((ROOT / "machine/compositions.json").read_text(encoding="utf-8"))
    activation_cases = load_jsonl(ROOT / "evals/activation/corpus.jsonl")
    composition_cases = load_jsonl(ROOT / "evals/composition/corpus.jsonl")
    behavioral_cases = load_jsonl(ROOT / "evals/behavioral/flagship.jsonl")

    openai_key = os.environ.get("OPENAI_API_KEY", "")
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not openai_key or not anthropic_key:
        raise SystemExit("OPENAI_API_KEY and ANTHROPIC_API_KEY are both required")

    model_specs = thresholds["models"]
    providers = {
        "openai": lambda model: (lambda system, user, max_tokens: openai_text(openai_key, model, system, user, max_tokens)),
        "anthropic": lambda model: (lambda system, user, max_tokens: anthropic_text(anthropic_key, model, system, user, max_tokens)),
    }

    report = {
        "schema": "dale-os/live-model-eval-report/v1",
        "dale_os_version": (ROOT / "VERSION").read_text(encoding="utf-8").strip(),
        "threshold_contract": "release/live-model-thresholds.json",
        "models": [],
    }
    any_failure = False

    for spec in model_specs:
        provider, model = spec["provider"], spec["model"]
        print(f"running {provider}:{model}", flush=True)
        call = providers[provider](model)
        activation_results = run_routing(call, manifest, activation_cases)
        activation_score = score_activation(activation_cases, activation_results)
        composition_results = run_composition(call, manifest, compositions, composition_cases)
        composition_score = score_composition(composition_cases, composition_results, compositions)
        behavioral_results = run_behavioral(call, behavioral_cases)
        behavioral_score = score_behavioral(behavioral_cases, behavioral_results)

        t = thresholds["per_model"]
        failures = []
        failures += passes(activation_score, t["activation"], {
            "coverage": "coverage",
            "positive_recall": "positive_recall_min",
            "positive_exact_route": "positive_exact_route_min",
            "negative_avoidance": "negative_avoidance_min",
        })
        failures += passes(composition_score, t["composition"], {
            "coverage": "coverage",
            "positive_exact_composition": "positive_exact_composition_min",
            "negative_overcomposition_avoidance": "negative_overcomposition_avoidance_min",
        })
        failures += passes(behavioral_score, t["behavioral_lexical"], {
            "coverage": "coverage",
            "lexical_pass_rate": "lexical_pass_rate_min",
        })
        status = "PASS" if not failures else "REVIEW_REQUIRED"
        any_failure |= bool(failures)
        model_report = {
            "provider": provider,
            "model": model,
            "status": status,
            "activation": activation_score,
            "composition": composition_score,
            "behavioral_lexical": behavioral_score,
            "threshold_failures": failures,
        }
        report["models"].append(model_report)
        (out / f"{provider}.json").write_text(json.dumps(model_report, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({
            "provider": provider,
            "model": model,
            "status": status,
            "activation": {k: v for k, v in activation_score.items() if k != "details"},
            "composition": {k: v for k, v in composition_score.items() if k != "details"},
            "behavioral_lexical": {k: v for k, v in behavioral_score.items() if k != "details"},
            "threshold_failures": failures,
        }, indent=2), flush=True)

    report["status"] = "PASS" if not any_failure else "REVIEW_REQUIRED"
    (out / "report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if any_failure:
        raise SystemExit(3)


if __name__ == "__main__":
    main()

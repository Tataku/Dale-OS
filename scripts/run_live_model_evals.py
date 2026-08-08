#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_jsonl(path: Path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def request_json(url: str, headers: dict[str, str], payload: dict | None = None, *, attempts: int = 4):
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    method = "GET" if payload is None else "POST"
    for attempt in range(1, attempts + 1):
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
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


def openai_models(api_key: str):
    data = request_json("https://api.openai.com/v1/models", {"Authorization": f"Bearer {api_key}"})
    return sorted({x.get("id") for x in data.get("data", []) if isinstance(x, dict) and x.get("id")})


def anthropic_models(api_key: str):
    data = request_json(
        "https://api.anthropic.com/v1/models?limit=1000",
        {"x-api-key": api_key, "anthropic-version": "2023-06-01"},
    )
    return sorted({x.get("id") for x in data.get("data", []) if isinstance(x, dict) and x.get("id")})


def choose_model(spec: dict, available: list[str], used: set[str]):
    available_set = set(available)
    for preferred in spec["preferred_ids"]:
        if preferred in available_set and preferred not in used:
            return preferred
        snapshots = sorted(
            [m for m in available if m.startswith(preferred + "-") and m not in used],
            reverse=True,
        )
        if snapshots:
            return snapshots[0]
    raise RuntimeError(
        f"No model exposed for {spec['provider']}:{spec['role']} from preferred IDs {spec['preferred_ids']}. "
        f"Available candidates: {available[:120]}"
    )


def openai_text(api_key: str, model: str, system: str, user: str, max_tokens: int = 1600):
    data = request_json(
        "https://api.openai.com/v1/chat/completions",
        {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        {
            "model": model,
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
            "max_completion_tokens": max_tokens,
        },
    )
    return data["choices"][0]["message"]["content"] or ""


def anthropic_text(api_key: str, model: str, system: str, user: str, max_tokens: int = 1600):
    data = request_json(
        "https://api.anthropic.com/v1/messages",
        {"x-api-key": api_key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
        {"model": model, "system": system, "messages": [{"role": "user", "content": user}], "max_tokens": max_tokens},
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
    starts = [p for p in (text.find("["), text.find("{")) if p >= 0]
    if not starts:
        raise ValueError(f"No JSON found in model output: {text[:500]}")
    value, _ = json.JSONDecoder().raw_decode(text[min(starts):])
    return value


def pct(num: int, den: int):
    return 0.0 if not den else round(num / den, 4)


def route_catalog(manifest: dict):
    return [{"name": x["name"], "description": x["description"]} for x in manifest["skills"]]


def run_routing(call, manifest: dict, cases: list[dict]):
    catalog = route_catalog(manifest)
    valid_names = {x["name"] for x in catalog}
    system = "Select the smallest set of Dale OS canonical skills needed for each independent request. Avoid vaguely related skills. Return JSON only."
    user = json.dumps({
        "skill_catalog": catalog,
        "cases": [{"case_id": c["id"], "prompt": c["prompt"]} for c in cases],
        "output_schema": [{"case_id": "string", "selected_skills": ["canonical-skill-name"]}],
    }, indent=2)
    parsed = extract_json(call(system, user, 5000))
    if not isinstance(parsed, list):
        raise RuntimeError("routing output must be a JSON array")
    by_id = {x.get("case_id"): x for x in parsed if isinstance(x, dict)}
    out = []
    for case in cases:
        selected = by_id.get(case["id"], {}).get("selected_skills", [])
        if not isinstance(selected, list):
            selected = []
        out.append({"case_id": case["id"], "selected_skills": [x for x in dict.fromkeys(selected) if isinstance(x, str) and x in valid_names]})
    return out


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
            exact_hit = selected == [case["expected_skill"]]
            recall += int(hit)
            exact += int(exact_hit)
            details.append({"case_id": case["id"], "selected_skills": selected, "expected": case["expected_skill"], "pass": hit, "exact": exact_hit})
        else:
            hit = case["forbidden_skill"] not in selected
            avoidance += int(hit)
            details.append({"case_id": case["id"], "selected_skills": selected, "forbidden": case["forbidden_skill"], "pass": hit})
    return {"coverage": pct(len(result_map), len(cases)), "positive_recall": pct(recall, len(positives)), "positive_exact_route": pct(exact, len(positives)), "negative_avoidance": pct(avoidance, len(negatives)), "details": details}


def run_composition(call, manifest: dict, compositions: dict, cases: list[dict]):
    catalog = route_catalog(manifest)
    valid_names = {x["name"] for x in catalog}
    recipes = [{"id": c["id"], "use_when": c["use_when"], "skills": [s["skill"] for s in c["sequence"]], "handoff_contract": c["handoff_contract"]} for c in compositions["compositions"]]
    system = "Select the smallest set of Dale OS skills that owns distinct obligations in each request. Do not load full compositions when the task is simpler. Return JSON only."
    user = json.dumps({
        "skill_catalog": catalog,
        "canonical_compositions": recipes,
        "cases": [{"case_id": c["id"], "prompt": c["prompt"]} for c in cases],
        "output_schema": [{"case_id": "string", "selected_skills": ["canonical-skill-name"]}],
    }, indent=2)
    parsed = extract_json(call(system, user, 3500))
    if not isinstance(parsed, list):
        raise RuntimeError("composition output must be a JSON array")
    by_id = {x.get("case_id"): x for x in parsed if isinstance(x, dict)}
    out = []
    for case in cases:
        selected = by_id.get(case["id"], {}).get("selected_skills", [])
        if not isinstance(selected, list):
            selected = []
        out.append({"case_id": case["id"], "selected_skills": [x for x in dict.fromkeys(selected) if isinstance(x, str) and x in valid_names]})
    return out


def score_composition(cases, results, compositions):
    by_comp = {c["id"]: {s["skill"] for s in c["sequence"]} for c in compositions["compositions"]}
    result_map = {x["case_id"]: set(x.get("selected_skills", [])) for x in results}
    positives = [c for c in cases if c.get("expected_composition")]
    negatives = [c for c in cases if c.get("forbidden_composition")]
    pos = neg = 0
    details = []
    for case in cases:
        selected = result_map.get(case["id"], set())
        if case.get("expected_composition"):
            expected = by_comp[case["expected_composition"]]
            ok = selected == expected
            pos += int(ok)
            details.append({"case_id": case["id"], "selected_skills": sorted(selected), "expected_skills": sorted(expected), "pass": ok})
        else:
            forbidden = by_comp[case["forbidden_composition"]]
            ok = selected != forbidden
            neg += int(ok)
            details.append({"case_id": case["id"], "selected_skills": sorted(selected), "forbidden_full_composition": sorted(forbidden), "pass": ok})
    return {"coverage": pct(len(result_map), len(cases)), "positive_exact_composition": pct(pos, len(positives)), "negative_overcomposition_avoidance": pct(neg, len(negatives)), "details": details}


def run_behavioral(call, cases: list[dict]):
    out = []
    for case in cases:
        skill_path = next((ROOT / "skills").glob(f"*/{case['skill']}/SKILL.md"))
        skill_text = skill_path.read_text(encoding="utf-8")
        system = "Apply this Dale OS skill faithfully. Follow its rule, boundaries, procedure, and falsifier. Answer directly and concisely.\n\n" + skill_text
        out.append({"case_id": case["id"], "response": call(system, case["prompt"], 900)})
    return out


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
    return {"coverage": pct(len(result_map), len(cases)), "lexical_pass_rate": pct(passed, len(cases)), "details": details}


def threshold_failures(scores: dict, thresholds: dict):
    checks = [
        ("activation", "coverage", "coverage"),
        ("activation", "positive_recall", "positive_recall_min"),
        ("activation", "positive_exact_route", "positive_exact_route_min"),
        ("activation", "negative_avoidance", "negative_avoidance_min"),
        ("composition", "coverage", "coverage"),
        ("composition", "positive_exact_composition", "positive_exact_composition_min"),
        ("composition", "negative_overcomposition_avoidance", "negative_overcomposition_avoidance_min"),
        ("behavioral_lexical", "coverage", "coverage"),
        ("behavioral_lexical", "lexical_pass_rate", "lexical_pass_rate_min"),
    ]
    failures = []
    for group, metric, threshold_key in checks:
        actual = scores[group][metric]
        required = thresholds[group][threshold_key]
        if actual + 1e-9 < required:
            failures.append({"group": group, "metric": metric, "actual": actual, "required": required})
    return failures


def safe_name(provider: str, role: str, model: str):
    return re.sub(r"[^a-zA-Z0-9._-]+", "-", f"{provider}-{role}-{model}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="artifacts/live-model-eval")
    args = ap.parse_args()
    out = ROOT / args.out
    out.mkdir(parents=True, exist_ok=True)

    contract = json.loads((ROOT / "release/live-model-thresholds.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    compositions = json.loads((ROOT / "machine/compositions.json").read_text(encoding="utf-8"))
    activation_cases = load_jsonl(ROOT / "evals/activation/corpus.jsonl")
    composition_cases = load_jsonl(ROOT / "evals/composition/corpus.jsonl")
    behavioral_cases = load_jsonl(ROOT / "evals/behavioral/flagship.jsonl")

    openai_key = os.environ.get("OPENAI_API_KEY", "")
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not openai_key or not anthropic_key:
        raise SystemExit("OPENAI_API_KEY and ANTHROPIC_API_KEY are both required")

    available = {"openai": openai_models(openai_key), "anthropic": anthropic_models(anthropic_key)}
    used = {"openai": set(), "anthropic": set()}
    resolved = []
    for spec in contract["models"]:
        provider = spec["provider"]
        model = choose_model(spec, available[provider], used[provider])
        used[provider].add(model)
        resolved.append({**spec, "model": model})

    print(json.dumps({"resolved_models": [{"provider": x["provider"], "role": x["role"], "model": x["model"]} for x in resolved]}, indent=2), flush=True)

    providers = {
        "openai": lambda model: (lambda system, user, max_tokens: openai_text(openai_key, model, system, user, max_tokens)),
        "anthropic": lambda model: (lambda system, user, max_tokens: anthropic_text(anthropic_key, model, system, user, max_tokens)),
    }

    report = {
        "schema": "dale-os/live-model-eval-report/v2",
        "dale_os_version": (ROOT / "VERSION").read_text(encoding="utf-8").strip(),
        "threshold_contract": "release/live-model-thresholds.json",
        "resolved_models": [{"provider": x["provider"], "role": x["role"], "model": x["model"]} for x in resolved],
        "models": [],
    }
    any_failure = False

    for spec in resolved:
        provider, role, model = spec["provider"], spec["role"], spec["model"]
        print(f"running {provider}:{role}:{model}", flush=True)
        call = providers[provider](model)
        activation = score_activation(activation_cases, run_routing(call, manifest, activation_cases))
        composition = score_composition(composition_cases, run_composition(call, manifest, compositions, composition_cases), compositions)
        behavioral = score_behavioral(behavioral_cases, run_behavioral(call, behavioral_cases))
        scores = {"activation": activation, "composition": composition, "behavioral_lexical": behavioral}
        failures = threshold_failures(scores, contract["per_model"])
        status = "PASS" if not failures else "REVIEW_REQUIRED"
        any_failure |= bool(failures)
        model_report = {"provider": provider, "role": role, "model": model, "status": status, **scores, "threshold_failures": failures}
        report["models"].append(model_report)
        (out / f"{safe_name(provider, role, model)}.json").write_text(json.dumps(model_report, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({
            "provider": provider,
            "role": role,
            "model": model,
            "status": status,
            "activation": {k: v for k, v in activation.items() if k != "details"},
            "composition": {k: v for k, v in composition.items() if k != "details"},
            "behavioral_lexical": {k: v for k, v in behavioral.items() if k != "details"},
            "threshold_failures": failures,
        }, indent=2), flush=True)

    report["status"] = "PASS" if not any_failure else "REVIEW_REQUIRED"
    (out / "report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if any_failure:
        raise SystemExit(3)


if __name__ == "__main__":
    main()

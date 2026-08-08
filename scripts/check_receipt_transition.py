#!/usr/bin/env python3
"""Check that a receipt handoff does not silently become more certain.

This is intentionally small. It does not authenticate authors or transport.
It only catches evidence-free status upgrades, dropped unknowns, and claim-grade
changes between two otherwise valid Dale OS receipt objects.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

BLOCKING = {"UNRESOLVED", "WITHHELD", "BLOCKED"}
PUBLISHABLE = {"DEGRADED", "PASS"}
REQUIRED = {"schema", "skill", "status", "summary", "claims", "unknowns", "mutations", "verification"}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: receipt must be an object")
    missing = REQUIRED - set(value)
    if missing:
        raise ValueError(f"{path}: missing required fields {sorted(missing)}")
    if value.get("schema") != "dale-os/receipt/v1":
        raise ValueError(f"{path}: unsupported receipt schema")
    return value


def claim_map(receipt: dict) -> dict[str, dict]:
    out = {}
    for claim in receipt.get("claims", []):
        if isinstance(claim, dict) and isinstance(claim.get("claim"), str):
            out[claim["claim"]] = claim
    return out


def check(parent: dict, child: dict) -> list[str]:
    errors: list[str] = []
    parent_verification = set(parent.get("verification", []))
    child_verification = set(child.get("verification", []))
    new_verification = child_verification - parent_verification

    if parent.get("status") in BLOCKING and child.get("status") in PUBLISHABLE and not new_verification:
        errors.append("blocking status upgraded without new verification evidence")

    removed_unknowns = set(parent.get("unknowns", [])) - set(child.get("unknowns", []))
    if removed_unknowns and not new_verification:
        errors.append("unknowns disappeared without new verification evidence: " + ", ".join(sorted(removed_unknowns)))

    parent_claims = claim_map(parent)
    child_claims = claim_map(child)
    for text, child_claim in child_claims.items():
        parent_claim = parent_claims.get(text)
        if parent_claim and parent_claim.get("evidence_grade") != child_claim.get("evidence_grade"):
            new_claim_evidence = set(child_claim.get("evidence", [])) - set(parent_claim.get("evidence", []))
            if not new_verification and not new_claim_evidence:
                errors.append(f"claim evidence grade changed without new evidence: {text}")

    if parent.get("status") in BLOCKING and child_claims.keys() - parent_claims.keys() and not new_verification:
        errors.append("new claims added to a blocking receipt without new verification evidence")

    return errors


def run_fixtures(path: Path) -> int:
    doc = json.loads(path.read_text(encoding="utf-8"))
    failures = []
    for case in doc.get("cases", []):
        errors = check(case["parent"], case["child"])
        actual = "PASS" if not errors else "FAIL"
        if actual != case["expected"]:
            failures.append(f"{case['id']}: expected {case['expected']}, got {actual}: {errors}")
    if failures:
        print("RECEIPT TRANSITION FIXTURES FAILED")
        for failure in failures:
            print("-", failure)
        return 1
    print(f"RECEIPT TRANSITION PASS: {len(doc.get('cases', []))} adversarial handoffs")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("parent", nargs="?", type=Path)
    parser.add_argument("child", nargs="?", type=Path)
    parser.add_argument("--fixtures", type=Path)
    args = parser.parse_args()

    if args.fixtures:
        return run_fixtures(args.fixtures)
    if not args.parent or not args.child:
        parser.error("provide parent and child receipts, or --fixtures")

    errors = check(load(args.parent), load(args.child))
    if errors:
        print("RECEIPT TRANSITION BLOCKED")
        for error in errors:
            print("-", error)
        return 1
    print("RECEIPT TRANSITION PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

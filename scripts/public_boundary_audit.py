#!/usr/bin/env python3
"""Conservative pre-public scan for obvious secrets, private data, and unsupported claims."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {'.md', '.txt', '.json', '.yaml', '.yml', '.py', '.ts', '.cff'}
SKIP_PARTS = {'.git', 'node_modules', '__pycache__'}
errors = []

SECRET_PATTERNS = {
    'OpenAI-style secret': re.compile(r'\bsk-[A-Za-z0-9_-]{20,}\b'),
    'GitHub classic token': re.compile(r'\bgh[pousr]_[A-Za-z0-9]{20,}\b'),
    'GitHub fine-grained token': re.compile(r'\bgithub_pat_[A-Za-z0-9_]{20,}\b'),
    'AWS access key': re.compile(r'\bAKIA[0-9A-Z]{16}\b'),
    'private key block': re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
}
PRIVATE_PATTERNS = {
    'labeled financial account number': re.compile(r'(?i)(?:brokerage|account|acct)\s*(?:number|#|no\.)\s*[:=]?\s*[0-9-]{6,}'),
    'labeled SSN': re.compile(r'(?i)(?:ssn|social security)\s*[:=]?\s*\d{3}-?\d{2}-?\d{4}'),
}
PROPRIETARY_PATTERNS = {
    'ACF scoring weights': re.compile(r'(?is)(?:CIS|Convexity Index Score).{0,120}(?:40%|25%|10%).{0,120}(?:40%|25%|10%)'),
}

for p in ROOT.rglob('*'):
    if not p.is_file() or any(part in SKIP_PARTS for part in p.parts):
        continue
    if p.suffix.lower() not in TEXT_SUFFIXES and p.name not in {'AGENTS.md', 'GEMINI.md'}:
        continue
    text = p.read_text(encoding='utf-8', errors='ignore')
    rel = p.relative_to(ROOT)
    for label, pattern in {**SECRET_PATTERNS, **PRIVATE_PATTERNS, **PROPRIETARY_PATTERNS}.items():
        if pattern.search(text):
            errors.append(f'{rel}: {label}')

# These phrases are acceptable in documents that explicitly forbid the claim, but not as positive README positioning.
readme = (ROOT / 'README.md').read_text(encoding='utf-8')
for phrase in ('RIA grade', 'RIA-grade', 'SEC compliant', 'SEC-compliant', 'institutional grade', 'institutional-grade'):
    if phrase.lower() in readme.lower():
        errors.append(f'README.md: unsupported certification-style positioning: {phrase}')

# Private build may contain the public/private boundary docs, but never a real dotenv file.
for forbidden in ('.env', '.env.local', '.env.production'):
    if (ROOT / forbidden).exists():
        errors.append(f'{forbidden}: dotenv files must not be committed')

if errors:
    print('PUBLIC BOUNDARY AUDIT FAILED')
    for error in errors:
        print('-', error)
    raise SystemExit(1)

print('PUBLIC BOUNDARY AUDIT PASS: no obvious secrets, labeled private account data, ACF scoring weights, or unsupported README certification claims')

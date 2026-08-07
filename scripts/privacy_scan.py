#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import re, subprocess
ROOT=Path(__file__).resolve().parents[1]
errors=[]

def fail(msg): errors.append(msg)

r=subprocess.run(['git','ls-files','-z'],cwd=ROOT,capture_output=True)
if r.returncode:
    raise SystemExit('git ls-files failed')
tracked=[Path(x.decode()) for x in r.stdout.split(b'\0') if x]

forbidden_names={'.env','.env.local','.env.production','id_rsa','id_ed25519'}
forbidden_suffixes={'.pem','.key','.p12','.pfx','.kdbx','.sqlite','.db','.qfx','.ofx','.xlsx','.xls'}
for path in tracked:
    rel=str(path)
    if path.name in forbidden_names or path.suffix.lower() in forbidden_suffixes:
        fail(f'sensitive release file type/name: {rel}')
    if path.parts and path.parts[0]=='second-brain':
        fail(f'internal Second Brain artifact on release surface: {rel}')
    full=ROOT/path
    if not full.is_file() or full.stat().st_size>2_000_000:
        continue
    text=full.read_text(encoding='utf-8',errors='ignore')
    patterns={
      'private-key': r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
      'openai-like-secret': r'\bsk-[A-Za-z0-9_-]{16,}',
      'github-like-token': r'\bgh[pousr]_[A-Za-z0-9]{20,}',
      'aws-access-key': r'\bAKIA[0-9A-Z]{16}\b',
      'labeled-account-number': r'(?i)\b(?:account|acct)[ _-]?(?:number|no\.?|id)\s*[:=]\s*[A-Za-z0-9*_-]{6,}',
      'acf-cis-weight-leak': r'(?is)(?:Convexity Index Score|\bCIS\b).{0,120}(?:40\s*%|25\s*%|weighted component|formula weight)'
    }
    for label,pat in patterns.items():
        if re.search(pat,text): fail(f'{rel}: potential {label}')

if errors:
    print('PRIVACY SCAN FAILED')
    for e in errors: print('-',e)
    raise SystemExit(1)
print(f'PRIVACY PASS: {len(tracked)} tracked files scanned; no blocked release artifacts or configured sensitive patterns found')

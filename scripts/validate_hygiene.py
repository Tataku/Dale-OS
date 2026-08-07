#!/usr/bin/env python3
from __future__ import annotations
import json, re, subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
errors=[]

def fail(message):
    errors.append(message)

def tracked_files():
    result=subprocess.run(['git','ls-files'],cwd=ROOT,capture_output=True,text=True,check=True)
    return [ROOT/p for p in result.stdout.splitlines() if p]

tracked=tracked_files()
tracked_rel={str(path.relative_to(ROOT)) for path in tracked}
version=(ROOT/'VERSION').read_text(encoding='utf-8').strip()
if not re.fullmatch(r'\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?',version):
    fail(f'VERSION: invalid version {version!r}')

manifest=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
index=json.loads((ROOT/'machine'/'agent-index.json').read_text(encoding='utf-8'))
citation=(ROOT/'CITATION.cff').read_text(encoding='utf-8')
changelog=(ROOT/'CHANGELOG.md').read_text(encoding='utf-8')

if manifest.get('version')!=version:
    fail(f'manifest.json: version {manifest.get("version")!r} != VERSION {version!r}')
if index.get('version')!=version:
    fail(f'machine/agent-index.json: version {index.get("version")!r} != VERSION {version!r}')
if not re.search(rf'^version:\s*["\']?{re.escape(version)}["\']?\s*$',citation,re.M):
    fail('CITATION.cff: version drift from VERSION')
if f'## {version} ' not in changelog:
    fail('CHANGELOG.md: current VERSION heading missing')

markdown_link=re.compile(r'\[[^\]]*\]\(([^)]+)\)')
for path in tracked:
    if path.suffix.lower()!='.md':
        continue
    text=path.read_text(encoding='utf-8',errors='ignore')
    for raw in markdown_link.findall(text):
        target=raw.strip().split()[0].strip('<>')
        if not target or target.startswith(('#','http://','https://','mailto:')):
            continue
        target=target.split('#',1)[0].split('?',1)[0]
        if not target:
            continue
        resolved=(path.parent/target).resolve()
        try:
            resolved.relative_to(ROOT.resolve())
        except ValueError:
            fail(f'{path.relative_to(ROOT)}: relative link escapes repository: {raw}')
            continue
        if not resolved.exists():
            fail(f'{path.relative_to(ROOT)}: broken relative link: {raw}')

# Construct retired names so this validator does not match itself during content scanning.
retired_paths={
    'docs/'+'RELEASE_READINESS.md',
    'LICENSE_'+'PENDING.md',
}
for retired_path in retired_paths:
    if retired_path in tracked_rel:
        fail(f'retired path is still tracked: {retired_path}')

retired_markers=[
    *retired_paths,
    'second-'+'brain/',
    '0.1.0-'+'dev',
    'private '+'foundation',
]
text_suffixes={'.md','.txt','.json','.yaml','.yml','.cff','.py'}
for path in tracked:
    if path==Path(__file__).resolve() or path.suffix.lower() not in text_suffixes:
        continue
    text=path.read_text(encoding='utf-8',errors='ignore')
    for marker in retired_markers:
        if marker in text:
            fail(f'{path.relative_to(ROOT)}: retired marker present: {marker}')

required_root={
    'README.md','AGENTS.md','INSTALL.md','PRINCIPLES.md','ARCHITECTURE.md','PROOF.md',
    'ROADMAP.md','CHANGELOG.md','CONTRIBUTING.md','GOVERNANCE.md','SECURITY.md',
    'RECEIPTS.md','CHALLENGE.md','CITATION.cff','LICENSE','VERSION','llms.txt','manifest.json'
}
actual_root={p.name for p in ROOT.iterdir() if p.is_file() and not p.name.startswith('.')}
missing=sorted(required_root-actual_root)
if missing:
    fail(f'root contract missing files: {missing}')

if errors:
    print('HYGIENE VALIDATION FAILED')
    for error in errors:
        print('-',error)
    raise SystemExit(1)
print(f'HYGIENE PASS: version {version}, relative links valid, retired paths/markers absent, root contract intact')

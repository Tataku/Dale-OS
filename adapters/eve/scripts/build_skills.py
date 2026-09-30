#!/usr/bin/env python3
from pathlib import Path
import shutil

HERE=Path(__file__).resolve()
EVE=HERE.parents[1]
ROOT=EVE.parents[1]
OUT=EVE/'agent'/'skills'
REFS=OUT/'references'

OUT.mkdir(parents=True, exist_ok=True)
for old in OUT.glob('*.md'):
    old.unlink()
if REFS.exists():
    shutil.rmtree(REFS)

count=0
reference_count=0
for src in sorted((ROOT/'skills').glob('*/*/SKILL.md')):
    skill_name=src.parent.name
    text=src.read_text(encoding='utf-8')
    src_refs=src.parent/'references'

    if src_refs.exists():
        dst_refs=REFS/skill_name
        shutil.copytree(src_refs, dst_refs)
        reference_count += sum(1 for p in src_refs.rglob('*') if p.is_file())
        text=text.replace('(references/', f'(references/{skill_name}/')

    (OUT/f'{skill_name}.md').write_text(text, encoding='utf-8')
    count+=1

print(f'built {count} eve skills + {reference_count} reference files')

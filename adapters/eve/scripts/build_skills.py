#!/usr/bin/env python3
from pathlib import Path
import shutil
HERE=Path(__file__).resolve(); EVE=HERE.parents[1]; ROOT=EVE.parents[1]; OUT=EVE/'agent'/'skills'
OUT.mkdir(parents=True, exist_ok=True)
for old in OUT.glob('*.md'): old.unlink()
count=0
for src in sorted((ROOT/'skills').glob('*/*/SKILL.md')):
    shutil.copyfile(src, OUT/f'{src.parent.name}.md'); count+=1
print(f'built {count} eve skills')
